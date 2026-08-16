#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""爽律升级助手 ShuangLaw Upgrade Assistant v0.2

目标：在升级 Core 时默认保留用户个性化；识别硬规则冲突、旧 Core 直接修改和无法迁移项。
本工具不自建云端记忆，不上传用户数据。
"""
from __future__ import annotations
import argparse, json, hashlib, shutil, zipfile
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/'05_工程执行层'/'配置'/'个性化键注册表.json'
DEFAULTS=ROOT/'05_工程执行层'/'配置'/'个性化默认设置.json'
TEMPLATE_SCHEMA_VERSION='0.1'

def now(): return datetime.now(timezone.utc).isoformat()
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def dump(obj,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def init_user_space(path:Path):
    path.mkdir(parents=True,exist_ok=True)
    for d in ['matters','custom-rules','custom-templates','snapshots','migrations','legacy-customizations']:
        (path/d).mkdir(exist_ok=True)
    profile=path/'user-profile.json'
    if not profile.exists():
        dump({"schema_version":"0.1","profile_id":"USER-PROFILE-001","profile_type":"USER","owner_label":None,
              "created_at":now(),"updated_at":now(),"last_migrated_from":None,"last_migrated_to":None,
              "default_upgrade_policy":"PRESERVE_USER","settings":[],"custom_assets":[],"template_asset_ids":[],"notes":[]}, profile)
    treg=path/'template-assets.json'
    if not treg.exists():
        dump({"schema_version":TEMPLATE_SCHEMA_VERSION,"registry_id":"USER-TEMPLATE-REGISTRY","updated_at":now(),"assets":[],"notes":[]},treg)
    return profile

def snapshot(user_space:Path,label:str):
    src=user_space/'user-profile.json'
    if not src.exists(): return None
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
    out=user_space/'snapshots'/f'{stamp}_{label}_user-profile.json'
    out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out); return str(out)

def is_guardrail(key, reg):
    meta=reg.get('keys',{}).get(key)
    if meta is not None: return not bool(meta.get('overridable',True))
    return any(key.startswith(p) for p in reg.get('reserved_hard_guardrail_prefixes',[]))

def registered(key, reg): return key in reg.get('keys',{})

def migrate_profile(profile, manifest, policy, reg):
    renamed=manifest.get('renamed_keys',{}) or {}; removed=set(manifest.get('removed_keys',[]) or [])
    items=[]; out_settings=[]; counts={"preserved":0,"migrated":0,"review_required":0,"blocked":0,"orphaned":0}
    for s0 in profile.get('settings',[]):
        s=dict(s0); old_key=s.get('key'); key=renamed.get(old_key,old_key); result='PRESERVED'; reason='兼容设置，按默认策略保留。'; old_value=s.get('value')
        if key!=old_key:
            s['key']=key; result='MIGRATED'; reason=f'设置键由 {old_key} 迁移为 {key}。'; counts['migrated']+=1
        elif key in removed:
            s['status']='ORPHANED'; result='ORPHANED'; reason='新版已移除此设置键，保留历史但不再生效。'; counts['orphaned']+=1
        elif is_guardrail(key,reg):
            hard_default=(reg.get('keys',{}).get(key) or {}).get('default')
            if old_value==hard_default:
                s['status']='DISABLED'; result='DISABLED'; reason='该项与不可覆盖硬规则一致，无需继续作为个性化 override 生效。'; counts['migrated']+=1
            else:
                s['status']='BLOCKED_BY_GUARDRAIL'; result='BLOCKED_BY_GUARDRAIL'; reason='该键属于不可覆盖硬规则；旧个性化与核心边界冲突，已阻止生效并保留记录。'; counts['blocked']+=1
        elif not registered(key,reg):
            result='REVIEW_REQUIRED'; reason='该设置键未登记，暂保留但升级后需人工确认其语义。'; counts['review_required']+=1
        elif policy=='ADOPT_NEW_DEFAULTS':
            default=reg['keys'][key].get('default')
            s['value']=default; s['status']='ACTIVE'; result='ADOPTED_NEW_DEFAULT'; reason='用户选择采用新版默认值。'; counts['migrated']+=1
        elif policy=='REVIEW_ALL':
            result='REVIEW_REQUIRED'; reason='用户选择逐项审阅。'; counts['review_required']+=1
        else:
            counts['preserved']+=1
        s['registered']=registered(key,reg); s['updated_at']=now(); out_settings.append(s)
        items.append({"setting_id":s.get('setting_id','UNKNOWN'),"key":key,"result":result,"old_value":old_value,"new_value":s.get('value'),"reason":reason})
    new=dict(profile); new['settings']=out_settings; new['updated_at']=now(); new['last_migrated_from']=manifest.get('from_version'); new['last_migrated_to']=manifest.get('to_version')
    status='PASS_WITH_REVIEW' if (counts['blocked'] or counts['review_required']) else 'PASS'
    report={"schema_version":"0.1","from_version":manifest.get('from_version'),"to_version":manifest.get('to_version'),"policy":policy,"status":status,"created_at":now(),"summary":counts,"items":items,"legacy_core_customizations":[],"snapshot_path":None,"notes":[]}
    return new, report

def scan_legacy_core(old_install:Path, baseline):
    files=baseline.get('files',{}); found=[]
    for rel,expected in files.items():
        p=old_install/rel
        if not p.exists(): found.append({"path":rel,"status":"DELETED","sha256":None}); continue
        actual=sha(p)
        if actual!=expected: found.append({"path":rel,"status":"MODIFIED","sha256":actual})
    baseline_set=set(files)
    for p in old_install.rglob('*'):
        if p.is_file():
            rel=p.relative_to(old_install).as_posix()
            if rel not in baseline_set: found.append({"path":rel,"status":"ADDED","sha256":sha(p)})
    return found

def cmd_init(a):
    p=init_user_space(Path(a.user_space)); print(p); return 0

def cmd_show(a):
    p=load(Path(a.user_space)/'user-profile.json')
    active=[s for s in p.get('settings',[]) if s.get('status')=='ACTIVE']
    print(f"当前 ACTIVE 个性化：{len(active)} 项")
    for s in active: print(f"- {s.get('setting_id')}: {s.get('key')} = {s.get('value')!r}")
    return 0

def cmd_migrate(a):
    us=Path(a.user_space); init_user_space(us); profile=load(us/'user-profile.json'); manifest=load(a.manifest); reg=load(REGISTRY)
    policy=a.policy or profile.get('default_upgrade_policy') or manifest.get('default_policy') or 'PRESERVE_USER'
    new,report=migrate_profile(profile,manifest,policy,reg)
    if a.old_install and a.baseline_manifest:
        legacy=scan_legacy_core(Path(a.old_install),load(a.baseline_manifest)); report['legacy_core_customizations']=legacy
        if legacy: report['status']='PASS_WITH_REVIEW' if report['status']=='PASS' else report['status']; report['notes'].append(f'检测到 {len(legacy)} 个旧 Core 差异，需审阅后再迁入用户空间。')
        if a.extract_legacy and legacy:
            out=us/'legacy-customizations'; out.mkdir(exist_ok=True)
            for item in legacy:
                if item['status'] in {'MODIFIED','ADDED'}:
                    src=Path(a.old_install)/item['path']
                    if src.exists():
                        dst=out/item['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
    report_path=Path(a.report) if a.report else us/'migrations'/f"{manifest.get('from_version')}_to_{manifest.get('to_version')}_migration-report.json"
    if a.apply:
        report['snapshot_path']=snapshot(us,f"before_{manifest.get('to_version')}")
        dump(new,us/'user-profile.json')
    else:
        candidate=us/'migrations'/f"{manifest.get('from_version')}_to_{manifest.get('to_version')}_candidate-profile.json"; dump(new,candidate); report['notes'].append(f'尚未写回原档案；候选档案：{candidate}')
    dump(report,report_path); print(report_path); return 3 if report['status']=='BLOCKED' else 0

def cmd_export(a):
    us=Path(a.user_space); out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in us.rglob('*'):
            if p.is_file(): z.write(p,p.relative_to(us).as_posix())
    print(out); return 0

def cmd_reset(a):
    us=Path(a.user_space); init_user_space(us); profile=load(us/'user-profile.json'); ids=set(a.setting_id or []); keys=set(a.key or [])
    targets=[s for s in profile.get('settings',[]) if (not ids and not keys) or s.get('setting_id') in ids or s.get('key') in keys]
    if not a.apply:
        print(json.dumps({"would_disable":[{"setting_id":s.get('setting_id'),"key":s.get('key')} for s in targets],"apply":False},ensure_ascii=False,indent=2)); return 0
    snap=snapshot(us,'before_reset')
    for s in profile.get('settings',[]):
        if s in targets: s['status']='DISABLED'; s['updated_at']=now()
    profile['updated_at']=now(); dump(profile,us/'user-profile.json'); print(json.dumps({"disabled":len(targets),"snapshot":snap},ensure_ascii=False)); return 0


def cmd_health(a):
    us=Path(a.user_space); init_user_space(us); profile=load(us/'user-profile.json'); reg=load(REGISTRY)
    active=[x for x in profile.get('settings',[]) if x.get('status')=='ACTIVE']
    seen={}; duplicates=[]; redundant=[]; unregistered=[]; pending=[]
    for x in active:
        key=x.get('key'); seen.setdefault(key,[]).append(x.get('setting_id'))
        meta=reg.get('keys',{}).get(key)
        if meta and meta.get('overridable',True) and x.get('value')==meta.get('default'):
            redundant.append({"setting_id":x.get('setting_id'),"key":key,"reason":"与当前版本默认一致"})
        if not meta: unregistered.append({"setting_id":x.get('setting_id'),"key":key})
    for key,ids in seen.items():
        if len(ids)>1: duplicates.append({"key":key,"setting_ids":ids})
    for x in profile.get('settings',[]):
        if x.get('status') in {'SUGGESTED','DEPRECATED','ORPHANED','BLOCKED_BY_GUARDRAIL'}:
            pending.append({"setting_id":x.get('setting_id'),"key":x.get('key'),"status":x.get('status')})
    report={"active_count":len(active),"redundant_with_current_default":redundant,"duplicate_active_keys":duplicates,"unregistered_active_keys":unregistered,"needs_review_or_cleanup":pending,"note":"体检只提出建议，不自动删除或关闭 ACTIVE 设置。"}
    if a.out: dump(report,a.out)
    else: print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

def _safe_member(name:str):
    p=Path(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts

def _merge_custom_assets(current, imported):
    items={x.get('asset_id'):x for x in (current or []) if isinstance(x,dict) and x.get('asset_id')}
    for x in imported or []:
        if isinstance(x,dict) and x.get('asset_id') and x.get('asset_id') not in items:
            items[x.get('asset_id')]=x
    return list(items.values())

def _merge_template_registry(current, incoming, conflict_policy='preserve'):
    cur={x.get('asset_id'):x for x in current.get('assets',[]) if isinstance(x,dict) and x.get('asset_id')}
    decisions=[]
    for x in incoming.get('assets',[]) or []:
        aid=x.get('asset_id')
        if not aid: continue
        if aid not in cur:
            cur[aid]=x; decisions.append({'asset_id':aid,'result':'IMPORTED'})
        elif conflict_policy=='incoming':
            cur[aid]=x; decisions.append({'asset_id':aid,'result':'REPLACED_BY_EXPLICIT_USER_CHOICE'})
        elif conflict_policy=='rename-incoming':
            base=aid; n=2; new_id=f'{base}-IMPORTED-{n}'
            while new_id in cur: n+=1; new_id=f'{base}-IMPORTED-{n}'
            y=dict(x); y['asset_id']=new_id; cur[new_id]=y; decisions.append({'asset_id':aid,'result':'IMPORTED_WITH_NEW_ID','new_asset_id':new_id})
        else:
            decisions.append({'asset_id':aid,'result':'PRESERVED_CURRENT'})
    out=dict(current); out['assets']=list(cur.values()); out['updated_at']=now(); return out, decisions

def cmd_import(a):
    us=Path(a.user_space); init_user_space(us); bundle=Path(a.bundle)
    with zipfile.ZipFile(bundle,'r') as z:
        names=[n for n in z.namelist() if _safe_member(n)]
        try: imported=json.loads(z.read('user-profile.json').decode('utf-8'))
        except KeyError: raise SystemExit('导入包缺少 user-profile.json')
        try: incoming_templates=json.loads(z.read('template-assets.json').decode('utf-8'))
        except KeyError: incoming_templates={"schema_version":TEMPLATE_SCHEMA_VERSION,"registry_id":"IMPORTED","assets":[],"notes":[]}
        current=load(us/'user-profile.json')
        current_templates=load(us/'template-assets.json')
        if a.policy=='replace':
            candidate=imported
        else:
            candidate=dict(current); existing={(x.get('scope'),x.get('matter_id'),x.get('key')):x for x in current.get('settings',[])}
            for x in imported.get('settings',[]): existing[(x.get('scope'),x.get('matter_id'),x.get('key'))]=x
            candidate['settings']=list(existing.values())
            candidate['custom_assets']=_merge_custom_assets(current.get('custom_assets'),imported.get('custom_assets'))
            candidate['template_asset_ids']=list(dict.fromkeys((current.get('template_asset_ids') or [])+(imported.get('template_asset_ids') or [])))
            candidate['updated_at']=now(); candidate.setdefault('notes',[]).append(f'从 {bundle.name} 合并导入。')
        merged_templates,decisions=_merge_template_registry(current_templates,incoming_templates,a.asset_conflict)
        preview={"policy":a.policy,"asset_conflict":a.asset_conflict,"current_settings":len(current.get('settings',[])),"imported_settings":len(imported.get('settings',[])),"candidate_settings":len(candidate.get('settings',[])),"template_decisions":decisions,"apply":bool(a.apply)}
        if not a.apply:
            print(json.dumps(preview,ensure_ascii=False,indent=2)); return 0
        snap=snapshot(us,'before_import')
        # Import template files. Default conflict policy is preserve current; never silently overwrite.
        for name in names:
            if not name.startswith('custom-templates/') or name.endswith('/'):
                continue
            dst=us/name; dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.exists() and a.asset_conflict=='preserve':
                continue
            if dst.exists() and a.asset_conflict=='incoming':
                stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
                backup=us/'snapshots'/'assets'/stamp/name
                backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(dst,backup)
            if dst.exists() and a.asset_conflict=='rename-incoming':
                stem,suffix=dst.stem,dst.suffix; n=2; ndst=dst.with_name(f'{stem}-imported-{n}{suffix}')
                while ndst.exists(): n+=1; ndst=dst.with_name(f'{stem}-imported-{n}{suffix}')
                dst=ndst
            with z.open(name) as src, open(dst,'wb') as out: shutil.copyfileobj(src,out)
        dump(candidate,us/'user-profile.json'); dump(merged_templates,us/'template-assets.json')
        preview['snapshot']=snap; print(json.dumps(preview,ensure_ascii=False,indent=2)); return 0

def cmd_template_list(a):
    us=Path(a.user_space); init_user_space(us); reg=load(us/'template-assets.json')
    items=[x for x in reg.get('assets',[]) if x.get('status')=='ACTIVE']
    print(json.dumps(items,ensure_ascii=False,indent=2)); return 0

def cmd_template_resolve(a):
    us=Path(a.user_space); init_user_space(us); reg=load(us/'template-assets.json')
    active=[x for x in reg.get('assets',[]) if x.get('status')=='ACTIVE' and (a.document_type in (x.get('document_types') or []) or '*' in (x.get('document_types') or []))]
    if a.asset_id:
        hit=[x for x in active if x.get('asset_id')==a.asset_id]
        result={'resolution':'EXPLICIT' if hit else 'MISSING_EXPLICIT_ASSET','selected':hit[0] if hit else None,'fallback_to_core_allowed':False if not hit else None}
    else:
        matter=[x for x in active if x.get('scope')=='MATTER' and a.matter_id and x.get('scope_ref')==a.matter_id]
        user=[x for x in active if x.get('scope')=='USER']
        candidates=matter or user
        if len(candidates)>1:
            result={'resolution':'CONFLICT_REVIEW_REQUIRED','selected':None,'candidate_asset_ids':[x.get('asset_id') for x in candidates],'fallback_to_core_allowed':False}
        else:
            selected=(candidates or [None])[0]
            result={'resolution':'MATTER' if matter else ('USER' if user else 'CORE_DEFAULT_AVAILABLE'),'selected':selected,'fallback_to_core_allowed':selected is None}
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0

def main():
    ap=argparse.ArgumentParser(description='爽律升级助手')
    sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('init'); p.add_argument('--user-space',required=True); p.set_defaults(func=cmd_init)
    p=sub.add_parser('show'); p.add_argument('--user-space',required=True); p.set_defaults(func=cmd_show)
    p=sub.add_parser('migrate'); p.add_argument('--user-space',required=True); p.add_argument('--manifest',required=True); p.add_argument('--policy',choices=['PRESERVE_USER','ADOPT_NEW_DEFAULTS','REVIEW_ALL']); p.add_argument('--old-install'); p.add_argument('--baseline-manifest'); p.add_argument('--extract-legacy',action='store_true'); p.add_argument('--apply',action='store_true'); p.add_argument('--report'); p.set_defaults(func=cmd_migrate)
    p=sub.add_parser('export'); p.add_argument('--user-space',required=True); p.add_argument('--out',required=True); p.set_defaults(func=cmd_export)
    p=sub.add_parser('reset'); p.add_argument('--user-space',required=True); p.add_argument('--setting-id',action='append'); p.add_argument('--key',action='append'); p.add_argument('--apply',action='store_true'); p.set_defaults(func=cmd_reset)
    p=sub.add_parser('health'); p.add_argument('--user-space',required=True); p.add_argument('--out'); p.set_defaults(func=cmd_health)
    p=sub.add_parser('import'); p.add_argument('--user-space',required=True); p.add_argument('--bundle',required=True); p.add_argument('--policy',choices=['merge','replace'],default='merge'); p.add_argument('--asset-conflict',choices=['preserve','incoming','rename-incoming'],default='preserve'); p.add_argument('--apply',action='store_true'); p.set_defaults(func=cmd_import)
    p=sub.add_parser('template-list'); p.add_argument('--user-space',required=True); p.set_defaults(func=cmd_template_list)
    p=sub.add_parser('template-resolve'); p.add_argument('--user-space',required=True); p.add_argument('--document-type',required=True); p.add_argument('--matter-id'); p.add_argument('--asset-id'); p.set_defaults(func=cmd_template_resolve)
    a=ap.parse_args(); return a.func(a)
if __name__=='__main__': raise SystemExit(main())
