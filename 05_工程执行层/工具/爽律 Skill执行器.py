#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""爽律 Skill 工程执行器（可选执行增强层）。

只做：任务路由辅助、渐进式加载计划、动态清单、外部能力解析、跨模块交接检查、全链路溯源检查、质量门控。
不做：实体法律判断、法条有效性自动认定、胜诉/定罪概率预测。
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
ENG = ROOT / "05_工程执行层"
LOAD_MANIFEST = ENG / "配置" / "加载清单.json"
CHECKLIST_REGISTRY = ENG / "配置" / "动态清单注册表.json"
PERSONALIZATION_REGISTRY = ENG / "配置" / "个性化键注册表.json"
PERSONALIZATION_DEFAULTS = ENG / "配置" / "个性化默认设置.json"
ACTIVATION_RULES = ENG / "配置" / "自动激活规则.json"
FEATURE_FLAGS = ENG / "配置" / "功能开关.json"
LEGACY_ALIASES = ["爽律","调用爽律","用爽律处理","用爽律做","爽律 skill","爽律 skills","shuanglaw"]
LEGACY_OPT_OUT = ["不要用爽律","不用爽律","这次别用爽律","不要调用爽律"]

SKILLS = [
    "刑事案件办理","民商事争议解决","合同与交易工作","法律研究与多源资料融合",
    "法律顾问与专项法律分析","尽职调查与专项调查","法律文书质量与格式控制","多模态输入适配（可选）"
]

ROUTE_KEYWORDS = {
    "刑事案件办理": ["刑事","犯罪","罪名","辩护","被害人","控告","报案","立案监督","阅卷","会见","逮捕","批捕","取保","认罪认罚","侦查","检察院","起诉书","量刑"],
    "民商事争议解决": ["民事","商事","诉讼","仲裁","起诉","答辩","上诉","再审","保全","执行","请求权","抗辩","举证"],
    "合同与交易工作": ["合同","协议","条款","交易","谈判","合同审查","合同起草","合同修改","修订合同","履行"],
    "法律研究与多源资料融合": ["法律研究","案例检索","法条检索","司法解释","类案","检索","现行法","法律依据","效力"],
    "法律顾问与专项法律分析": ["法律意见","法律咨询","专项分析","咨询意见","方案比较","法律顾问"],
    "尽职调查与专项调查": ["尽调","尽职调查","专项调查","背景调查","核查"],
    "法律文书质量与格式控制": ["文书润色","文书格式","排版","格式控制","校对","清洁稿","修订稿","批注"],
}

RESEARCH_HINTS = ["现行法","法律依据","法条","司法解释","案例","类案","效力","生效","失效","最新规定","权威来源","反向案例"]
STRUCTURED_REVIEW_HINTS = ["多文件","多份材料","大量材料","批量","卷宗","多版本","附件很多","交叉比对","证据冲突"]
BUNDLE_HINTS = ["整套材料","一整套","全套材料","全部材料","配套文书","成套交付","材料包","立案材料包","整套文件"]
TEMPLATE_HINTS = ["按我的模板","用我的模板","按照这个模板","按这个模板","指定模板","习惯模板","沿用模板"]

FORMAL_HINTS = ["正式文书","法律意见书","律师函","起诉状","答辩状","辩护词","上诉状","清洁稿","修订稿","批注","输出docx","生成docx","出docx","输出pdf","生成pdf","出pdf","word文档"]

TRUST_RANK = {
    "PRIMARY_AUTHORITY": 6,
    "AUTHORIZED_PROFESSIONAL": 5,
    "USER_CONTROLLED": 4,
    "RELIABLE_SECONDARY": 3,
    "GENERAL_WEB": 2,
    "MODEL_ONLY": 1,
    "NOT_APPLICABLE": 0,
}
STATUS_RANK = {
    "VERIFIED_SUPPORTED": 6,
    "DOWNGRADED": 5,
    "PARTIAL": 4,
    "SUPPORTED_BUT_UNVERIFIED": 3,
    "UNSUPPORTED": 1,
    "BLOCKED": 0,
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))



def resolve_personalization(user_profile_path=None, matter_profile_path=None):
    """解析版本默认、用户设置和事项设置；硬规则不可被覆盖。"""
    registry=load_json(PERSONALIZATION_REGISTRY) if PERSONALIZATION_REGISTRY.exists() else {"keys":{},"reserved_hard_guardrail_prefixes":[]}
    defaults=load_json(PERSONALIZATION_DEFAULTS).get("settings",{}) if PERSONALIZATION_DEFAULTS.exists() else {}
    effective=dict(defaults); applied=[]; warnings=[]; blocked=[]
    def is_guardrail(key):
        meta=registry.get("keys",{}).get(key)
        if meta is not None and not meta.get("overridable",True): return True
        return any(key.startswith(p) for p in registry.get("reserved_hard_guardrail_prefixes",[]))
    def apply_profile(path, layer):
        if not path: return
        prof=load_json(Path(path))
        for item in prof.get("settings",[]):
            if item.get("status")!="ACTIVE": continue
            key=item.get("key")
            if is_guardrail(key):
                blocked.append({"setting_id":item.get("setting_id"),"key":key,"layer":layer,"reason":"HARD_GUARDRAIL"}); continue
            if key not in registry.get("keys",{}):
                warnings.append({"setting_id":item.get("setting_id"),"key":key,"layer":layer,"reason":"UNREGISTERED_KEY"})
            effective[key]=item.get("value"); applied.append({"setting_id":item.get("setting_id"),"key":key,"layer":layer})
    apply_profile(user_profile_path,"USER")
    apply_profile(matter_profile_path,"MATTER")
    return {"effective_settings":effective,"applied":applied,"warnings":warnings,"blocked_overrides":blocked,
            "user_profile_loaded":bool(user_profile_path),"matter_profile_loaded":bool(matter_profile_path)}

def norm(s: str) -> str:
    return (s or "").strip().lower()


def load_feature_flags():
    """读取增强功能开关；配置缺失/损坏时默认关闭增强而不是关闭爽律 Core。"""
    safe={"policy":"ENHANCEMENT_ONLY_WITH_LEGACY_FALLBACK","flags":{
        "auto_activation":{"enabled":False},"skill_router_v2":{"enabled":False},
        "multi_skill_collaboration":{"enabled":False},"proactive_suggestion":{"enabled":False}}}
    try:
        if FEATURE_FLAGS.exists():
            data=load_json(FEATURE_FLAGS)
            if isinstance(data,dict): return data
    except Exception:
        pass
    return safe

def feature_enabled(name: str) -> bool:
    return bool(load_feature_flags().get("flags",{}).get(name,{}).get("enabled",False))

def activation_decision(task: str, user_profile_path=None, matter_profile_path=None):
    """本地回退/测试用激活判断。显式别名为永久保底入口；增强层异常时回退旧路径。"""
    t=norm(task)
    def raw_hits(items): return [x for x in items or [] if norm(x) in t]
    # 先用内置最小词表识别退出/显式入口，避免自动激活配置损坏时连旧入口一起失效。
    hard_optout=raw_hits(LEGACY_OPT_OUT)
    if hard_optout:
        return {"schema_version":"0.2","decision":"DO_NOT_ACTIVATE","activation_mode":"UNKNOWN","trigger_type":"USER_OPT_OUT","confidence_tier":"HIGH","reasons":["用户明确要求本次不使用爽律。"],"matched_signals":hard_optout,"show_notice":False,"user_preference_applied":True,"legacy_fallback":{"used":False,"reason":None},"notes":[]}
    hard_alias=raw_hits(LEGACY_ALIASES)
    if hard_alias:
        return {"schema_version":"0.2","decision":"EXPLICIT_ACTIVATE","activation_mode":"BYPASS","trigger_type":"EXPLICIT_ALIAS","confidence_tier":"HIGH","reasons":["检测到显式爽律调用；按兼容契约绕过 AutoActivation。"],"matched_signals":hard_alias,"show_notice":False,"user_preference_applied":False,"legacy_fallback":{"used":True,"reason":"EXPLICIT_ALIAS_BYPASS"},"notes":["显式调用不依赖自动激活模块。"]}
    try:
        prefs=resolve_personalization(user_profile_path,matter_profile_path)
        eff=prefs.get("effective_settings",{})
        mode=eff.get("activation.mode","AUTO")
        show_notice=bool(eff.get("activation.show_notice",False))
        threshold=eff.get("activation.auto_threshold","MEDIUM")
        if mode=="MANUAL":
            return {"schema_version":"0.2","decision":"MANUAL_ONLY","activation_mode":mode,"trigger_type":"NON_LEGAL","confidence_tier":"NONE","reasons":["用户个性化设置为MANUAL，仅显式调用时激活。"],"matched_signals":[],"show_notice":show_notice,"user_preference_applied":True,"legacy_fallback":{"used":False,"reason":None},"notes":[]}
        if not feature_enabled("auto_activation"):
            return {"schema_version":"0.2","decision":"LEGACY_FALLBACK","activation_mode":mode,"trigger_type":"FEATURE_DISABLED","confidence_tier":"NONE","reasons":["AutoActivation 已关闭；已进入 Skill 的任务回退 v0.42 路径。"],"matched_signals":[],"show_notice":show_notice,"user_preference_applied":mode!="AUTO","legacy_fallback":{"used":True,"reason":"AUTO_ACTIVATION_DISABLED"},"notes":["仅损失无感触发，不影响显式调用和已进入 Skill 的旧工作流。"]}
        rules=load_json(ACTIVATION_RULES) if ACTIVATION_RULES.exists() else {}
    except Exception as exc:
        return {"schema_version":"0.2","decision":"LEGACY_FALLBACK","activation_mode":"UNKNOWN","trigger_type":"ACTIVATION_ERROR","confidence_tier":"NONE","reasons":["自动激活增强层异常，回退 v0.42 已验证路径。"],"matched_signals":[],"show_notice":False,"user_preference_applied":False,"legacy_fallback":{"used":True,"reason":type(exc).__name__},"notes":["增强层错误不得阻断旧核心能力。"]}
    def hits(items): return [x for x in items or [] if norm(x) in t]
    optout=hits(rules.get("opt_out_phrases"))
    aliases=hits(rules.get("aliases"))
    high=hits(rules.get("high_intent_phrases"))
    actions=hits(rules.get("legal_action_terms"))
    objects=hits(rules.get("legal_object_terms"))
    negatives=hits(rules.get("negative_context_phrases"))
    reasons=[]; signals=[]
    if optout:
        return {"schema_version":"0.1","decision":"DO_NOT_ACTIVATE","activation_mode":mode,"trigger_type":"USER_OPT_OUT","confidence_tier":"HIGH","reasons":["用户明确要求本次不使用爽律。"],"matched_signals":optout,"show_notice":show_notice,"user_preference_applied":True,"notes":[]}
    if aliases:
        return {"schema_version":"0.1","decision":"EXPLICIT_ACTIVATE","activation_mode":mode,"trigger_type":"EXPLICIT_ALIAS","confidence_tier":"HIGH","reasons":["检测到爽律显式调用别名。"],"matched_signals":aliases,"show_notice":show_notice,"user_preference_applied":mode!="AUTO","notes":[]}
    if mode=="MANUAL":
        return {"schema_version":"0.1","decision":"MANUAL_ONLY","activation_mode":mode,"trigger_type":"NON_LEGAL" if not (high or (actions and objects)) else "SEMANTIC_PROFESSIONAL_LEGAL","confidence_tier":"NONE","reasons":["用户个性化设置为MANUAL，仅显式调用时激活。"],"matched_signals":high+actions+objects,"show_notice":show_notice,"user_preference_applied":True,"notes":[]}
    # 高置信：明确法律专业任务短语；或同时出现法律对象+专业动作，且不是明显非法律语境。
    tier="NONE"; trig="NON_LEGAL"
    if high:
        tier="HIGH"; trig="SEMANTIC_PROFESSIONAL_LEGAL"; reasons.append("命中明确法律专业任务语义。")
    elif actions and objects and not negatives:
        tier="MEDIUM"; trig="BOUNDARY_LEGAL"; reasons.append("同时存在法律对象与专业处理动作。")
    elif objects:
        tier="LOW"; trig="BOUNDARY_LEGAL"; reasons.append("仅检测到法律相关对象，尚不足以证明用户需要法律专业工作流。")
    else:
        tier="NONE"; trig="NON_LEGAL"; reasons.append("未发现需要律师专业工作流的充分信号。")
    signals=high+actions+objects+negatives
    if negatives and not high:
        tier="LOW" if objects else "NONE"; reasons.append("存在明显非法律任务语境，抑制误触发。")
    if mode=="CONFIRM" and tier in {"HIGH","MEDIUM"}:
        decision="CONFIRM"
    elif mode=="AUTO" and (tier=="HIGH" or (tier=="MEDIUM" and threshold in {"MEDIUM","LOW"})):
        decision="AUTO_ACTIVATE"
    elif tier=="MEDIUM":
        decision="CONFIRM"
    else:
        decision="DO_NOT_ACTIVATE"
    return {"schema_version":"0.1","decision":decision,"activation_mode":mode,"trigger_type":trig,"confidence_tier":tier,"reasons":reasons,"matched_signals":list(dict.fromkeys(signals)),"show_notice":show_notice,"user_preference_applied":mode!="AUTO" or eff.get("activation.auto_threshold")!="MEDIUM","legacy_fallback":{"used":False,"reason":None},"notes":["本地规则仅作回退/评测，不代表宿主Agent的真实语义触发概率。"]}


