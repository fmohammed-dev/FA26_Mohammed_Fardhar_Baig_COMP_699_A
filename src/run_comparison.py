"""Week 2: compare fixed structured scoring with a skill-only reference."""
from pathlib import Path
import json,hashlib,platform,importlib.metadata,math
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from career_methods import validate_inputs,components,structured_score,ordered,precision_at_k,ndcg_at_k
ROOT=Path(__file__).resolve().parents[1]
def run():
    D=ROOT/'data/synthetic';O=ROOT/'results/week_2';O.mkdir(parents=True,exist_ok=True)
    protocol_bytes=(ROOT/'src/protocol.json').read_bytes();P=json.loads(protocol_bytes)
    profiles=json.loads((D/'profiles.json').read_text());opportunities=json.loads((D/'opportunities.json').read_text());labels=json.loads((D/'relevance.json').read_text());manifest=json.loads((D/'manifest.json').read_text())
    for name,h in manifest['sha256'].items():
        if hashlib.sha256((D/name).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed: '+name)
    checks=validate_inputs(profiles,opportunities,labels);checks['input_digests_match']=True
    grades={(r['student_id'],r['opportunity_id']):r['grade'] for r in labels}
    scores=[];ranks=[];metric_rows=[]
    for p in profiles:
        candidates=[]
        for o in opportunities:
            parts=components(p,o)
            candidates.append({'student_id':p['student_id'],'opportunity_id':o['opportunity_id'],**parts,'skill_only':parts['skill_coverage'],'structured':structured_score(parts,P)})
        scores.extend(candidates)
        for method in ['skill_only','structured']:
            ranked=ordered(candidates,method);g=[grades[p['student_id'],r['opportunity_id']] for r in ranked]
            for rank,r in enumerate(ranked,1):ranks.append({'student_id':p['student_id'],'method':method,'opportunity_id':r['opportunity_id'],'rank':rank,'score':r[method],'grade':g[rank-1]})
            metric_rows.append({'student_id':p['student_id'],'method':method,'precision_at_3':precision_at_k(g,P['k']),'ndcg_at_3':ndcg_at_k(g,P['k'])})
    score_table=pd.DataFrame(scores);ranking_table=pd.DataFrame(ranks);metrics=pd.DataFrame(metric_rows)
    aggregate=metrics.groupby('method')[['precision_at_3','ndcg_at_3']].mean().reset_index()
    checks['all_scores_finite_and_bounded']=bool(score_table[['skill_only','structured']].map(lambda x:math.isfinite(x) and 0<=x<=1).all().all())
    checks['two_full_rankings_per_profile']=len(ranks)==2*len(labels)
    checks['grades_unchanged_during_execution']=hashlib.sha256((D/'relevance.json').read_bytes()).hexdigest()==manifest['sha256']['relevance.json']
    checks['protocol_unchanged_during_execution']=(ROOT/'src/protocol.json').read_bytes()==protocol_bytes
    assert all(checks.values())
    for name,frame in [('score_components',score_table),('rankings',ranking_table),('metrics_by_student',metrics),('metrics_summary',aggregate)]:frame.to_csv(O/(name+'.csv'),index=False)
    pd.DataFrame([{'check':k,'passed':v} for k,v in checks.items()]).to_csv(O/'validation_checks.csv',index=False)
    ranking_table[ranking_table['rank']<=3].to_csv(O/'top3_recommendations.csv',index=False)
    paired=metrics.pivot(index='student_id',columns='method',values=['precision_at_3','ndcg_at_3']);paired.columns=['_'.join(c) for c in paired.columns]
    for metric in ['precision_at_3','ndcg_at_3']:paired[metric+'_delta']=paired[metric+'_structured']-paired[metric+'_skill_only']
    paired.to_csv(O/'paired_differences.csv')
    fig,ax=plt.subplots(figsize=(7,3.6));wide=metrics.pivot(index='student_id',columns='method',values='ndcg_at_3');wide.plot.bar(ax=ax,color=['#9AA8B5','#235789']);ax.set_ylim(0,1.05);ax.set(ylabel='NDCG@3',xlabel='Synthetic student scenario',title='Initial structured ranking comparison');ax.legend(['Skill only','Structured'],loc='lower right');fig.tight_layout();fig.savefig(O/'ndcg_by_student.png',dpi=160);plt.close(fig)
    summary={'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas','matplotlib']},'profiles':len(profiles),'opportunities':len(opportunities),'pairs':len(labels),'protocol':P,'protocol_sha256':hashlib.sha256(protocol_bytes).hexdigest(),'input_hashes':manifest['sha256'],'validation_checks_passed':len(checks),'training':'none','randomness':'none','independent_annotations':False}
    (O/'execution_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(aggregate.to_string(index=False));print('\nPer-scenario differences:\n'+paired.to_string());return aggregate
if __name__=='__main__':run()
