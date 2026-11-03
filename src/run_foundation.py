"""Week 1: input validation and descriptive evidence, without comparative results."""
from pathlib import Path
import json,hashlib,platform,importlib.metadata
import pandas as pd
from career_methods import validate_inputs
ROOT=Path(__file__).resolve().parents[1]
def run():
    D=ROOT/'data/synthetic';O=ROOT/'results/week_1';O.mkdir(parents=True,exist_ok=True)
    profiles=json.loads((D/'profiles.json').read_text());opportunities=json.loads((D/'opportunities.json').read_text());labels=json.loads((D/'relevance.json').read_text())
    manifest=json.loads((D/'manifest.json').read_text())
    for n,h in manifest['sha256'].items():
        if hashlib.sha256((D/n).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed: '+n)
    checks=validate_inputs(profiles,opportunities,labels);checks['input_digests_match']=True
    pd.DataFrame([{'check':k,'passed':v} for k,v in checks.items()]).to_csv(O/'validation_checks.csv',index=False)
    pd.DataFrame([{'student_id':p['student_id'],'field':p['field'],'skills':len(p['skills']),'preferred_type':p['preferred_type'],'preferred_modes':'|'.join(p['preferred_modes'])} for p in profiles]).to_csv(O/'profile_summary.csv',index=False)
    pd.DataFrame([{'opportunity_id':o['opportunity_id'],'title':o['title'],'required_skills':'|'.join(o['required_skills']),'accepted_fields':'|'.join(o['accepted_fields']),'type':o['type'],'mode':o['mode']} for o in opportunities]).to_csv(O/'opportunity_summary.csv',index=False)
    pd.DataFrame(labels).groupby(['student_id','grade']).size().unstack(fill_value=0).to_csv(O/'grade_distribution.csv')
    summary={'profiles':len(profiles),'opportunities':len(opportunities),'pairs':len(labels),'fields':len({p['field'] for p in profiles}),'checks_passed':len(checks),'comparative_experiment_executed':False,'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas']},'input_hashes':manifest['sha256']}
    (O/'execution_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':run()