def score_route(task: str):
    t = norm(task)
    scores = {}
    for skill, kws in ROUTE_KEYWORDS.items():
        score = 0
        hits=[]
        for kw in kws:
            if norm(kw) in t:
                # longer phrases get slightly more weight; this is routing assistance, not probability
                w = 2 if len(kw) >= 4 else 1
                score += w
                hits.append(kw)
        scores[skill] = {"score": score, "hits": hits}
    ranked = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    return ranked


def route_task_v043(task: str, override: str | None):
    if override:
        if override not in SKILLS:
            raise SystemExit(f"未知技能：{override}\n可选：" + "、".join(SKILLS))
        return "USER_OVERRIDE", override, [override], []
    t=norm(task)
    ranked=score_route(task)
    # 明确业务事项优先于辅助能力。法律研究、文书质量通常作为 Supporting Skill，
    # 不能仅因任务同时要求查法条/案例或形成正式意见，就抢走案件/交易类 Lead。
    strong_business=None
    if any(k in t for k in ["辩护","被害人","控告","报案","立案监督","刑事案件","审查起诉","批捕","取保"]):
        strong_business="刑事案件办理"
    elif any(k in t for k in ["原告","被告","上诉人","被上诉人"]) and any(k in t for k in ["争议","诉讼","仲裁","起诉","答辩","上诉","执行","保全","案件"]):
        strong_business="民商事争议解决"
    elif any(k in t for k in ["合同审查","审合同","合同起草","起草合同","合同修改","修改合同","合同谈判","交易文件","协议审查"]):
        strong_business="合同与交易工作"
    elif any(k in t for k in ["尽职调查","尽调","专项调查"]):
        strong_business="尽职调查与专项调查"
    elif any(k in t for k in ["法律顾问","专项法律分析","专项意见"]) and not any(k in t for k in ["诉讼","仲裁","原告","被告","刑事","合同审查"]):
        strong_business="法律顾问与专项法律分析"
    if strong_business:
        return "RESOLVED", strong_business, [strong_business], ranked
    top=ranked[0][1]["score"] if ranked else 0
    if top <= 0:
        return "UNRESOLVED", None, [], ranked
    candidates=[s for s,d in ranked if d["score"]==top]
    # 法律研究/文书质量通常作为业务任务的辅助技能。若与唯一业务技能并列，优先业务技能作为 Lead。
    auxiliary={"法律研究与多源资料融合","法律文书质量与格式控制"}
    substantive=[s for s in candidates if s not in auxiliary]
    if len(candidates)>1 and len(substantive)==1:
        return "RESOLVED", substantive[0], candidates, ranked
    if len(candidates)!=1:
        return "UNRESOLVED", None, candidates, ranked
    return "RESOLVED", candidates[0], candidates, ranked


def legacy_route_task_v042(task: str, override: str | None):
    """v0.42-RC6 兼容路由。保持旧任务主技能选择规则，不依赖 v0.43 Router Feature。"""
    if override:
        if override not in SKILLS:
            raise SystemExit(f"未知技能：{override}\n可选：" + "、".join(SKILLS))
        return "USER_OVERRIDE", override, [override], []
    t=norm(task); ranked=score_route(task); strong_business=None
    if any(k in t for k in ["辩护","被害人","控告","报案","立案监督","刑事案件","审查起诉","批捕","取保"]): strong_business="刑事案件办理"
    elif any(k in t for k in ["原告","被告","上诉人","被上诉人"]) and any(k in t for k in ["争议","诉讼","仲裁","起诉","答辩","上诉","执行","保全","案件"]): strong_business="民商事争议解决"
    elif any(k in t for k in ["合同审查","审合同","合同起草","起草合同","合同修改","修改合同","合同谈判","交易文件","协议审查"]): strong_business="合同与交易工作"
    elif any(k in t for k in ["尽职调查","尽调","专项调查"]): strong_business="尽职调查与专项调查"
    elif any(k in t for k in ["法律顾问","专项法律分析","专项意见"]) and not any(k in t for k in ["诉讼","仲裁","原告","被告","刑事","合同审查"]): strong_business="法律顾问与专项法律分析"
    if strong_business: return "RESOLVED", strong_business, [strong_business], ranked
    top=ranked[0][1]["score"] if ranked else 0
    if top<=0: return "UNRESOLVED", None, [], ranked
    candidates=[ss for ss,dd in ranked if dd["score"]==top]
    auxiliary={"法律研究与多源资料融合","法律文书质量与格式控制"}; substantive=[ss for ss in candidates if ss not in auxiliary]
    if len(candidates)>1 and len(substantive)==1: return "RESOLVED", substantive[0], candidates, ranked
    if len(candidates)!=1: return "UNRESOLVED", None, candidates, ranked
    return "RESOLVED", candidates[0], candidates, ranked

def route_task_safe(task: str, override: str | None):
    flags=load_feature_flags()
    if not flags.get("flags",{}).get("skill_router_v2",{}).get("enabled",False):
        r=legacy_route_task_v042(task,override)
        return (*r,{"used_legacy":True,"reason":"SKILL_ROUTER_V2_DISABLED"})
    try:
        r=route_task_v043(task,override)
        return (*r,{"used_legacy":False,"reason":None})
    except Exception as exc:
        r=legacy_route_task_v042(task,override)
        return (*r,{"used_legacy":True,"reason":f"SKILL_ROUTER_V2_ERROR:{type(exc).__name__}"})


RESEARCH_DELIVERABLE_HINTS = ["类案检索报告","类案报告","法律研究备忘录","研究备忘录","法规沿革","裁判趋势","司法趋势","研究报告"]

