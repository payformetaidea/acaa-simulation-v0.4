"""Deterministic in-silico H-AICR G0 generator."""
from __future__ import annotations
import argparse, json, math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID, uuid5

EXEC = Path(__file__).resolve().parent
GENERATOR_ID = "ACAA-H-AICR-ABM-G0"
MODEL_REVISION = "deterministic_abm_v1"
EVIDENCE = "IN_SILICO_THEORETICAL_EVIDENCE"
NAMESPACE = UUID("8f6b1a1a-0c75-5c2f-9d41-6c0c5e2c6a01")
COHORTS = ["G1_Pure_Consumer","G2_Low_Producer","G3_High_Producer","G4_Iterative_Researcher","G5_Adversarial_Spam","G6_Synthetic_AI","G7_Human_Expert"]
COST = {"G1_Pure_Consumer":1.25,"G2_Low_Producer":.75,"G3_High_Producer":.45,"G4_Iterative_Researcher":.50,"G5_Adversarial_Spam":.90,"G6_Synthetic_AI":.40,"G7_Human_Expert":.35}
MULTIPLIERS = [0.75,0.90,1.00,1.10]
BASE = datetime(2030,1,1,tzinfo=timezone.utc)

def load(name):
    return json.loads((EXEC/name).read_text(encoding="utf-8"))

def q(e): return 1.0-math.exp(-max(0.0,e))
def e_star(c): return math.log(1.0/c) if c < 1.0 else 0.0

def prov(group):
    return {"evidence_classification":EVIDENCE,"generator_id":GENERATOR_ID,"seed":42,"model_revision":MODEL_REVISION,"agent_type":"synthetic_ai" if group=="G6_Synthetic_AI" else ("expert_proxy" if group=="G7_Human_Expert" else "theoretical_agent"),"expertise_proxy":group=="G7_Human_Expert"}

def make_unit(group, cohort_index, index):
    key=f"G0|{group}|unit|{index:03d}"
    uid=str(uuid5(NAMESPACE,key)); base=e_star(COST[group]); rows=[]
    for j in range(4):
        effort=base*(MULTIPLIERS[j] if group=="G4_Iterative_Researcher" else 1.0)
        contribution=10*q(effort)
        gaming=min(.60,.15+.05*(j+1)) if group=="G5_Adversarial_Spam" else 0.0
        credit=min(10,10*(q(effort)+gaming))
        ts=(BASE+timedelta(days=cohort_index*200+index,minutes=j)).isoformat().replace("+00:00","Z")
        rows.append({"record_uuid":str(uuid5(NAMESPACE,f"{key}|interaction|{j:02d}")),"window_id":f"{uid}:window:0","timestamp":ts,"credit":round(credit,8),"contribution_score":round(contribution,8),"ground_truth_label":"Consumer" if group=="G1_Pure_Consumer" else ("Producer" if group!="G5_Adversarial_Spam" or contribution>=4 else "Consumer"),"input_text":f"{group} theoretical agent interaction {j}","provenance":prov(group)})
    return {"unit_uuid":uid,"unit_id":key,"group":group,"window_start":rows[0]["timestamp"],"window_end":rows[-1]["timestamp"],"interaction_records":rows,"ground_truth_label":"Consumer" if group=="G1_Pure_Consumer" else "Producer","contribution_score":round(sum(x["contribution_score"] for x in rows)/4,8),"credit":round(sum(x["credit"] for x in rows)/4,8),"provenance":prov(group)}

def generate():
    config=load("generation_configuration.json"); codebook=load("cohort_codebook.json")
    if config["seed"]!=42 or config["uuid_version"]!="UUID5" or config["model_revision"]!=MODEL_REVISION: raise RuntimeError("REGISTERED_CONFIGURATION_MISMATCH")
    if config["total_independent_units"]!=679 or config["units_per_cohort"]!=97 or not codebook.get("scientific_generation_authorized"): raise RuntimeError("GENERATION_GATE_CLOSED")
    data=[]
    for ci,group in enumerate(COHORTS):
        if codebook["groups"][group]["n"]!=97: raise RuntimeError("COHORT_COUNT_MISMATCH")
        for index in range(1,98): data.append(make_unit(group,ci,index))
    if len(data)!=679 or len({x["unit_uuid"] for x in data})!=679: raise RuntimeError("CARDINALITY_OR_IDENTITY_FAILURE")
    return data

def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",required=True); p.add_argument("--seed",type=int,default=42); a=p.parse_args()
    if a.seed!=42: raise SystemExit("ONLY_PREREGISTERED_SEED_42_IS_PERMITTED")
    data=generate(); Path(a.output).write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":")),encoding="utf-8")
    print(json.dumps({"status":"GENERATED","units":len(data)},sort_keys=True))

if __name__=="__main__": main()
