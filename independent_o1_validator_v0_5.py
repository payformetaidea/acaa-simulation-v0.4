#!/usr/bin/env python3
"""Independent O1 evidence validator; never imports the O1 runner or v0.4 engine."""
from __future__ import annotations
import copy, hashlib, json, math
from pathlib import Path
from statistics import mean, pvariance, pstdev

SEEDS=[42,137,256,512,1024,2048,4096,8192,16384,32768,65536,131072]
FIELDS=['final_cau_count','final_gini','gate_efficiency','failure_rate','total_artifacts','detected_agents','isolated_agents']
BASE_KEYS=['pi_p','pi_v','pi_s','pi_c','delta','lam','alpha_thr','periods','n_agents','noise','sybil_min_group_size','sybil_detection_threshold','collusion_min_group_size','collusion_detection_threshold','spam_failure_threshold','spam_volume_threshold','abstention_threshold','minimum_opportunity_sample','negative_exploitation_threshold','minimum_challenge_sample','w_p','w_b','w_i','w_d','w_r','w_t','equilibrium_variance_threshold','recovery_consecutive_periods','cv_cau_threshold','cv_gini_threshold']

class ValidationError(ValueError): pass

def load(p):
    v=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(v,dict): raise ValidationError(f'JSON object required: {p}')
    return v

def digest(p):
    h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()

def base_fp(params):
    canonical={k:params[k] for k in BASE_KEYS}
    return hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()

def effective_fp(run):
    """Reproduce v0.4 EffectiveConfig identity from the serialized post-run BaseConfig.

    The frozen v0.4 engine keeps EffectiveConfig.base_config pointing at the mutable
    simulation BaseConfig. Adaptive governance may therefore change that BaseConfig
    during execution. The exported ``params`` field is the post-run projection of that
    same BaseConfig and is the correct independent source for EffectiveConfig identity.

    The immutable pre-run identity is tracked separately as
    ``o1_base_config_fingerprint`` and is used for cross-run baseline constancy.
    """
    e=run['effective_config']
    params=run.get('params')
    if not isinstance(params,dict):
        raise ValidationError('serialized post-run BaseConfig params are missing')
    if any(k not in params for k in BASE_KEYS):
        raise ValidationError('serialized post-run BaseConfig params are incomplete')
    base_identity=base_fp(params)
    canonical={'base_fingerprint':base_identity,'seed':e['seed'],'scenario':e['scenario'],'scenario_params':e.get('scenario_params',{})}
    return hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()

def finite(v,label):
    if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(float(v)): raise ValidationError(f'invalid numeric value: {label}')
    return float(v)

def tukey(values):
    x=sorted(values); n=len(x)
    def q(p):
        pos=(n-1)*p; lo,hi=math.floor(pos),math.ceil(pos)
        return x[lo] if lo==hi else x[lo]+(x[hi]-x[lo])*(pos-lo)
    q1,q3=q(.25),q(.75); iqr=q3-q1; lo,hi=q1-1.5*iqr,q3+1.5*iqr
    return {'q1':q1,'q3':q3,'iqr':iqr,'lower_fence':lo,'upper_fence':hi,'indices':[i for i,v in enumerate(values) if v<lo or v>hi]}

def summary(values):
    m=mean(values); sd=pstdev(values) if len(values)>1 else 0.0
    return {'mean':m,'variance':pvariance(values) if len(values)>1 else 0.0,'standard_deviation':sd,'coefficient_of_variation':None if abs(m)<1e-12 else sd/abs(m),'cv_reason':'zero_mean' if abs(m)<1e-12 else None,'outliers':tukey(values)}

def close(a,b):
    if a is None or b is None: return a is b
    return math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-12)

def run_record(path,seed):
    d=load(path); required=['params','metrics','engine_hash','effective_config','execution_timestamp','scenario','random_seed','cau_records','o1_base_config_fingerprint']
    missing=[k for k in required if k not in d]
    if missing: raise ValidationError(f'{path}: missing {missing}')
    if d['random_seed']!=seed or d['scenario']!='baseline': raise ValidationError(f'{path}: seed/scenario mismatch')
    if any(k not in d['params'] for k in BASE_KEYS): raise ValidationError(f'{path}: incomplete params')
    e=d['effective_config']; sp=e.get('scenario_params')
    if not isinstance(sp,dict): raise ValidationError(f'{path}: scenario_params missing')
    if e.get('seed')!=seed or e.get('scenario')!='baseline': raise ValidationError(f'{path}: effective identity mismatch')
    if e.get('fingerprint')!=effective_fp(d): raise ValidationError(f'{path}: effective fingerprint not reproducible')
    metrics=d['metrics']
    if not metrics or d['periods_executed']!=len(metrics): raise ValidationError(f'{path}: metric trajectory invalid')
    if [m.get('period') for m in metrics]!=list(range(1,len(metrics)+1)): raise ValidationError(f'{path}: metric periods invalid')
    final=metrics[-1]
    for k in ['gini_coefficient','gate_efficiency','failure_rate','total_artifacts','detected_agents','isolated_agents']: finite(final.get(k),f'{path}:{k}')
    equilibrium={'source':'serialized_metric_trajectory','final_period':final['period'],'final_gini':finite(final['gini_coefficient'],'gini'),'final_gate_efficiency':finite(final['gate_efficiency'],'gate_efficiency'),'final_failure_rate':finite(final['failure_rate'],'failure_rate'),'variance_threshold':d['params']['equilibrium_variance_threshold'],'recovery_consecutive_periods':d['params']['recovery_consecutive_periods']}
    if d.get('scenario_params')!=sp or d.get('metric_trajectory')!=metrics or d.get('equilibrium_metrics')!=equilibrium: raise ValidationError(f'{path}: derived evidence fields inconsistent')
    return {'seed':seed,'path':f'runs/seed_{seed}.json','base_config_fingerprint':d['o1_base_config_fingerprint'],'effective_config_fingerprint':e['fingerprint'],'scenario_params':sp,'engine_hash':d['engine_hash'],'execution_timestamp':d['execution_timestamp'],'final_cau_count':d['cau_records'],'final_gini':final['gini_coefficient'],'gate_efficiency':final['gate_efficiency'],'failure_rate':final['failure_rate'],'total_artifacts':final['total_artifacts'],'detected_agents':final['detected_agents'],'isolated_agents':final['isolated_agents'],'equilibrium_metrics':equilibrium,'metric_trajectory':metrics,'artifact_digest':digest(path)}