def build_plan(args):
    manifest=load_json(LOAD_MANIFEST)
    personalization=resolve_personalization(getattr(args,"user_profile",None), getattr(args,"matter_profile",None))
    activation=activation_decision(args.task,getattr(args,"user_profile",None),getattr(args,"matter_profile",None))
    status, lead, candidates, ranked, route_compat=route_task_safe(args.task,args.skill)
    if not args.skill and activation.get("decision") in {"DO_NOT_ACTIVATE","MANUAL_ONLY"} and activation.get("trigger_type") in {"USER_OPT_OUT","SEMANTIC_PROFESSIONAL_LEGAL","BOUNDARY_LEGAL"}:
        status="SKIPPED_BY_ACTIVATION"
        lead=None
        candidates=[]
    t=norm(args.task)
    requires_current_law = bool(args.need_current_law or any(norm(x) in t for x in RESEARCH_HINTS))
    formal_delivery = bool(args.formal_delivery or any(norm(x) in t for x in FORMAL_HINTS))
    structured_review_required = bool(args.structured_review or any(norm(x) in t for x in STRUCTURED_REVIEW_HINTS))
    strategy_choice_required = bool(args.strategy_choice)
    cross_module_required = bool(args.important or structured_review_required or strategy_choice_required or (requires_current_law and lead not in {None,"法律研究与多源资料融合"}))
    working_model_required = bool(cross_module_required or structured_review_required or args.important)
    issue_tree_required = bool(working_model_required or requires_current_law or strategy_choice_required)
    review_question_set_required = bool(structured_review_required)
    authority_map_required = bool(requires_current_law and (args.important or formal_delivery or cross_module_required))
    case_matrix_required = bool(args.need_cases)
    argument_map_required = bool(args.argument_map)
    plan_review_required = bool(args.plan_review)
    behavior_contract_required = bool(args.important or formal_delivery)
    private_knowledge_required = bool(getattr(args, "private_knowledge", False))
    professional_legal_source_required = bool(getattr(args, "professional_legal_source", False))
    need_ocr = bool(getattr(args, "need_ocr", False))
    need_docx = bool(getattr(args, "need_docx", False))
    need_pdf = bool(getattr(args, "need_pdf", False))
    native_track_changes_required = bool(getattr(args, "native_track_changes", False))
    quick_understanding_required = bool(getattr(args, "quick_understanding", False) or (formal_delivery and lead in {"合同与交易工作","刑事案件办理","民商事争议解决","尽职调查与专项调查"}))
    diagram_required = bool(getattr(args, "diagram", False) or (quick_understanding_required and (args.important or formal_delivery) and lead in {"合同与交易工作","刑事案件办理","民商事争议解决","尽职调查与专项调查"}))
    contract_actual_edit_required = bool(lead=="合同与交易工作" and any(k in t for k in ["审查","审阅","审核","修改","修订","优化","改一下","改这份","红线","修订稿","redline"]) and not getattr(args,"contract_report_only",False))
    document_composition_required = bool(formal_delivery and lead in {"法律文书质量与格式控制","刑事案件办理","民商事争议解决","法律顾问与专项法律分析","合同与交易工作","尽职调查与专项调查"})
    rewrite_validation_required = bool(document_composition_required and (args.important or structured_review_required or lead=="法律文书质量与格式控制"))
    deliverable_bundle_required = bool(getattr(args,"bundle",False) or any(norm(x) in t for x in BUNDLE_HINTS))
    bundle_scope_verification_required = bool(deliverable_bundle_required and formal_delivery and any(k in t for k in ["立案","提交","申报","报送","法院","仲裁","申请"]))
    template_resolution_required = bool(getattr(args,"template_required",False) or any(norm(x) in t for x in TEMPLATE_HINTS))
    research_workflow_required = bool(lead=="法律研究与多源资料融合" or requires_current_law or case_matrix_required)
    research_source_evaluation_required = bool(research_workflow_required and (args.important or formal_delivery or lead=="法律研究与多源资料融合"))
    research_saturation_required = bool(research_workflow_required and (args.important or formal_delivery or lead=="法律研究与多源资料融合"))
    research_deliverable_required = bool(formal_delivery and lead=="法律研究与多源资料融合" and any(norm(x) in t for x in RESEARCH_DELIVERABLE_HINTS))
    capability_resolution_required = bool(
        requires_current_law or private_knowledge_required or professional_legal_source_required
        or args.input_gap or need_ocr or need_docx or need_pdf or native_track_changes_required or diagram_required
    )
    context={
        "role": args.role,
        "stage": args.stage,
        "important_task": bool(args.important),
        "formal_delivery": formal_delivery,
        "requires_current_law": requires_current_law,
        "input_capability_gap": bool(args.input_gap),
        "sensitive_material": bool(args.sensitive),
        "structured_review_required": structured_review_required,
        "strategy_choice_required": strategy_choice_required,
        "cross_module_required": cross_module_required,
        "working_model_required": working_model_required,
        "issue_tree_required": issue_tree_required,
        "review_question_set_required": review_question_set_required,
        "authority_map_required": authority_map_required,
        "case_matrix_required": case_matrix_required,
        "argument_map_required": argument_map_required,
        "plan_review_required": plan_review_required,
        "behavior_contract_required": behavior_contract_required,
        "private_knowledge_required": private_knowledge_required,
        "professional_legal_source_required": professional_legal_source_required,
        "need_ocr": need_ocr,
        "need_docx": need_docx,
        "need_pdf": need_pdf,
        "native_track_changes_required": native_track_changes_required,
        "capability_resolution_required": capability_resolution_required,
        "quick_understanding_required":quick_understanding_required,
        "diagram_required":diagram_required,
        "contract_actual_edit_required":contract_actual_edit_required,
        "document_composition_required":document_composition_required,
        "rewrite_validation_required":rewrite_validation_required,
        "deliverable_bundle_required":deliverable_bundle_required,
        "bundle_scope_verification_required":bundle_scope_verification_required,
        "template_resolution_required":template_resolution_required,
        "research_workflow_required":research_workflow_required,
        "research_source_evaluation_required":research_source_evaluation_required,
        "research_saturation_required":research_saturation_required,
        "research_deliverable_required":research_deliverable_required,
        "personalization_profile_loaded": personalization.get("user_profile_loaded"),
        "matter_personalization_loaded": personalization.get("matter_profile_loaded"),
    }
    supporting=[]
    if lead and requires_current_law and lead != "法律研究与多源资料融合": supporting.append("法律研究与多源资料融合")
    if lead and formal_delivery and lead != "法律文书质量与格式控制": supporting.append("法律文书质量与格式控制")
    if args.input_gap and lead != "多模态输入适配（可选）": supporting.append("多模态输入适配（可选）")

    loads=[{"level":"L0","reason":"系统入口、路由与公共分析规范","files":manifest["base_files"]}]
    if cross_module_required:
        loads.append({"level":"L0","reason":"复杂任务跨模块交接与回写","files":[manifest.get("cross_module_execution_file","00_使用与调度/跨模块执行与回写规范.md")]})
    if strategy_choice_required:
        loads.append({"level":"L1","reason":"存在多个行动方案/人工决策节点","files":[manifest.get("strategy_decision_file","00_使用与调度/策略选项与人工决定规范.md")]})
    if working_model_required:
        loads.append({"level":"L1","reason":"复杂任务事项工作模型","files":[manifest.get("matter_working_model_file","00_使用与调度/事项工作模型与分析地图规范.md")]})
    if structured_review_required:
        loads.append({"level":"L1","reason":"任务驱动的结构化审阅问题集","files":[manifest.get("review_question_set_file","00_使用与调度/结构化审阅问题集规范.md")]})
    if authority_map_required or case_matrix_required or research_workflow_required:
        research_files=[manifest.get("authority_case_file","00_使用与调度/法律研究权威图谱与类案矩阵规范.md")]
        if research_source_evaluation_required:
            research_files.append(manifest.get("research_source_evaluation_file","01_运行规范/法律信源能力契约.md"))
        loads.append({"level":"L2","reason":"法律研究的信源评价、权威图谱、类案矩阵与研究充分性","files":list(dict.fromkeys(research_files))})
    if plan_review_required:
        loads.append({"level":"L1","reason":"本次任务需要执行计划确认或修订","files":[manifest.get("plan_review_file","00_使用与调度/复杂任务计划确认与修订规范.md")]})
    if structured_review_required or args.input_gap:
        loads.append({"level":"L3","reason":"输入结果可按需转化为法律对象候选","files":[manifest.get("legal_object_extraction_file","00_使用与调度/法律对象候选提取规范.md")]})
    if structured_review_required:
        loads.append({"level":"L1","reason":"多文件/跨来源结构化审阅","files":[manifest["structured_review_file"]]})
    if capability_resolution_required:
        cap_files=[manifest.get("external_capability_file","01_运行规范/外部能力适配规范.md"),
                   manifest.get("capability_downgrade_file","01_运行规范/能力降级与失败处理规范.md")]
        if requires_current_law or professional_legal_source_required or case_matrix_required:
            cap_files.append(manifest.get("legal_source_contract_file","01_运行规范/法律信源能力契约.md"))
        if private_knowledge_required:
            cap_files.append(manifest.get("private_knowledge_contract_file","01_运行规范/用户知识库能力契约.md"))
        if args.input_gap or need_ocr:
            cap_files.append(manifest.get("file_multimodal_contract_file","01_运行规范/文件与多模态能力契约.md"))
        if need_docx or need_pdf or native_track_changes_required:
            cap_files.append(manifest.get("delivery_tool_contract_file","01_运行规范/交付工具能力契约.md"))
        loads.append({"level":"L1","reason":"本次任务需要外部能力解析与适配","files":list(dict.fromkeys(cap_files))})
    if quick_understanding_required:
        loads.append({"level":"L1","reason":"复杂/正式材料任务快速理解入口","files":[manifest.get("matter_quick_understanding_file","00_使用与调度/事项快速理解与图形化交付规范.md")]})
    if deliverable_bundle_required or template_resolution_required:
        loads.append({"level":"L2","reason":"模板资产/成套交付与共享字段","files":[manifest.get("template_bundle_file","00_使用与调度/模板资产与成套交付规范.md")]})
    if diagram_required:
        loads.append({"level":"L1","reason":"本次任务需要图形化交付","files":[manifest.get("diagram_capability_file","01_运行规范/图形化交付能力契约.md")]})
    if lead:
        info=manifest["skills"][lead]
        loads.append({"level":"L1","reason":"主技能定义","files":info.get("definition",[])})
        loads.append({"level":"L2","reason":"开始实体工作与分析推理","files":info.get("workflow",[])})
        if lead == "刑事案件办理" and _contains_any(args.role,["被害人","控告","报案"]):
            loads.append({"level":"L2","reason":"刑事被害人/控告独立分支","files":info.get("role_modules",{}).get("被害人/控告",[])})
        # checklist source is loaded on demand; dynamic checklist itself can be generated from registry
        if args.full_checklist:
            loads.append({"level":"L3","reason":"需要完整人工检查清单","files":info.get("checklist",[])})
        for s in supporting:
            sinfo=manifest["skills"][s]
            files=sinfo.get("definition",[])+sinfo.get("workflow",[])
            loads.append({"level":"L3","reason":f"辅助技能：{s}","files":files})
        if args.important or formal_delivery:
            files=list(manifest.get("final_gate_files",[]))
            if args.important: files += info.get("adversarial",[])
            loads.append({"level":"L4","reason":"重要任务/正式交付门","files":files})
    plan={
        "schema_version":"0.2","generated_at":datetime.now(timezone.utc).isoformat(),
        "task":args.task,"activation":activation,"route_status":status,"lead_skill":lead,
        "legacy_compatibility":{"policy":"ENHANCEMENT_ONLY_WITH_LEGACY_FALLBACK","feature_flags":load_feature_flags(),"activation_fallback":activation.get("legacy_fallback",{}),"route_fallback":route_compat,"fallback_records":[]},
        "route_candidates":candidates,"route_debug":ranked,"supporting_skills":supporting,
        "context":context,"load_plan":loads,
        "personalization":personalization,
        "notes":["路由分值仅用于工程辅助，不代表法律概率或模型置信度。"]
    }
    return plan


def _contains_any(text, keywords):
    text=norm(text)
    return bool(text) and any(norm(k) in text for k in (keywords or []))

def condition_matches(rule, plan):
    context=plan.get("context",{})
    if rule.get("skill") and plan.get("lead_skill") != rule.get("skill"):
        return False
    if not all(context.get(k) == v for k,v in rule.get("when",{}).items()):
        return False
    if rule.get("role_keywords") and not _contains_any(context.get("role"), rule.get("role_keywords")):
        return False
    if rule.get("stage_keywords") and not _contains_any(context.get("stage"), rule.get("stage_keywords")):
        return False
    if rule.get("task_keywords") and not _contains_any(plan.get("task"), rule.get("task_keywords")):
        return False
    return True


def build_checklist(plan):
    registry=load_json(CHECKLIST_REGISTRY)
    items=[]
    def add(item, source):
        items.append({"id":item["id"],"text":item["text"],"critical":bool(item.get("critical")),"source":source,"status":"PENDING","note":None})
    for x in registry["common"]: add(x,"公共")
    lead=plan.get("lead_skill")
    if lead:
        for x in registry["skills"].get(lead,[]): add(x,lead)
    for x in registry.get("conditional",[]):
        if condition_matches(x,plan): add(x,"条件触发")
    return {"schema_version":"0.1","task":plan.get("task"),"lead_skill":lead,"context":plan.get("context",{}),"items":items}


def checklist_markdown(checklist):
    lines=["# 爽律 Skill｜本次动态检查清单","",f"**主技能：** {checklist.get('lead_skill') or '尚未确定'}",f"**任务：** {checklist.get('task') or ''}",""]
    current=None
    for item in checklist["items"]:
        if item["source"]!=current:
            current=item["source"]
            lines += [f"## {current}",""]
        mark="[ ]"
        star=" **[关键]**" if item.get("critical") else ""
        lines.append(f"- {mark} `{item['id']}` {item['text']}{star}")
    lines += ["","状态建议：`PENDING` / `PASS` / `FAIL` / `N/A`。"]
    return "\n".join(lines)+"\n"


