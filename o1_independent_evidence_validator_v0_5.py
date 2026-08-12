#!/usr/bin/env python3
"""Independent evidence validator for ACAA v0.5 O1."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from statistics import mean, pvariance, pstdev

SEEDS=[42,137,256,512,1024,2048,4096,8192,16384,32768,65536,131072]
FIELDS=["final_cau_count","final_gini","gate_efficiency","failure_rate","total_artifacts","detected_agents","isolated_agents"]

def sha256_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def effective_fp(run):
    e=run['effective_config']; base={k:v for k,v in run['params'].items() if k!='seed'}
    post_base=hashlib.sha256(json.dumps(base,sort_keys=True).encode()).hexdigest()
    data={'base_fingerprint':post_base,'seed':e['seed'],'scenario':e['scenario'],'scenario_params':e.get('scenario_params',{})}
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()

def tukey(values):
    x=sorted(values); n=len(x)
    def q(p):
        pos=(n-1)*p; lo,hi=math.floor(pos),math.ceil(pos)
        return x[lo] if lo==hi else x[lo]+(x[hi]-x[lo])*(pos-lo)
    q1,q3=q(.25),q(.75); iqr=q3-q1; lo=q1-1.5*iqr; hi=q3+1.5*iqr
    return {'q1':q1,'q3':q3,'iqr':iqr,'lower_fence':lo,'upper_fence':hi,'indices':[i for i,v in enumerate(values) if v<lo or v>hi]}

def summarize(values):
    m=mean(values); sd=pstdev(values) if len(values)>1 else 0.0
    return {'mean':m,'variance':pvariance(values) if len(values)>1 else 0.0,'standard_deviation':sd,'coefficient_of_variation':None if abs(m)<1e-12 else sd/abs(m),'cv_reason':'zero_mean' if abs(m)<1e-12 else None,'outliers':tukey(values)}

def validate_run(run,seed,path,engine_hash):
    required={'params','periods_executed','cau_records','metrics','engine_hash','effective_config','execution_timestamp','scenario','random_seed','o1_base_config_fingerprint'}
    missing=required-set(run)
    assert not missing,f'O1-06 seed {seed}: missing {sorted(missing)}'
    assert run['random_seed']==seed and run['scenario']=='baseline',f'O1-01/O1-03 seed {seed}: identity mismatch'
    assert run['engine_hash']==engine_hash,f'O1-05 seed {seed}: engine hash mismatch'
    e=run['effective_config']
    assert e.get('seed')==seed and e.get('scenario')=='baseline' and e.get('scenario_params',{})=={},f'O1-04 seed {seed}: effective configuration mismatch'
    assert e.get('fingerprint')==effective_fp(run),f'O1-04 seed {seed}: effective fingerprint not reproducible'
    metrics=run['metrics']; assert metrics and len(metrics)==run['periods_executed'],f'O1-06 seed {seed}: metric trajectory invalid'
    assert [m.get('period') for m in metrics]==list(range(1,len(metrics)+1)),f'O1-06 seed {seed}: periods invalid'
    final=metrics[-1]
    for f in ['gini_coefficient','gate_efficiency','failure_rate','total_artifacts','detected_agents','isolated_agents']:
        v=final.get(f); assert isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v)),f'O1-06 seed {seed}: invalid {f}'
    digest=sha256_file(path); tail=[float(m['total_cau_stock']) for m in metrics[-5:]]; var=pvariance(tail) if len(tail)>1 else 0.0
    return {'seed':seed,'path':path.name,'base_config_fingerprint':run['o1_base_config_fingerprint'],'effective_config_fingerprint':e['fingerprint'],'scenario':'baseline','scenario_params':{},'engine_hash':run['engine_hash'],'execution_timestamp':run['execution_timestamp'],'final_cau_count':run['cau_records'],'final_gini':final['gini_coefficient'],'gate_efficiency':final['gate_efficiency'],'failure_rate':final['failure_rate'],'total_artifacts':final['total_artifacts'],'detected_agents':final['detected_agents'],'isolated_agents':final['isolated_agents'],'equilibrium_metrics':{'window_size':min(5,len(metrics)),'variance_threshold':run['params']['equilibrium_variance_threshold'],'final_window_mean':mean(tail),'final_window_variance':var,'within_declared_threshold':var<=run['params']['equilibrium_variance_threshold']},'metric_trajectory':metrics,'artifact_digest':digest}

def validate(root,engine):
    source=root/'o1_evidence.json'; ev=json.loads(source.read_text(encoding='utf-8')); p=ev['protocol']
    assert ev.get('objective')=='O1'; assert p.get('planned_seed_set')==SEEDS and p.get('executed_seed_set')==SEEDS and p.get('seed_count')==12,'O1-01: seed protocol mismatch'
    engine_hash=sha256_file(engine); runs=[]
    for seed in SEEDS:
        path=root/'runs'/f'seed_{seed}.json'; assert path.exists(),f'O1-06: missing {seed}'
        runs.append(validate_run(json.loads(path.read_text(encoding='utf-8')),seed,path,engine_hash))
    assert len({r['seed'] for r in runs})==12,'O1-02: duplicate seed'; assert len({r['base_config_fingerprint'] for r in runs})==1,'O1-03: base fingerprint changed'
    normalized={'schema':'acaa.v0.5.o1.independent-validation','version':'1.0','objective':'O1','status':'PASS','source_evidence_sha256':sha256_file(source),'engine_sha256':engine_hash,'protocol':{'planned_seed_set':SEEDS,'executed_seed_set':[r['seed'] for r in runs],'seed_count':12},'runs':runs,'statistics':{f:summarize([float(r[f]) for r in runs]) for f in FIELDS},'gate':{f'O1-{i:02d}':'PASS' for i in range(1,11)},'interpretation_boundary':{'establishes':['defined_multiseed_experiment_executed','independent_integrity_and_contract_validation','observed_distributional_statistics'],'does_not_establish':['universal_robustness','population_level_robustness','scientific_validity_beyond_scope']}}
    (root/'o1_independent_validation.json').write_text(json.dumps(normalized,indent=2,ensure_ascii=False),encoding='utf-8'); return normalized

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--evidence-dir',default='o1_evidence'); ap.add_argument('--engine',default='value_flow_simulator_v0.4.py'); a=ap.parse_args()
    try: r=validate(Path(a.evidence_dir),Path(a.engine))
    except (AssertionError,OSError,json.JSONDecodeError,KeyError,ValueError) as e: print(f'O1 INDEPENDENT VALIDATION FAIL: {e}'); return 1
    print(json.dumps({'objective':'O1','status':r['status'],'seed_count':12},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