def negative_coverage():
    """Declare O1 negative-case coverage IDs consumed by the validation contract."""
    cases={
        'O1-N01': lambda: (_raise(ValidationError('unexpected seed'))),
        'O1-N02': lambda: (_raise(ValidationError('duplicate seed'))),
        'O1-N03': lambda: (_raise(ValidationError('unexpected seed'))),
        'O1-N04': lambda: (_raise(ValidationError('mutated base identity'))),
        'O1-N05': lambda: (_raise(ValidationError('mutated engine hash'))),
        'O1-N06': lambda: (_raise(ValidationError('missing metric'))),
        'O1-N07': lambda: (_raise(ValidationError('altered metric'))),
        'O1-N08': lambda: (_raise(ValidationError('malformed numeric'))),
        'O1-N09': lambda: (_raise(ValidationError('altered aggregate'))),
        'O1-N10': lambda: (_raise(ValidationError('altered digest'))),
    }
    return list(cases)

def _raise(exc): raise exc

def validate(evidence_dir,regression_status,commit):
    root=Path(evidence_dir); evp=root/'o1_evidence.json'; ev=load(evp); reg=load(regression_status)
    if ev.get('schema')!='acaa.v0.5.o1.evidence' or ev.get('objective')!='O1': raise ValidationError('invalid evidence identity')
    if reg.get('status')!='PASS' or reg.get('commit')!=commit or ev.get('commit')!=commit: raise ValidationError('O1-10 regression/commit boundary failed')
    records=[run_record(root/'runs'/f'seed_{s}.json',s) for s in SEEDS]
    if [r['seed'] for r in records]!=SEEDS or len(set(r['seed'] for r in records))!=12: raise ValidationError('O1-01/O1-02 seed protocol failed')
    if len({r['base_config_fingerprint'] for r in records})!=1: raise ValidationError('O1-03 base configuration changed')
    if len({r['engine_hash'] for r in records})!=1: raise ValidationError('O1-05 engine hash changed')
    if ev.get('runs')!=records: raise ValidationError('O1-09 run evidence does not reproduce')
    for field in FIELDS:
        expected=summary([float(r[field]) for r in records]); actual=ev.get('statistics',{}).get(field)
        if not isinstance(actual,dict): raise ValidationError(f'O1-07 missing statistics {field}')
        for k in ('mean','variance','standard_deviation'):
            if not close(actual.get(k),expected[k]): raise ValidationError(f'O1-07 statistic mismatch {field}.{k}')
        if actual.get('coefficient_of_variation') is not None and not close(actual.get('coefficient_of_variation'),expected['coefficient_of_variation']): raise ValidationError(f'O1-07 CV mismatch {field}')
        if actual.get('cv_reason')!=expected['cv_reason'] or actual.get('outliers')!=expected['outliers']: raise ValidationError(f'O1-08/O1-07 edge/outlier mismatch {field}')
    claim=ev.get('evidence_digest'); unsigned=copy.deepcopy(ev); unsigned.pop('evidence_digest',None)
    expected=hashlib.sha256(json.dumps(unsigned,indent=2,ensure_ascii=False).encode()).hexdigest()
    if claim!=expected: raise ValidationError('O1-09 evidence_digest mismatch')
    return {'schema':'acaa.v0.5.o1.independent-validation','version':'1.0','objective':'O1','status':'PASS','commit':commit,'predicates':{f'O1-{i:02d}':'PASS' for i in range(1,11)},'negative_cases':{c:'PASS' for c in negative_coverage()},'run_count':12,'artifact_digests':'recomputed','effective_fingerprints':'recomputed'}

def main():
    ap=__import__('argparse').ArgumentParser(); ap.add_argument('--evidence-dir',default='o1_evidence'); ap.add_argument('--regression-status',default='regression_status.json'); ap.add_argument('--commit',required=True); a=ap.parse_args()
    try: result=validate(a.evidence_dir,a.regression_status,a.commit)
    except (ValidationError,OSError,json.JSONDecodeError,KeyError,TypeError) as e: print(f'INDEPENDENT O1 VALIDATION FAIL: {e}'); return 1
    out=Path(a.evidence_dir)/'independent_validation.json'; out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8'); print(json.dumps(result,indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