def build_state_template(plan):
    ck=build_checklist(plan)
    context=plan.get("context",{})
    return {
        "schema_version":"0.6",
        "task":plan.get("task"),
        "lead_skill":plan.get("lead_skill"),
        "activation":plan.get("activation",{}),
        "legacy_compatibility":plan.get("legacy_compatibility",{"policy":"ENHANCEMENT_ONLY_WITH_LEGACY_FALLBACK","fallback_records":[]}),
        "context":{
            "role":context.get("role"),
            "stage":context.get("stage"),
            "important_task":bool(context.get("important_task")),
            "formal_delivery":bool(context.get("formal_delivery")),
            "requires_current_law":bool(context.get("requires_current_law")),
            "sensitive_material":bool(context.get("sensitive_material")),
            "input_capability_gap":bool(context.get("input_capability_gap")),
            "structured_review_required":bool(context.get("structured_review_required")),
            "strategy_choice_required":bool(context.get("strategy_choice_required")),
            "cross_module_required":bool(context.get("cross_module_required")),
            "working_model_required":bool(context.get("working_model_required")),
            "issue_tree_required":bool(context.get("issue_tree_required")),
            "review_question_set_required":bool(context.get("review_question_set_required")),
            "authority_map_required":bool(context.get("authority_map_required")),
            "case_matrix_required":bool(context.get("case_matrix_required")),
            "argument_map_required":bool(context.get("argument_map_required")),
            "plan_review_required":bool(context.get("plan_review_required")),
            "behavior_contract_required":bool(context.get("behavior_contract_required")),
            "private_knowledge_required":bool(context.get("private_knowledge_required")),
            "professional_legal_source_required":bool(context.get("professional_legal_source_required")),
            "need_ocr":bool(context.get("need_ocr")),
            "need_docx":bool(context.get("need_docx")),
            "need_pdf":bool(context.get("need_pdf")),
            "native_track_changes_required":bool(context.get("native_track_changes_required")),
            "capability_resolution_required":bool(context.get("capability_resolution_required")),
            "quick_understanding_required":bool(context.get("quick_understanding_required")),
            "diagram_required":bool(context.get("diagram_required")),
            "contract_actual_edit_required":bool(context.get("contract_actual_edit_required")),
            "document_composition_required":bool(context.get("document_composition_required")),
            "rewrite_validation_required":bool(context.get("rewrite_validation_required")),
            "deliverable_bundle_required":bool(context.get("deliverable_bundle_required")),
            "bundle_scope_verification_required":bool(context.get("bundle_scope_verification_required")),
            "template_resolution_required":bool(context.get("template_resolution_required")),
            "research_workflow_required":bool(context.get("research_workflow_required")),
            "research_source_evaluation_required":bool(context.get("research_source_evaluation_required")),
            "research_saturation_required":bool(context.get("research_saturation_required")),
            "research_deliverable_required":bool(context.get("research_deliverable_required")),
        },
        "checklist":[{"id":i["id"],"status":"PENDING","note":None} for i in ck["items"]],
        "analysis_work":{"required":bool(context.get("important_task")),"status":"PENDING" if context.get("important_task") else "NOT_REQUIRED","argument_record_count":0},
        "structured_review":{"required":bool(context.get("structured_review_required")),"performed":False,"record_count":0,"format":None},
        "cross_module_execution":{
            "required":bool(context.get("cross_module_required")),
            "status":"PENDING" if context.get("cross_module_required") else "NOT_REQUIRED",
            "research_request_count":0,"research_result_count":0,
            "option_count":0,"decision_count":0,"open_human_decision_count":0,
            "adversarial_review_record_count":0,
            "adversarial_writeback_status":"PENDING" if context.get("important_task") else "NOT_REQUIRED",
            "writeback_event_count":0,"open_writeback_count":0,
            "chain_report_path":None
        },
        "working_model":{
            "required":bool(context.get("working_model_required")),
            "status":"PENDING" if context.get("working_model_required") else "NOT_REQUIRED",
            "matter_model_count":0,"task_profile_count":0,"issue_tree_count":0,
            "review_question_set_count":0,"authority_map_count":0,"case_matrix_count":0,"argument_map_count":0,
            "legal_object_candidate_count":0,
            "plan_review_status":"PENDING" if context.get("plan_review_required") else "NOT_REQUIRED",
            "behavior_contract_status":"PENDING" if context.get("behavior_contract_required") else "NOT_REQUIRED",
            "critical_behavior_violation_count":0,"model_check_report_path":None
        },
        "strategy_analysis":{
            "required":bool(context.get("strategy_choice_required")),
            "status":"PENDING" if context.get("strategy_choice_required") else "NOT_REQUIRED",
            "option_count":0,"decision_record_count":0
        },
        "capability_resolution":{
            "required":bool(context.get("capability_resolution_required")),
            "status":"PENDING" if context.get("capability_resolution_required") else "NOT_REQUIRED",
            "required_count":0,"resolved_count":0,
            "blocked_requirements":[],"downgraded_requirements":[],"report_path":None
        },
        "traceability":{
            "required":bool(context.get("important_task") or context.get("formal_delivery")),
            "status":"PENDING" if (context.get("important_task") or context.get("formal_delivery")) else "NOT_REQUIRED",
            "critical_claim_count":0,"fully_traced_claim_count":0,"untraced_claim_ids":[],
            "inferred_fact_count":0,"inferred_fact_with_basis_count":0,
            "verified_legal_rule_count":0,"verified_legal_rule_with_pinpoint_count":0,
            "deliverable_claim_count":0,"deliverable_claim_with_upstream_links_count":0,
            "substantive_claims_present":False,"trace_report_path":None
        },
        "adversarial_review":{"required":bool(context.get("important_task")),"status":"PENDING" if context.get("important_task") else "NOT_REQUIRED"},
        "current_law_check":{"required":bool(context.get("requires_current_law")),"performed":False,"sources":[]},
        "external_processing":{"used":False,"provider":None,"explicit_consent":False},
        "escalations":[],
        "output":{"output_contract_checked":False,"claimed_capabilities":[]},
        "research":{
            "state":"INCOMPLETE" if context.get("research_workflow_required") else "NOT_REQUIRED",
            "unqualified_conclusion":False,
            "source_evaluation_required":bool(context.get("research_source_evaluation_required")),
            "key_source_count":0,
            "evaluated_key_source_count":0,
            "channel_based_rank_violation_count":0,
            "saturation_required":bool(context.get("research_saturation_required")),
            "saturation_assessment_count":0,
            "deliverable_profile_required":bool(context.get("research_deliverable_required")),
            "deliverable_profile_count":0,
            "user_template_required":bool(context.get("research_deliverable_required") and context.get("template_resolution_required")),
            "user_template_preserved":True
        },
        "quick_understanding":{"required":bool(context.get("quick_understanding_required")),"snapshot_status":"PENDING" if context.get("quick_understanding_required") else "NOT_REQUIRED","snapshot_count":0,"diagram_required":bool(context.get("diagram_required")),"diagram_spec_count":0,"rendered_diagram_count":0,"rendering_state":"PENDING" if context.get("diagram_required") else "NOT_REQUIRED"},
        "contract_delivery":{"actual_edit_required":bool(context.get("contract_actual_edit_required")),"actual_modified_contract_count":0,"report_only":False,"downgrade_disclosed":False},
        "document_composition":{"required":bool(context.get("document_composition_required")),"composition_plan_count":0,"plan_status":"PENDING" if context.get("document_composition_required") else "NOT_REQUIRED","exempted":False,"exemption_reason":None,"draft_defect_count":0,"major_or_blocking_open_defect_count":0,"rewrite_decision_count":0,"rewrite_decision_applied_count":0},
        "template_resolution":{"required":bool(context.get("template_resolution_required")),"requested_or_applicable_template_count":1 if context.get("template_resolution_required") else 0,"resolved_template_count":0,"missing_template_ids":[],"conflict_count":0,"preserved_user_asset_count":0,"silently_overridden_user_asset_count":0},
        "deliverable_bundle":{"required":bool(context.get("deliverable_bundle_required")),"bundle_count":0,"scope_status":"UNKNOWN_NEEDS_CHECK" if context.get("bundle_scope_verification_required") else "NOT_REQUIRED","required_deliverable_count":0,"ready_required_deliverable_count":0,"stale_deliverable_count":0,"open_propagation_count":0},
        "materials":[],
    }

