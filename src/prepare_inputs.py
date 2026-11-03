"""Create small, fixed synthetic scenarios without consulting ranker outputs."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/synthetic'
def generate():
    D.mkdir(parents=True,exist_ok=True)
    profiles=[
    {'student_id':'S01','field':'data_science','skills':['python','sql','statistics','tableau'],'preferred_type':'full_time','preferred_modes':['remote','hybrid']},
    {'student_id':'S02','field':'computer_science','skills':['python','java','git','sql'],'preferred_type':'internship','preferred_modes':['remote']},
    {'student_id':'S03','field':'business_analytics','skills':['sql','excel','powerbi','python'],'preferred_type':'full_time','preferred_modes':['onsite','hybrid']},
    {'student_id':'S04','field':'cybersecurity','skills':['networking','linux','python','security'],'preferred_type':'internship','preferred_modes':['hybrid','remote']},
    {'student_id':'S05','field':'health_informatics','skills':['sql','excel','healthcare','python'],'preferred_type':'full_time','preferred_modes':['remote','hybrid']},
    {'student_id':'S06','field':'finance','skills':['excel','statistics','sql','python'],'preferred_type':'internship','preferred_modes':['remote']}]
    raw=[
    ('O01','Data analyst',['sql','tableau'],['data_science','business_analytics'],'full_time','hybrid'),
    ('O02','Data science intern',['python','statistics'],['data_science','computer_science'],'internship','onsite'),
    ('O03','Backend developer',['python','git'],['computer_science'],'full_time','onsite'),
    ('O04','Software engineering intern',['java','git'],['computer_science'],'internship','remote'),
    ('O05','Business analyst',['excel','requirements'],['business_analytics','computer_science'],'full_time','hybrid'),
    ('O06','Reporting analyst',['sql','powerbi'],['business_analytics','data_science'],'full_time','onsite'),
    ('O07','Security analyst',['linux','security'],['cybersecurity'],'full_time','onsite'),
    ('O08','Security intern',['networking','security'],['cybersecurity'],'internship','hybrid'),
    ('O09','Clinical data analyst',['sql','healthcare'],['health_informatics','data_science'],'full_time','hybrid'),
    ('O10','Health data intern',['excel','healthcare'],['health_informatics'],'internship','onsite'),
    ('O11','Risk analyst',['statistics','excel'],['finance','business_analytics'],'full_time','onsite'),
    ('O12','Finance intern',['excel','sql'],['finance'],'internship','remote')]
    opportunities=[dict(zip(['opportunity_id','title','required_skills','accepted_fields','type','mode'],r)) for r in raw]
    # Pairwise grades are specified before any scoring function is called.
    grades={
    'S01':[2,1,0,0,0,1,0,0,1,0,1,0],
    'S02':[1,0,1,2,0,0,0,0,0,0,0,0],
    'S03':[1,0,0,0,1,2,0,0,0,0,1,1],
    'S04':[0,0,1,0,0,0,1,2,0,0,0,0],
    'S05':[1,0,0,0,1,1,0,0,2,1,0,0],
    'S06':[0,1,0,0,1,1,0,0,0,0,1,2]}
    explanations={
    'S01':{'O01':'Direct analyst role with SQL/Tableau and preferred full-time hybrid context','O02':'Strong technical overlap but internship/onsite conflicts with stated preferences','O06':'Transferable SQL/data background, missing Power BI','O09':'Transferable SQL but no healthcare skill','O11':'Statistics transfers, but Excel and finance context are limited'},
    'S02':{'O01':'Partial SQL fit, missing Tableau and intended analyst specialization','O03':'Direct software skill fit but full-time onsite conflicts with preferences','O04':'Direct Java/Git fit and preferred remote internship'},
    'S03':{'O01':'Transferable SQL/analytics fit, missing Tableau','O05':'Relevant field and Excel, missing requirements skill','O06':'Direct SQL/Power BI and preferred full-time onsite role','O11':'Partial Excel and business fit, missing statistics','O12':'Useful reporting skills, but finance specialization and internship differ from target'},
    'S04':{'O03':'Python is transferable but Git and general software role remain gaps','O07':'Direct security skills but full-time onsite conflicts with internship preference','O08':'Direct networking/security and preferred hybrid internship'},
    'S05':{'O01':'Transferable SQL, missing Tableau','O05':'Excel is useful but requirements skill is absent','O06':'SQL reporting transfers but Power BI is absent','O09':'Direct healthcare/SQL and preferred full-time hybrid context','O10':'Domain and tools align but internship/onsite differ from preferences'},
    'S06':{'O02':'Python/statistics transfer but data-science context and onsite mode are limitations','O05':'Excel transfers but business requirements skill is absent','O06':'SQL reporting transfers but Power BI is absent','O11':'Direct quantitative tools and finance field but full-time onsite differs from preference','O12':'Direct Excel/SQL and preferred remote finance internship'}}
    labels=[{'student_id':sid,'opportunity_id':o['opportunity_id'],'grade':g,'rationale':explanations[sid].get(o['opportunity_id'],'No useful role/domain fit in this constructed scenario')} for sid,gs in grades.items() for o,g in zip(opportunities,gs)]
    for name,data in [('profiles.json',profiles),('opportunities.json',opportunities),('relevance.json',labels)]:
        (D/name).write_text(json.dumps(data,indent=2)+'\n')
    manifest={'provenance':'Manually authored fictional diagnostic cases; no real people or real vacancies. Grades are fixed before scoring and are not independently annotated.','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.glob('*.json')) if p.name!='manifest.json'}}
    (D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return profiles,opportunities,labels
if __name__=='__main__':
    p,o,l=generate();print('Prepared',len(p),'profiles,',len(o),'opportunities and',len(l),'graded pairs.')
