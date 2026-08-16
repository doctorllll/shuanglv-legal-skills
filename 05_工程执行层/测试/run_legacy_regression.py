#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json, importlib.util, tempfile, shutil
ROOT=Path(__file__).resolve().parents[2]
EXEC=ROOT/'05_工程执行层/工具/爽律 Skill执行器.py'
FLAGS=ROOT/'05_工程执行层/配置/功能开关.json'
CASES=Path(__file__).with_name('legacy_regression_cases.json')
spec=importlib.util.spec_from_file_location('shuanglv_executor',EXEC); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base=json.loads(FLAGS.read_text(encoding='utf-8')); cases=json.loads(CASES.read_text(encoding='utf-8'))['cases']
results=[]
# A. Router v2 OFF must match v0.42 baseline
try:
    off=json.loads(json.dumps(base,ensure_ascii=False)); off['flags']['skill_router_v2']['enabled']=False
    FLAGS.write_text(json.dumps(off,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for c in cases:
        st,lead,cands,ranked,meta=m.route_task_safe(c['task'],None)
        results.append({'id':c['id']+'-FLAG-OFF','pass':lead==c['expected_lead'] and meta.get('used_legacy') is True,'lead':lead,'meta':meta})
finally:
    FLAGS.write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# B. Router v2 exception must fallback
orig=m.route_task_v043
def broken(*a,**k): raise RuntimeError('simulated router failure')
m.route_task_v043=broken
for c in cases:
    st,lead,cands,ranked,meta=m.route_task_safe(c['task'],None)
    results.append({'id':c['id']+'-ROUTER-FAIL','pass':lead==c['expected_lead'] and meta.get('used_legacy') is True,'lead':lead,'meta':meta})
m.route_task_v043=orig
# C. AutoActivation OFF must not break explicit alias
try:
    off=json.loads(json.dumps(base,ensure_ascii=False)); off['flags']['auto_activation']['enabled']=False
    FLAGS.write_text(json.dumps(off,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    r=m.activation_decision('调用爽律审查这个合同')
    results.append({'id':'LEGACY-EXPLICIT-AUTO-OFF','pass':r.get('decision')=='EXPLICIT_ACTIVATE','decision':r})
finally:
    FLAGS.write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# D. Corrupt auto-activation rules: explicit alias still works
orig_text=(ROOT/'05_工程执行层/配置/自动激活规则.json').read_text(encoding='utf-8')
try:
    (ROOT/'05_工程执行层/配置/自动激活规则.json').write_text('{broken',encoding='utf-8')
    r=m.activation_decision('调用爽律研究这个法律问题')
    results.append({'id':'LEGACY-EXPLICIT-CONFIG-BROKEN','pass':r.get('decision')=='EXPLICIT_ACTIVATE','decision':r})
finally:
    (ROOT/'05_工程执行层/配置/自动激活规则.json').write_text(orig_text,encoding='utf-8')
# E. Proactive suggestion OFF is non-blocking by contract
results.append({'id':'LEGACY-PROACTIVE-NONBLOCKING','pass':base['flags']['proactive_suggestion']['blocking'] is False and base['flags']['proactive_suggestion']['fallback']=='NO_SUGGESTION'})
# F. Multi-skill collaboration OFF has downgrade fallback
results.append({'id':'LEGACY-COLLAB-NONBLOCKING','pass':base['flags']['multi_skill_collaboration']['blocking'] is False and base['flags']['multi_skill_collaboration']['fallback']=='V0.42_CAPABILITY_ADAPTATION'})
passed=sum(1 for x in results if x['pass']); total=len(results)
report={'suite':'Legacy Regression Gate','baseline':'v0.42-RC6','passed':passed,'total':total,'status':'PASS' if passed==total else 'FAIL','results':results}
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if passed==total else 3)