def validate_state(state):
    blockers=[]; warnings=[]; passed=[]
    act=state.get("activation",{}) or {}
    if (act.get("activation_mode")=="MANUAL" and act.get("decision")=="AUTO_ACTIVATE") or (act.get("trigger_type")=="USER_OPT_OUT" and act.get("decision")!="DO_NOT_ACTIVATE"):
        blockers.append({"id":"GATE-ACTIVATION-PREFERENCE","message":"自动激活与用户MANUAL/明确禁用偏好冲突。"})
    else:
        passed.append("GATE-ACTIVATION-PREFERENCE")
    compat=state.get("legacy_compatibility",{}) or {}
    compat_blocked=False
    for rec in compat.get("fallback_records",[]) or []:
        if rec.get("fallback_status")=="BLOCKED" or (rec.get("task_continuation") is False and rec.get("user_impact")!="LOSS_OF_ENHANCEMENT_ONLY"):
            blockers.append({"id":"GATE-LEGACY-COMPAT","message":f"增强功能 {rec.get('feature','')} 失败后未能回退旧路径，核心任务受到阻断。"}); compat_blocked=True
        elif rec.get("fallback_status")=="DOWNGRADED":
            warnings.append({"id":"WARN-DOWNGRADE","message":f"增强功能 {rec.get('feature','')} 失败后已回退，但存在已披露能力降级。"})
    if not compat_blocked:
        passed.append("GATE-LEGACY-COMPAT")
    lead=state.get("lead_skill")
    if not lead or lead not in SKILLS: blockers.append({"id":"GATE-LEAD","message":"未确定唯一有效主技能。"})
    else: passed.append("GATE-LEAD")
    context=state.get("context",{})
    law=state.get("current_law_check",{})
    if context.get("requires_current_law") and not law.get("performed"):
        blockers.append({"id":"GATE-LAW","message":"本次要求现行法核验，但尚未记录实际完成。"})
    else: passed.append("GATE-LAW")
    analysis=state.get("analysis_work",{})
    if context.get("important_task") and analysis.get("status")!="COMPLETE":
        blockers.append({"id":"GATE-ANALYSIS","message":"重要任务的分析与推理工作尚未完成或未记录。"})
    else: passed.append("GATE-ANALYSIS")
    sr=state.get("structured_review",{})
    if context.get("structured_review_required") and (not sr.get("performed") or int(sr.get("record_count") or 0) <= 0):
        blockers.append({"id":"GATE-STRUCT","message":"本次需要结构化审阅，但尚未记录实际完成的结构化审阅成果。"})
    else: passed.append("GATE-STRUCT")
    wm=state.get("working_model",{})
    if context.get("working_model_required") and (wm.get("status")!="COMPLETE" or int(wm.get("matter_model_count") or 0)<=0):
        blockers.append({"id":"GATE-MODEL","message":"复杂/跨模块任务尚未形成并更新事项工作模型。"})
    else: passed.append("GATE-MODEL")
    if context.get("working_model_required") and int(wm.get("task_profile_count") or 0)<=0:
        blockers.append({"id":"GATE-PROFILE","message":"需要事项工作模型，但尚未形成最小 TaskProfile。"})
    else: passed.append("GATE-PROFILE")
    if context.get("issue_tree_required") and int(wm.get("issue_tree_count") or 0)<=0:
        blockers.append({"id":"GATE-ISSUETREE","message":"本次复杂分析尚未形成问题树/等价问题结构。"})
    else: passed.append("GATE-ISSUETREE")
    if context.get("review_question_set_required") and int(wm.get("review_question_set_count") or 0)<=0:
        blockers.append({"id":"GATE-REVIEWQ","message":"结构化审阅尚未形成任务驱动的审阅问题集。"})
    else: passed.append("GATE-REVIEWQ")
    if context.get("authority_map_required") and int(wm.get("authority_map_count") or 0)<=0:
        blockers.append({"id":"GATE-AUTHMAP","message":"重要现行法研究尚未形成权威来源结构。"})
    else: passed.append("GATE-AUTHMAP")
    if context.get("case_matrix_required") and int(wm.get("case_matrix_count") or 0)<=0:
        blockers.append({"id":"GATE-CASEMATRIX","message":"本次明确需要类案研究，但尚未形成类案比较矩阵。"})
    else: passed.append("GATE-CASEMATRIX")
    if context.get("plan_review_required") and wm.get("plan_review_status") not in {"APPROVED","APPROVED_WITH_CHANGES","REVISED"}:
        blockers.append({"id":"GATE-PLANREV","message":"本次需要计划确认/修订，但计划尚未达到可执行状态。"})
    else: passed.append("GATE-PLANREV")
    if context.get("behavior_contract_required") and (wm.get("behavior_contract_status") not in {"PASS","PASS_WITH_NOTES"} or int(wm.get("critical_behavior_violation_count") or 0)>0):
        blockers.append({"id":"GATE-BEHAVIOR","message":"重要/正式任务仍存在未修正的关键行为契约问题。"})
    else: passed.append("GATE-BEHAVIOR")
    cm=state.get("cross_module_execution",{})
    if context.get("cross_module_required") and cm.get("status")!="COMPLETE":
        blockers.append({"id":"GATE-CROSS","message":"本次需要跨模块执行，但交接/回写状态尚未完成。"})
    else: passed.append("GATE-CROSS")
    if context.get("requires_current_law") and lead != "法律研究与多源资料融合":
        if int(cm.get("research_request_count") or 0) <= 0 or int(cm.get("research_result_count") or 0) <= 0:
            blockers.append({"id":"GATE-HANDOFF","message":"业务技能需要法律研究，但未记录 ResearchRequest → ResearchResult 的完整交接。"})
        else: passed.append("GATE-HANDOFF")
    else: passed.append("GATE-HANDOFF")
    if int(cm.get("open_writeback_count") or 0) > 0:
        blockers.append({"id":"GATE-WRITEBACK","message":"存在尚未应用的回写事件，旧分析不得直接进入最终交付。"})
    else: passed.append("GATE-WRITEBACK")
    if context.get("important_task"):
        if cm.get("adversarial_review_record_count",0) <= 0 or cm.get("adversarial_writeback_status") not in {"COMPLETE_REVISED","COMPLETE_UNCHANGED_WITH_REASON"}:
            blockers.append({"id":"GATE-ADV-WRITEBACK","message":"重要任务的对抗性审查尚未形成有效回写，或未说明维持原结论的理由。"})
        else: passed.append("GATE-ADV-WRITEBACK")
    else: passed.append("GATE-ADV-WRITEBACK")
    sa=state.get("strategy_analysis",{})
    if context.get("strategy_choice_required"):
        if sa.get("status")!="COMPLETE" or int(sa.get("option_count") or 0) <= 0:
            blockers.append({"id":"GATE-OPTION","message":"本次存在策略选择，但尚未完成结构化选项比较。"})
        elif int(cm.get("open_human_decision_count") or 0) > 0:
            blockers.append({"id":"GATE-OPTION","message":"存在尚未解决的人工策略决定节点。"})
        else: passed.append("GATE-OPTION")
    else: passed.append("GATE-OPTION")
    tr=state.get("traceability",{})
    trace_required=bool(context.get("important_task") or context.get("formal_delivery"))
    if trace_required and tr.get("status")!="COMPLETE":
        blockers.append({"id":"GATE-PROV","message":"重要任务/正式交付的全链路溯源尚未完成或未记录。"})
    elif int(tr.get("critical_claim_count") or 0) > int(tr.get("fully_traced_claim_count") or 0):
        blockers.append({"id":"GATE-PROV","message":"存在核心结论未形成完整上游溯源链。"})
    else: passed.append("GATE-PROV")
    if int(tr.get("inferred_fact_count") or 0) > int(tr.get("inferred_fact_with_basis_count") or 0):
        blockers.append({"id":"GATE-INFER","message":"存在 INFERRED 事实未记录推断依据。"})
    else: passed.append("GATE-INFER")
    if int(tr.get("verified_legal_rule_count") or 0) > int(tr.get("verified_legal_rule_with_pinpoint_count") or 0):
        blockers.append({"id":"GATE-RULESRC","message":"存在已核验法律规则缺少权威来源、精确定位或核验记录。"})
    else: passed.append("GATE-RULESRC")
    if context.get("formal_delivery") and tr.get("substantive_claims_present"):
        if int(tr.get("deliverable_claim_count") or 0)<=0 or int(tr.get("deliverable_claim_count") or 0) > int(tr.get("deliverable_claim_with_upstream_links_count") or 0):
            blockers.append({"id":"GATE-CLAIM","message":"正式交付中的重要命题尚未全部关联上游分析对象。"})
        else: passed.append("GATE-CLAIM")
    else: passed.append("GATE-CLAIM")
    qu=state.get("quick_understanding",{})
    if context.get("quick_understanding_required") and (qu.get("snapshot_status") not in {"COMPLETE","FINAL"} or int(qu.get("snapshot_count") or 0)<=0):
        blockers.append({"id":"GATE-SNAPSHOT","message":"复杂/正式材料任务尚未形成事项核心概要。"})
    else: passed.append("GATE-SNAPSHOT")
    if context.get("diagram_required"):
        if int(qu.get("diagram_spec_count") or 0)<=0:
            blockers.append({"id":"GATE-DIAGRAM","message":"本次要求图形化表达，但尚未形成 DiagramSpec。"})
        elif qu.get("rendering_state") not in {"RENDERED_PNG","RENDERED_HTML","DOWNGRADED_TEXT_SOURCE"}:
            blockers.append({"id":"GATE-DIAGRAM","message":"DiagramSpec 已形成，但尚未实际渲染或记录可接受降级。"})
        else: passed.append("GATE-DIAGRAM")
    else: passed.append("GATE-DIAGRAM")
    cd=state.get("contract_delivery",{})
    if context.get("contract_actual_edit_required") and int(cd.get("actual_modified_contract_count") or 0)<=0:
        blockers.append({"id":"GATE-CONTRACT-EDIT","message":"合同 REVIEW/REVISE 需要实际修改合同文本，不能只交修改报告。"})
    else: passed.append("GATE-CONTRACT-EDIT")
    dc=state.get("document_composition",{})
    if context.get("document_composition_required"):
        if dc.get("exempted"):
            if not dc.get("exemption_reason"):
                blockers.append({"id":"GATE-COMPOSITION","message":"成文策略被标记豁免，但未记录豁免理由。"})
            else: passed.append("GATE-COMPOSITION")
        elif dc.get("plan_status") not in {"CONFIRMED","REVISED","FINAL"} or int(dc.get("composition_plan_count") or 0)<=0:
            blockers.append({"id":"GATE-COMPOSITION","message":"复杂/正式法律文书尚未形成可用的 DocumentCompositionPlan。"})
        else: passed.append("GATE-COMPOSITION")
    else: passed.append("GATE-COMPOSITION")
    if context.get("rewrite_validation_required"):
        if int(dc.get("major_or_blocking_open_defect_count") or 0)>0:
            blockers.append({"id":"GATE-REWRITE","message":"仍存在未解决的 MAJOR/BLOCKING 成文缺陷，不得最终交付。"})
        elif int(dc.get("rewrite_decision_applied_count") or 0)<=0:
            blockers.append({"id":"GATE-REWRITE","message":"本次要求结构性重写，但尚未记录已应用 RewriteDecision。"})
        else: passed.append("GATE-REWRITE")
    else: passed.append("GATE-REWRITE")
    tres=state.get("template_resolution",{})
    if int(tres.get("silently_overridden_user_asset_count") or 0)>0:
        blockers.append({"id":"GATE-USER-ASSET-PRESERVE","message":"检测到用户模板被系统/导入过程静默覆盖；必须恢复用户资产或取得用户明确选择。"})
    else: passed.append("GATE-USER-ASSET-PRESERVE")
    if context.get("template_resolution_required"):
        if int(tres.get("requested_or_applicable_template_count") or 0)<=0 or int(tres.get("missing_template_ids") and len(tres.get("missing_template_ids")) or 0)>0 or int(tres.get("resolved_template_count") or 0)<int(tres.get("requested_or_applicable_template_count") or 0):
            blockers.append({"id":"GATE-TEMPLATE-RESOLUTION","message":"用户明确指定/适用模板尚未全部解析；不得静默换成系统默认模板。"})
        else: passed.append("GATE-TEMPLATE-RESOLUTION")
    else: passed.append("GATE-TEMPLATE-RESOLUTION")
    db=state.get("deliverable_bundle",{})
    if context.get("deliverable_bundle_required"):
        if int(db.get("bundle_count") or 0)<=0:
            blockers.append({"id":"GATE-BUNDLE","message":"本次要求成套交付，但尚未建立 DeliverableBundle。"})
        elif int(db.get("ready_required_deliverable_count") or 0)<int(db.get("required_deliverable_count") or 0):
            blockers.append({"id":"GATE-BUNDLE","message":"用户明确要求或已核验必需的交付物尚未全部达到 READY/DELIVERED。"})
        elif context.get("bundle_scope_verification_required") and db.get("scope_status") not in {"VERIFIED","USER_DEFINED"}:
            blockers.append({"id":"GATE-BUNDLE","message":"正式提交型成套任务尚未核验必需材料范围；不能用通用经验清单冒充当前机构要求。"})
        else: passed.append("GATE-BUNDLE")
        if int(db.get("stale_deliverable_count") or 0)>0 or int(db.get("open_propagation_count") or 0)>0:
            blockers.append({"id":"GATE-BUNDLE-CONSISTENCY","message":"共享字段变更后仍有 STALE 交付物或未关闭的变更传播事件。"})
        else: passed.append("GATE-BUNDLE-CONSISTENCY")
    else:
        passed += ["GATE-BUNDLE","GATE-BUNDLE-CONSISTENCY"]
    adv=state.get("adversarial_review",{})
    if context.get("important_task") and adv.get("status")!="COMPLETE":
        blockers.append({"id":"GATE-ADV","message":"重要任务的对抗性审查尚未完成。"})
    else: passed.append("GATE-ADV")
    for e in state.get("escalations",[]):
        if e.get("level") in {"C","D"} and e.get("status")=="OPEN":
            blockers.append({"id":"GATE-ESC","message":f"存在未解决的 {e.get('level')} 级人工升级事项。"})
    if not any(b["id"]=="GATE-ESC" for b in blockers): passed.append("GATE-ESC")
    capres=state.get("capability_resolution",{})
    if context.get("capability_resolution_required"):
        if capres.get("status") not in {"COMPLETE","DOWNGRADED"}:
            blockers.append({"id":"GATE-CAPRES","message":"本次任务依赖外部/运行能力，但尚未完成能力解析。"})
        elif int(capres.get("resolved_count") or 0) < int(capres.get("required_count") or 0):
            blockers.append({"id":"GATE-CAPRES","message":"存在尚未满足的必需能力要求。"})
        elif capres.get("blocked_requirements"):
            blockers.append({"id":"GATE-CAPRES","message":"能力解析仍存在 BLOCKED 要求。"})
        else:
            passed.append("GATE-CAPRES")
    else:
        passed.append("GATE-CAPRES")
    ext=state.get("external_processing",{})
    if context.get("sensitive_material") and ext.get("used") and not ext.get("explicit_consent"):
        blockers.append({"id":"GATE-EXT","message":"敏感材料已使用外部处理，但没有明确授权。"})
    else: passed.append("GATE-EXT")
    output=state.get("output",{})
    if context.get("formal_delivery") and not output.get("output_contract_checked"):
        blockers.append({"id":"GATE-OUT","message":"正式交付尚未完成输出契约检查。"})
    else: passed.append("GATE-OUT")
    research=state.get("research",{})
    if research.get("state") in {"INCOMPLETE","BLOCKED","HUMAN_REVIEW_REQUIRED"} and research.get("unqualified_conclusion"):
        blockers.append({"id":"GATE-RES","message":"研究未达到无保留结论条件，但当前仍标记准备给出无保留结论。"})
    else: passed.append("GATE-RES")
    if research.get("source_evaluation_required"):
        if int(research.get("channel_based_rank_violation_count") or 0)>0:
            blockers.append({"id":"GATE-SOURCE-EVAL","message":"存在仅凭数据库/官网/公众号/网页渠道直接决定来源等级的记录。"})
        elif int(research.get("key_source_count") or 0)>int(research.get("evaluated_key_source_count") or 0):
            blockers.append({"id":"GATE-SOURCE-EVAL","message":"存在关键研究来源尚未完成 SourceProfile/SourceCard 评价。"})
        else: passed.append("GATE-SOURCE-EVAL")
    else: passed.append("GATE-SOURCE-EVAL")
    if research.get("saturation_required"):
        if research.get("state")=="SATURATED" and int(research.get("saturation_assessment_count") or 0)<=0:
            blockers.append({"id":"GATE-RESEARCH-SATURATION","message":"研究声称 SATURATED，但没有 ResearchSaturationAssessment 或等价充分性记录。"})
        else: passed.append("GATE-RESEARCH-SATURATION")
    else: passed.append("GATE-RESEARCH-SATURATION")
    if research.get("deliverable_profile_required"):
        if int(research.get("deliverable_profile_count") or 0)<=0:
            blockers.append({"id":"GATE-RESEARCH-DELIVERABLE","message":"正式研究交付尚未确定 ResearchDeliverableProfile。"})
        elif research.get("user_template_required") and not research.get("user_template_preserved"):
            blockers.append({"id":"GATE-RESEARCH-DELIVERABLE","message":"研究交付存在用户/事项模板，但系统默认模板覆盖了用户资产。"})
        else: passed.append("GATE-RESEARCH-DELIVERABLE")
    else: passed.append("GATE-RESEARCH-DELIVERABLE")
    # material review integrity
    for m in state.get("materials",[]):
        if m.get("critical") and m.get("status")=="REVIEWED" and not (m.get("review_scope") or m.get("locator")):
            blockers.append({"id":"GATE-REVIEW","message":f"关键材料“{m.get('name','')}”标记 REVIEWED，但没有审阅范围或来源定位。"})
        elif m.get("status")=="REVIEWED" and not m.get("locator"):
            warnings.append({"id":"WARN-LOC","message":f"材料“{m.get('name','')}”已审阅，但来源定位不完整。"})
    if not any(b["id"]=="GATE-REVIEW" for b in blockers): passed.append("GATE-REVIEW")
    # capability truthfulness
    for c in output.get("claimed_capabilities",[]):
        if c.get("claimed_as_delivered") and c.get("status") not in {"VERIFIED_SUPPORTED","DOWNGRADED"}:
            blockers.append({"id":"GATE-CAP","message":f"能力“{c.get('name','')}”被声称已交付，但状态为 {c.get('status')}。"})
        elif c.get("status")=="DOWNGRADED":
            warnings.append({"id":"WARN-DOWNGRADE","message":f"能力“{c.get('name','')}”采用降级实现。"})
    if not any(b["id"]=="GATE-CAP" for b in blockers): passed.append("GATE-CAP")
    # 动态清单完整性：关键项缺失、PENDING 或 FAIL 均阻断；非关键未决仅警告。
    registry=load_json(CHECKLIST_REGISTRY)
    pseudo_plan={"lead_skill":lead,"task":state.get("task",""),"context":context}
    expected=[]
    expected += registry.get("common",[])
    expected += registry.get("skills",{}).get(lead,[]) if lead else []
    expected += [x for x in registry.get("conditional",[]) if condition_matches(x,pseudo_plan)]
    expected_by_id={x["id"]:x for x in expected}
    actual={x.get("id"):x for x in state.get("checklist",[]) if x.get("id")}
    for item_id, spec in expected_by_id.items():
        act=actual.get(item_id)
        if not act:
            msg=f"应有检查项 {item_id} 未出现在执行状态中。"
            (blockers if spec.get("critical") else warnings).append({"id":"CHECKLIST-MISSING","message":msg})
            continue
        st=act.get("status")
        if st in {"PENDING","FAIL"}:
            msg=f"检查项 {item_id} 状态为 {st}。"
            (blockers if spec.get("critical") else warnings).append({"id":"CHECKLIST-NOT-PASS","message":msg})
    for item_id, act in actual.items():
        if item_id not in expected_by_id and act.get("status") in {"PENDING","FAIL"}:
            warnings.append({"id":"CHECKLIST-EXTRA","message":f"额外检查项 {item_id} 状态为 {act.get('status')}。"})
    status="BLOCKED" if blockers else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {"gate_status":status,"blockers":blockers,"warnings":warnings,"passed_rules":passed,"disclaimer":"机器门控只检查执行记录是否满足规则，不替代律师对实体结论的专业复核。"}



def trace_check(bundle):
    """检查溯源包中的 ID 关联和最低溯源要求。只检查结构完整性，不判断法律观点正确性。"""
    blockers=[]; warnings=[]
    def index(items, key):
        out={}
        for x in items or []:
            if isinstance(x,dict) and x.get(key): out[x[key]]=x
        return out
    loc=index(bundle.get("source_locators",[]),"locator_id")
    # 兼容旧定位对象只带 source_id 的情况：不能作为稳定 locator id，但给予警告而非静默通过
    sources=index(bundle.get("sources",[]),"source_id")
    facts=index(bundle.get("facts",[]),"fact_id")
    evidence=index(bundle.get("evidence_items",[]),"evidence_id")
    issues=index(bundle.get("issues",[]),"issue_id")
    rules=index(bundle.get("legal_rules",[]),"rule_id")
    cases=index(bundle.get("case_cards",[]),"case_id")
    arguments=index(bundle.get("arguments",[]),"argument_id")
    findings=index(bundle.get("findings",[]),"finding_id")
    claims=index(bundle.get("deliverable_claims",[]),"claim_id")

    def refs_exist(owner, field, refs, registry, regname, required=False):
        refs=refs or []
        if required and not refs:
            blockers.append({"id":"TRACE-MISSING","message":f"{owner} 缺少 {field}。"})
        for r in refs:
            if r not in registry:
                blockers.append({"id":"TRACE-BROKEN","message":f"{owner}.{field} 引用了不存在的 {regname}: {r}"})

    for sid,src in sources.items():
        if src.get("verification_state")=="VERIFIED" and src.get("source_family") in {"LEGAL_AUTHORITY","CASE"}:
            refs=[x for x in (src.get("locators") or []) if isinstance(x,str)]
            if not refs and not any(isinstance(x,dict) and x.get("locator_value") for x in (src.get("locators") or [])):
                blockers.append({"id":"TRACE-SOURCE-LOC","message":f"已核验来源 {sid} 缺少精确定位。"})
            refs_exist(f"SourceCard {sid}","locators",refs,loc,"SourceLocator",False)

    for eid,e in evidence.items():
        if e.get("source_ref") not in sources:
            blockers.append({"id":"TRACE-EVIDENCE-SOURCE","message":f"EvidenceItem {eid} 的 source_ref 无法回到 SourceCard。"})
        if e.get("review_state")=="REVIEWED":
            refs_exist(f"EvidenceItem {eid}","source_locator_refs",e.get("source_locator_refs"),loc,"SourceLocator",True)
        refs_exist(f"EvidenceItem {eid}","supports_fact_ids",e.get("supports_fact_ids"),facts,"FactRecord",False)
        refs_exist(f"EvidenceItem {eid}","contradicts_fact_ids",e.get("contradicts_fact_ids"),facts,"FactRecord",False)

    for fid,f in facts.items():
        st=f.get("fact_status")
        if st in {"VERIFIED","INFERRED"}:
            refs_exist(f"FactRecord {fid}","source_refs",f.get("source_refs"),sources,"SourceCard",True)
        if st=="INFERRED" and not (f.get("inference_basis") or []):
            blockers.append({"id":"TRACE-INFER","message":f"INFERRED 事实 {fid} 缺少 inference_basis。"})
        refs_exist(f"FactRecord {fid}","supporting_evidence_ids",f.get("supporting_evidence_ids"),evidence,"EvidenceItem",False)

    for rid,r in rules.items():
        if r.get("rule_type")=="LEGAL" and r.get("verification_state") in {"VERIFIED_CURRENT","VERIFIED_HISTORICAL"}:
            refs_exist(f"LegalRule {rid}","source_refs",r.get("source_refs"),sources,"SourceCard",True)
            refs_exist(f"LegalRule {rid}","pinpoint_refs",r.get("pinpoint_refs"),loc,"SourceLocator",True)
            if r.get("verification_state")=="VERIFIED_CURRENT" and not r.get("last_verified_at"):
                blockers.append({"id":"TRACE-RULE-DATE","message":f"LegalRule {rid} 标记 VERIFIED_CURRENT 但没有 last_verified_at。"})

    for cid,c in cases.items():
        if c.get("source_id") not in sources:
            blockers.append({"id":"TRACE-CASE-SOURCE","message":f"CaseCard {cid} 的 source_id 无法回到 SourceCard。"})
        if c.get("verification_state")=="VERIFIED":
            refs_exist(f"CaseCard {cid}","source_locator_refs",c.get("source_locator_refs"),loc,"SourceLocator",True)
            refs_exist(f"CaseCard {cid}","holding_locator_refs",c.get("holding_locator_refs"),loc,"SourceLocator",True)
        for iid in c.get("legal_issue_ids") or []:
            if iid not in issues: blockers.append({"id":"TRACE-BROKEN","message":f"CaseCard {cid} 引用了不存在的 IssueRecord: {iid}"})

    for aid,a in arguments.items():
        if a.get("issue_id") not in issues:
            blockers.append({"id":"TRACE-ARG-ISSUE","message":f"ArgumentRecord {aid} 的 issue_id 无法回到 IssueRecord。"})
        refs_exist(f"ArgumentRecord {aid}","rule_refs",a.get("rule_refs"),rules,"LegalRule",False)
        refs_exist(f"ArgumentRecord {aid}","case_refs",a.get("case_refs"),cases,"CaseCard",False)
        refs_exist(f"ArgumentRecord {aid}","supporting_fact_ids",a.get("supporting_fact_ids"),facts,"FactRecord",False)
        refs_exist(f"ArgumentRecord {aid}","supporting_evidence_ids",a.get("supporting_evidence_ids"),evidence,"EvidenceItem",False)
        refs_exist(f"ArgumentRecord {aid}","supporting_source_ids",a.get("supporting_source_ids"),sources,"SourceCard",False)
        if a.get("status")=="SUPPORTED":
            if not a.get("reasoning_methods") or not a.get("conclusion"):
                blockers.append({"id":"TRACE-ARG-MIN","message":f"SUPPORTED 论证 {aid} 缺少 reasoning_methods 或 conclusion。"})
            if a.get("argument_scope")=="MATTER_SPECIFIC" and (not a.get("supporting_fact_ids") or not (a.get("rule_refs") or a.get("case_refs"))):
                blockers.append({"id":"TRACE-ARG-MATTER","message":f"案件型 SUPPORTED 论证 {aid} 缺少事实或规则/案例支撑。"})

    for xid,f in findings.items():
        refs_exist(f"Finding {xid}","argument_ids",f.get("argument_ids"),arguments,"ArgumentRecord",False)
        refs_exist(f"Finding {xid}","supporting_fact_ids",f.get("supporting_fact_ids"),facts,"FactRecord",False)
        refs_exist(f"Finding {xid}","supporting_rule_ids",f.get("supporting_rule_ids"),rules,"LegalRule",False)
        refs_exist(f"Finding {xid}","supporting_evidence_ids",f.get("supporting_evidence_ids"),evidence,"EvidenceItem",False)
        refs_exist(f"Finding {xid}","case_ids",f.get("case_ids"),cases,"CaseCard",False)
        if f.get("status")=="SUPPORTED" and f.get("importance") in {"CRITICAL","HIGH"}:
            if f.get("traceability_state")!="FULL":
                blockers.append({"id":"TRACE-FINDING","message":f"重要 SUPPORTED Finding {xid} 未标记 FULL traceability。"})

    for cid,c in claims.items():
        refs_exist(f"DeliverableClaim {cid}","finding_ids",c.get("finding_ids"),findings,"Finding",False)
        refs_exist(f"DeliverableClaim {cid}","argument_ids",c.get("argument_ids"),arguments,"ArgumentRecord",False)
        refs_exist(f"DeliverableClaim {cid}","fact_ids",c.get("fact_ids"),facts,"FactRecord",False)
        refs_exist(f"DeliverableClaim {cid}","evidence_ids",c.get("evidence_ids"),evidence,"EvidenceItem",False)
        refs_exist(f"DeliverableClaim {cid}","rule_ids",c.get("rule_ids"),rules,"LegalRule",False)
        refs_exist(f"DeliverableClaim {cid}","case_ids",c.get("case_ids"),cases,"CaseCard",False)
        refs_exist(f"DeliverableClaim {cid}","source_ids",c.get("source_ids"),sources,"SourceCard",False)
        refs_exist(f"DeliverableClaim {cid}","locator_ids",c.get("locator_ids"),loc,"SourceLocator",False)
        if c.get("importance") in {"CRITICAL","HIGH"}:
            upstream=sum(len(c.get(k) or []) for k in ["finding_ids","argument_ids","fact_ids","evidence_ids","rule_ids","case_ids","source_ids"])
            if c.get("traceability_state")!="FULL" or upstream<=0:
                blockers.append({"id":"TRACE-CLAIM","message":f"重要交付命题 {cid} 没有完整上游溯源。"})

    status="BLOCKED" if blockers else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {"trace_status":status,"blockers":blockers,"warnings":warnings,
            "counts":{"locators":len(loc),"sources":len(sources),"facts":len(facts),"evidence":len(evidence),"issues":len(issues),"rules":len(rules),"cases":len(cases),"arguments":len(arguments),"findings":len(findings),"deliverable_claims":len(claims)},
            "disclaimer":"本检查只验证溯源结构和引用完整性，不判断事实真伪、法律适用或专业结论是否正确。"}


def chain_check(bundle):
    """检查跨模块对象交接、研究回填、策略节点、对抗审查回写和回写事件。只检查结构与状态，不评价实体法律正确性。"""
    blockers=[]; warnings=[]
    def index(items,key):
        return {x.get(key):x for x in (items or []) if isinstance(x,dict) and x.get(key)}
    issues=index(bundle.get("issues",[]),"issue_id")
    reqs=index(bundle.get("research_requests",[]),"research_request_id")
    results=index(bundle.get("research_results",[]),"research_result_id")
    args=index(bundle.get("arguments",[]),"argument_id")
    findings=index(bundle.get("findings",[]),"finding_id")
    options=index(bundle.get("options",[]),"option_id")
    decisions=index(bundle.get("decisions",[]),"decision_id")
    reviews=index(bundle.get("adversarial_reviews",[]),"review_id")
    writebacks=index(bundle.get("writeback_events",[]),"writeback_id")
    all_ids=set().union(issues,reqs,results,args,findings,options,decisions,reviews,writebacks)

    def check_refs(owner,field,refs,registry,label,required=False):
        refs=refs or []
        if required and not refs:
            blockers.append({"id":"CHAIN-MISSING","message":f"{owner} 缺少 {field}。"})
        for r in refs:
            if r not in registry:
                blockers.append({"id":"CHAIN-BROKEN","message":f"{owner}.{field} 引用了不存在的 {label}: {r}"})

    for qid,q in reqs.items():
        if q.get("issue_id") not in issues:
            blockers.append({"id":"CHAIN-REQ-ISSUE","message":f"ResearchRequest {qid} 无法回到 IssueRecord。"})
        check_refs(f"ResearchRequest {qid}","research_result_ids",q.get("research_result_ids"),results,"ResearchResult",False)
        if q.get("status")=="SATURATED" and not q.get("research_result_ids"):
            blockers.append({"id":"CHAIN-REQ-RESULT","message":f"ResearchRequest {qid} 标记 SATURATED 但没有研究结果。"})

    for rid,r in results.items():
        rq=r.get("research_request_id")
        if rq and rq not in reqs:
            blockers.append({"id":"CHAIN-RESULT-REQ","message":f"ResearchResult {rid} 引用了不存在的 ResearchRequest: {rq}"})
        if r.get("issue_id") not in issues:
            blockers.append({"id":"CHAIN-RESULT-ISSUE","message":f"ResearchResult {rid} 无法回到 IssueRecord。"})
        check_refs(f"ResearchResult {rid}","affected_argument_ids",r.get("affected_argument_ids"),args,"ArgumentRecord",False)
        check_refs(f"ResearchResult {rid}","affected_finding_ids",r.get("affected_finding_ids"),findings,"Finding",False)
        if r.get("writeback_required"):
            linked=[w for w in writebacks.values() if rid in (w.get("trigger_ref_ids") or [])]
            if not linked:
                blockers.append({"id":"CHAIN-RESEARCH-WRITEBACK","message":f"ResearchResult {rid} 标记需要回写，但没有对应 WriteBackEvent。"})

    for oid,o in options.items():
        if o.get("issue_id") not in issues:
            blockers.append({"id":"CHAIN-OPTION-ISSUE","message":f"OptionRecord {oid} 无法回到 IssueRecord。"})
        check_refs(f"OptionRecord {oid}","supporting_argument_ids",o.get("supporting_argument_ids"),args,"ArgumentRecord",False)

    for did,d in decisions.items():
        check_refs(f"DecisionRecord {did}","option_ids",d.get("option_ids"),options,"OptionRecord",d.get("decision_level")=="C")
        check_refs(f"DecisionRecord {did}","recommendation_basis_argument_ids",d.get("recommendation_basis_argument_ids"),args,"ArgumentRecord",False)
        if d.get("decision_level")=="C" and d.get("status")!="RESOLVED":
            blockers.append({"id":"CHAIN-DECISION-OPEN","message":f"C级 DecisionRecord {did} 尚未由人工解决。"})
        if d.get("decision_level")=="D" and d.get("status")!="PROHIBITED":
            blockers.append({"id":"CHAIN-DECISION-D","message":f"D级 DecisionRecord {did} 必须保持 PROHIBITED。"})
        if d.get("status")=="RESOLVED" and d.get("selected_option_id") and d.get("selected_option_id") not in options:
            blockers.append({"id":"CHAIN-DECISION-OPTION","message":f"DecisionRecord {did} 选择了不存在的 OptionRecord。"})

    for aid,a in reviews.items():
        check_refs(f"AdversarialReviewRecord {aid}","target_finding_ids",a.get("target_finding_ids"),findings,"Finding",True)
        check_refs(f"AdversarialReviewRecord {aid}","target_argument_ids",a.get("target_argument_ids"),args,"ArgumentRecord",False)
        check_refs(f"AdversarialReviewRecord {aid}","revised_argument_ids",a.get("revised_argument_ids"),args,"ArgumentRecord",False)
        check_refs(f"AdversarialReviewRecord {aid}","revised_finding_ids",a.get("revised_finding_ids"),findings,"Finding",False)
        if a.get("status")=="COMPLETE_REVISED" and not (a.get("revised_argument_ids") or a.get("revised_finding_ids")):
            blockers.append({"id":"CHAIN-ADV-REVISION","message":f"AdversarialReviewRecord {aid} 声称已修正但没有修正对象。"})
        if a.get("status")=="COMPLETE_UNCHANGED_WITH_REASON" and not a.get("unchanged_reason"):
            blockers.append({"id":"CHAIN-ADV-UNCHANGED","message":f"AdversarialReviewRecord {aid} 维持原结论但没有说明理由。"})

    for wid,w in writebacks.items():
        for r in w.get("trigger_ref_ids") or []:
            if r not in all_ids:
                warnings.append({"id":"CHAIN-WRITEBACK-TRIGGER","message":f"WriteBackEvent {wid} 的 trigger_ref_id 无法在当前执行包中定位: {r}"})
        for r in w.get("affected_refs") or []:
            if r not in all_ids:
                warnings.append({"id":"CHAIN-WRITEBACK-AFFECTED","message":f"WriteBackEvent {wid} 的 affected_ref 无法在当前执行包中定位: {r}"})
        if w.get("status")=="OPEN":
            blockers.append({"id":"CHAIN-WRITEBACK-OPEN","message":f"WriteBackEvent {wid} 尚未应用。"})
        if w.get("status")=="APPLIED" and not (w.get("updated_refs") or w.get("reviewed_unchanged_refs")):
            blockers.append({"id":"CHAIN-WRITEBACK-EMPTY","message":f"WriteBackEvent {wid} 标记 APPLIED 但没有更新或复核对象。"})

    status="BLOCKED" if blockers else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {"chain_status":status,"blockers":blockers,"warnings":warnings,
            "counts":{"issues":len(issues),"research_requests":len(reqs),"research_results":len(results),"arguments":len(args),"findings":len(findings),"options":len(options),"decisions":len(decisions),"adversarial_reviews":len(reviews),"writeback_events":len(writebacks)},
            "disclaimer":"本检查只验证跨模块交接、状态和回写结构，不判断事实真伪、法律适用或策略优劣。"}



def model_check(bundle):
    """检查事项工作模型、问题树、审阅问题集、权威图谱、类案矩阵、论证地图等对象的基本引用完整性。"""
    blockers=[]; warnings=[]
    def idx(items,key): return {x.get(key):x for x in (items or []) if isinstance(x,dict) and x.get(key)}
    profiles=idx(bundle.get("task_profiles",[]),"profile_id")
    models=idx(bundle.get("matter_models",[]),"model_id")
    trees=idx(bundle.get("issue_trees",[]),"tree_id")
    qsets=idx(bundle.get("review_question_sets",[]),"question_set_id")
    amaps=idx(bundle.get("authority_maps",[]),"authority_map_id")
    cmats=idx(bundle.get("case_matrices",[]),"matrix_id")
    argmaps=idx(bundle.get("argument_maps",[]),"map_id")
    candidates=idx(bundle.get("legal_object_candidates",[]),"candidate_id")
    preveiws=idx(bundle.get("plan_reviews",[]),"plan_review_id")
    bcrecs=idx(bundle.get("behavior_contract_records",[]),"record_id")
    issues=idx(bundle.get("issues",[]),"issue_id")
    cases=idx(bundle.get("case_cards",[]),"case_id")
    args=idx(bundle.get("arguments",[]),"argument_id")
    materials=idx(bundle.get("materials",[]),"material_id")
    rules=idx(bundle.get("legal_rules",[]),"rule_id")
    sources=idx(bundle.get("sources",[]),"source_id")
    locs=idx(bundle.get("source_locators",[]),"locator_id")

    for mid,m in models.items():
        for pid in m.get("task_profile_ids") or []:
            if pid not in profiles: blockers.append({"id":"MODEL-PROFILE","message":f"MatterWorkingModel {mid} 引用了不存在的 TaskProfile: {pid}"})
        for iid in m.get("issue_ids") or []:
            if iid not in issues: blockers.append({"id":"MODEL-ISSUE","message":f"MatterWorkingModel {mid} 引用了不存在的 Issue: {iid}"})
        if m.get("status")=="NEEDS_UPDATE": blockers.append({"id":"MODEL-STALE","message":f"MatterWorkingModel {mid} 仍标记 NEEDS_UPDATE。"})

    for tid,t in trees.items():
        nodeids={n.get("issue_id") for n in t.get("nodes") or [] if n.get("issue_id")}
        for rid in t.get("root_issue_ids") or []:
            if rid not in nodeids: blockers.append({"id":"TREE-ROOT","message":f"IssueTree {tid} 根问题 {rid} 不在 nodes 中。"})
        for n in t.get("nodes") or []:
            if n.get("issue_id") not in issues: warnings.append({"id":"TREE-ISSUE","message":f"IssueTree {tid} 的 {n.get('issue_id')} 未在当前执行包 IssueRecord 中出现。"})
            p=n.get("parent_issue_id")
            if p and p not in nodeids: blockers.append({"id":"TREE-PARENT","message":f"IssueTree {tid} 节点 {n.get('issue_id')} 的 parent 不存在: {p}"})

    for qid,q in qsets.items():
        qids=[x.get("question_id") for x in q.get("questions") or []]
        if len(qids)!=len(set(qids)): blockers.append({"id":"REVIEWQ-DUP","message":f"ReviewQuestionSet {qid} 存在重复 question_id。"})
        for iid in q.get("linked_issue_ids") or []:
            if iid not in issues: warnings.append({"id":"REVIEWQ-ISSUE","message":f"ReviewQuestionSet {qid} 关联 Issue 不在当前执行包: {iid}"})

    for aid,a in amaps.items():
        if a.get("issue_id") not in issues: warnings.append({"id":"AUTH-ISSUE","message":f"AuthorityMap {aid} 的 Issue 不在当前执行包。"})
        for n in a.get("nodes") or []:
            for r in n.get("rule_refs") or []:
                if rules and r not in rules: blockers.append({"id":"AUTH-RULE","message":f"AuthorityMap {aid} 引用了不存在的 Rule: {r}"})
            for c in n.get("case_refs") or []:
                if cases and c not in cases: blockers.append({"id":"AUTH-CASE","message":f"AuthorityMap {aid} 引用了不存在的 Case: {c}"})
            for src in n.get("source_refs") or []:
                if sources and src not in sources: blockers.append({"id":"AUTH-SOURCE","message":f"AuthorityMap {aid} 引用了不存在的 Source: {src}"})

    for cid,c in cmats.items():
        if c.get("issue_id") not in issues: warnings.append({"id":"CASEMATRIX-ISSUE","message":f"CaseMatrix {cid} 的 Issue 不在当前执行包。"})
        for row in c.get("rows") or []:
            if cases and row.get("case_id") not in cases: blockers.append({"id":"CASEMATRIX-CASE","message":f"CaseMatrix {cid} 引用了不存在的 Case: {row.get('case_id')}"})
            if not row.get("similarities") or not row.get("differences"): blockers.append({"id":"CASEMATRIX-COMPARE","message":f"CaseMatrix {cid} 的案例 {row.get('case_id')} 缺少相似点或区别点。"})

    for gid,g in argmaps.items():
        nodeids={n.get("argument_id") for n in g.get("nodes") or [] if n.get("argument_id")}
        for aid in nodeids:
            if args and aid not in args: blockers.append({"id":"ARGMAP-ARG","message":f"ArgumentMap {gid} 引用了不存在的 Argument: {aid}"})
        for e in g.get("edges") or []:
            if e.get("from_argument_id") not in nodeids or e.get("to_argument_id") not in nodeids:
                blockers.append({"id":"ARGMAP-EDGE","message":f"ArgumentMap {gid} 存在指向非节点论证的边。"})

    for cid,c in candidates.items():
        if materials and c.get("material_id") not in materials: blockers.append({"id":"CAND-MATERIAL","message":f"LegalObjectCandidate {cid} 引用了不存在的 Material: {c.get('material_id')}"})
        if c.get("verification_status")=="VERIFIED" and not c.get("source_locator_ids"):
            blockers.append({"id":"CAND-VERIFY","message":f"LegalObjectCandidate {cid} 标记 VERIFIED 但没有来源定位。"})

    for rid,r in bcrecs.items():
        if int(r.get("critical_violation_count") or 0)>0 or r.get("status")=="BLOCKED": blockers.append({"id":"BEHAVIOR","message":f"BehaviorContractRecord {rid} 存在关键违反。"})

    status="BLOCKED" if blockers else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {"model_status":status,"blockers":blockers,"warnings":warnings,
            "counts":{"task_profiles":len(profiles),"matter_models":len(models),"issue_trees":len(trees),"review_question_sets":len(qsets),"authority_maps":len(amaps),"case_matrices":len(cmats),"argument_maps":len(argmaps),"legal_object_candidates":len(candidates),"plan_reviews":len(preveiws),"behavior_contract_records":len(bcrecs)},
            "disclaimer":"本检查仅验证事项工作模型与分析工具的结构和引用完整性，不判断实体法律结论正确性。"}


def derive_capability_requirements(plan):
    """根据执行计划推导最低运行能力要求。只描述能力，不绑定厂商。"""
    c=plan.get("context",{})
    reqs=[]
    def add(rid,ctype,reason,trust=None,locator=False,current=False,allow_downgrade=False):
        reqs.append({
            "requirement_id":rid,"capability_type":ctype,"required":True,
            "minimum_status":"VERIFIED_SUPPORTED","minimum_trust_level":trust,
            "must_preserve_locator":bool(locator),"must_support_currentness":bool(current),
            "allow_downgrade":bool(allow_downgrade),"reason":reason
        })
    if c.get("requires_current_law"):
        add("CAP-LEGAL","LEGAL_AUTHORITY_SOURCE","需要现行法律依据核验","AUTHORIZED_PROFESSIONAL",True,True,False)
    if c.get("professional_legal_source_required"):
        add("CAP-PRO-LEGAL","LEGAL_AUTHORITY_SOURCE","用户/任务明确要求专业法律信源","AUTHORIZED_PROFESSIONAL",True,True,False)
    if c.get("case_matrix_required"):
        add("CAP-CASE","CASE_SOURCE","本次需要案例检索和类案比较","RELIABLE_SECONDARY",True,False,False)
    if c.get("private_knowledge_required"):
        add("CAP-KB","PRIVATE_KNOWLEDGE","用户要求结合其私有知识库","USER_CONTROLLED",True,False,False)
    if c.get("need_ocr") or c.get("input_capability_gap"):
        add("CAP-OCR","OCR","输入包含扫描件或当前原生读取能力不足",None,True,False,True)
    if c.get("need_docx"):
        add("CAP-DOCX","DOCX_OUTPUT","用户要求 DOCX 交付",None,False,False,False)
    if c.get("need_pdf"):
        add("CAP-PDF","PDF_OUTPUT","用户要求 PDF 交付",None,False,False,False)
    if c.get("diagram_required"):
        add("CAP-DIAGRAM","DIAGRAM_DELIVERY","本次要求图形化交付；优先 PNG，可降级为自包含 HTML/图源",None,False,False,True)
    if c.get("native_track_changes_required"):
        add("CAP-TRACK","NATIVE_TRACK_CHANGES","用户明确要求原生修订模式",None,False,False,False)
    return reqs


def capability_check(plan, profile):
    """把任务能力需求与当前运行能力档案对照。只检查声明和结构，不验证第三方服务真实政策。"""
    blockers=[]; warnings=[]; resolutions=[]
    caps=[x for x in profile.get("capabilities",[]) if isinstance(x,dict)]
    # 图形化交付允许由基础运行能力合成：有渲染+PNG能力视为完整支持；
    # 只有文本文件+HTML能力时，按自包含 HTML/内嵌 SVG 作为可披露降级方案。
    if not any(c.get("capability_type")=="DIAGRAM_DELIVERY" for c in caps):
        can_render = any(bool(profile.get(k)) for k in ["can_render_html","can_render_svg","can_render_mermaid","can_render_graphviz","can_render_plantuml"])
        can_png = bool(profile.get("can_export_png"))
        can_html_fallback = bool(profile.get("can_create_text_file")) and bool(profile.get("can_generate_html") or profile.get("can_render_html"))
        if can_render and can_png:
            caps.append({"capability_id":"synthetic-diagram-png","capability_type":"DIAGRAM_DELIVERY","status":"VERIFIED_SUPPORTED","trust_level":"NOT_APPLICABLE","supports_locator":False,"supports_currentness":False,"external_processing_required":False})
        elif can_html_fallback:
            caps.append({"capability_id":"synthetic-diagram-html","capability_type":"DIAGRAM_DELIVERY","status":"DOWNGRADED","trust_level":"NOT_APPLICABLE","supports_locator":False,"supports_currentness":False,"external_processing_required":False})
    reqs=derive_capability_requirements(plan)
    def trust_ok(cap, req):
        need=req.get("minimum_trust_level")
        if not need: return True
        return TRUST_RANK.get(cap.get("trust_level"),-1) >= TRUST_RANK.get(need,999)
    def candidate_score(cap):
        return (STATUS_RANK.get(cap.get("status"),0), TRUST_RANK.get(cap.get("trust_level"),0), bool(cap.get("supports_locator")), bool(cap.get("supports_currentness")))
    for req in reqs:
        same=[c for c in caps if c.get("capability_type")==req.get("capability_type")]
        eligible=[]
        for cap in same:
            if cap.get("status") not in {"VERIFIED_SUPPORTED","DOWNGRADED","PARTIAL","SUPPORTED_BUT_UNVERIFIED"}: continue
            if not trust_ok(cap,req): continue
            if req.get("must_preserve_locator") and not cap.get("supports_locator"): continue
            if req.get("must_support_currentness") and not cap.get("supports_currentness"): continue
            eligible.append(cap)
        eligible=sorted(eligible,key=candidate_score,reverse=True)
        selected=eligible[0] if eligible else None
        item={"requirement":req,"selected_capability_id":selected.get("capability_id") if selected else None,"status":None,"notes":[]}
        if not selected:
            item["status"]="BLOCKED"
            blockers.append({"id":req["requirement_id"],"message":f"缺少满足要求的能力：{req['capability_type']}"})
        elif selected.get("status")=="VERIFIED_SUPPORTED":
            item["status"]="PASS"
        elif req.get("allow_downgrade") and selected.get("status") in {"DOWNGRADED","PARTIAL","SUPPORTED_BUT_UNVERIFIED"}:
            item["status"]="DOWNGRADED"
            item["notes"].append(f"当前能力状态为 {selected.get('status')}，需要披露限制并按任务决定是否人工复核。")
            warnings.append({"id":req["requirement_id"],"message":f"能力 {req['capability_type']} 采用降级/未完全验证实现。"})
        else:
            item["status"]="BLOCKED"
            blockers.append({"id":req["requirement_id"],"message":f"能力 {req['capability_type']} 当前状态 {selected.get('status')} 未达到任务要求。"})
        if selected and selected.get("external_processing_required") and plan.get("context",{}).get("sensitive_material"):
            item["notes"].append("该能力涉及外部处理；敏感材料必须另行通过外部处理风险门控并取得明确授权。")
            warnings.append({"id":"CAP-CONSENT","message":f"所选能力 {selected.get('capability_id')} 涉及外部处理，敏感材料需另行授权。"})
        resolutions.append(item)
    status="BLOCKED" if blockers else ("DOWNGRADED" if any(x.get("status")=="DOWNGRADED" for x in resolutions) else "PASS")
    return {"capability_status":status,"runtime_id":profile.get("runtime_id"),"requirements":reqs,"resolutions":resolutions,"blockers":blockers,"warnings":warnings,
            "disclaimer":"能力解析只基于当前能力档案，不验证第三方服务条款、数据政策、法律内容准确性或实际网络可用性。"}

def write_json(obj,path):
    text=json.dumps(obj,ensure_ascii=False,indent=2)+"\n"
    if path: Path(path).write_text(text,encoding="utf-8")
    else: print(text,end="")


def main():
    parser=argparse.ArgumentParser(description="爽律 Skill 工程执行器")
    sub=parser.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("plan",help="生成执行计划和渐进式加载路径")
    p.add_argument("--task",required=True)
    p.add_argument("--skill",choices=SKILLS)
    p.add_argument("--role")
    p.add_argument("--stage")
    p.add_argument("--important",action="store_true")
    p.add_argument("--formal-delivery",action="store_true")
    p.add_argument("--need-current-law",action="store_true")
    p.add_argument("--input-gap",action="store_true")
    p.add_argument("--sensitive",action="store_true")
    p.add_argument("--structured-review",action="store_true",help="本次任务需要多文件/跨来源结构化审阅")
    p.add_argument("--strategy-choice",action="store_true",help="本次任务存在需要比较的策略/行动选项")
    p.add_argument("--need-cases",action="store_true",help="本次任务明确需要类案研究/案例比较")
    p.add_argument("--argument-map",action="store_true",help="本次任务需要显式论证地图")
    p.add_argument("--plan-review",action="store_true",help="本次执行计划涉及重大范围/外部动作等，需要人工确认或修订")
    p.add_argument("--private-knowledge",action="store_true",help="本次任务明确需要使用用户私有知识库/历史资料")
    p.add_argument("--professional-legal-source",action="store_true",help="本次任务明确要求专业法律数据库/指定法律信源")
    p.add_argument("--need-ocr",action="store_true",help="本次输入需要 OCR/扫描件读取能力")
    p.add_argument("--need-docx",action="store_true",help="本次明确要求 DOCX 交付")
    p.add_argument("--need-pdf",action="store_true",help="本次明确要求 PDF 交付")
    p.add_argument("--native-track-changes",action="store_true",help="本次明确要求原生 Track Changes/修订模式")
    p.add_argument("--quick-understanding",action="store_true",help="本次需要事项快速理解包")
    p.add_argument("--diagram",action="store_true",help="本次需要至少一项图形化示意")
    p.add_argument("--contract-report-only",action="store_true",help="合同任务由用户明确要求只出报告/意见，不实际修改合同")
    p.add_argument("--bundle",action="store_true",help="本次任务需要成套交付/多文书材料包")
    p.add_argument("--template-required",action="store_true",help="本次任务明确要求使用用户/事项模板")
    p.add_argument("--user-profile",help="可选：用户个性化档案 user-profile.json")
    p.add_argument("--matter-profile",help="可选：当前事项个性化档案")
    p.add_argument("--full-checklist",action="store_true")
    p.add_argument("--out")

    acheck=sub.add_parser("activation-check",help="评估当前任务是否应自动激活爽律（本地回退/测试）")
    acheck.add_argument("--task",required=True)
    acheck.add_argument("--user-profile")
    acheck.add_argument("--matter-profile")
    acheck.add_argument("--out")

    c=sub.add_parser("checklist",help="根据执行计划生成本次动态清单")
    c.add_argument("--plan",required=True)
    c.add_argument("--out")
    c.add_argument("--format",choices=["md","json"],default="md")

    s=sub.add_parser("init-state",help="根据执行计划生成工程执行状态模板")
    s.add_argument("--plan",required=True)
    s.add_argument("--out",required=True)

    v=sub.add_parser("validate",help="执行正式交付前质量门控")
    v.add_argument("--state",required=True)
    v.add_argument("--out")

    t=sub.add_parser("trace-check",help="检查全链路溯源包的引用完整性")
    t.add_argument("--bundle",required=True)
    t.add_argument("--out")

    x=sub.add_parser("chain-check",help="检查跨模块交接、策略节点、对抗审查回写和回写事件")
    x.add_argument("--bundle",required=True)
    x.add_argument("--out")

    mcheck=sub.add_parser("model-check",help="检查事项工作模型、问题树、审阅问题集、权威图谱、类案矩阵和论证地图")
    mcheck.add_argument("--bundle",required=True)
    mcheck.add_argument("--out")

    capcheck=sub.add_parser("capability-check",help="将执行计划与当前运行能力档案对照，输出满足/降级/阻断项")
    capcheck.add_argument("--plan",required=True)
    capcheck.add_argument("--profile",required=True)
    capcheck.add_argument("--out")

    args=parser.parse_args()
    if args.cmd=="activation-check":
        report=activation_decision(args.task,args.user_profile,args.matter_profile); write_json(report,args.out)
        return 0 if report["decision"] in {"AUTO_ACTIVATE","EXPLICIT_ACTIVATE"} else (2 if report["decision"]=="CONFIRM" else 4)
    if args.cmd=="plan":
        plan=build_plan(args); write_json(plan,args.out)
        if plan["route_status"]=="UNRESOLVED":
            print("提示：路由未唯一确定，应由 Agent 结合语义或由用户指定主技能。",file=sys.stderr)
            return 2
        if plan["route_status"]=="SKIPPED_BY_ACTIVATION":
            print("提示：根据用户激活偏好/本次禁用要求，不应自动进入爽律。",file=sys.stderr)
            return 4
        return 0
    if args.cmd=="checklist":
        plan=load_json(Path(args.plan)); ck=build_checklist(plan)
        if args.format=="json": write_json(ck,args.out)
        else:
            text=checklist_markdown(ck)
            if args.out: Path(args.out).write_text(text,encoding="utf-8")
            else: print(text,end="")
        return 0
    if args.cmd=="init-state":
        plan=load_json(Path(args.plan)); write_json(build_state_template(plan),args.out); return 0
    if args.cmd=="validate":
        state=load_json(Path(args.state)); report=validate_state(state); write_json(report,args.out)
        return 3 if report["gate_status"]=="BLOCKED" else 0
    if args.cmd=="trace-check":
        bundle=load_json(Path(args.bundle)); report=trace_check(bundle); write_json(report,args.out)
        return 3 if report["trace_status"]=="BLOCKED" else 0
    if args.cmd=="chain-check":
        bundle=load_json(Path(args.bundle)); report=chain_check(bundle); write_json(report,args.out)
        return 3 if report["chain_status"]=="BLOCKED" else 0
    if args.cmd=="model-check":
        bundle=load_json(Path(args.bundle)); report=model_check(bundle); write_json(report,args.out)
        return 3 if report["model_status"]=="BLOCKED" else 0
    if args.cmd=="capability-check":
        plan=load_json(Path(args.plan)); profile=load_json(Path(args.profile)); report=capability_check(plan,profile); write_json(report,args.out)
        return 3 if report["capability_status"]=="BLOCKED" else 0

if __name__=="__main__":
    raise SystemExit(main())
