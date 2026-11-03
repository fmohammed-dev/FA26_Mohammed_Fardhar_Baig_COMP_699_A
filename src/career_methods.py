"""Inspectable structured matching; labels never enter the scoring functions."""
import math

def normalize(values):
    return {v.strip().lower() for v in values if isinstance(v,str) and v.strip()}

def components(profile,opportunity):
    needed=normalize(opportunity['required_skills'])
    if not needed:raise ValueError('At least one required skill is needed')
    coverage=len(normalize(profile['skills']) & needed)/len(needed)
    field=float(profile['field'].strip().lower() in normalize(opportunity['accepted_fields']))
    kind=float(profile['preferred_type']==opportunity['type'])
    mode=float(opportunity['mode'] in profile['preferred_modes'])
    return {'skill_coverage':coverage,'field_match':field,'type_match':kind,'mode_match':mode,'preference_match':(kind+mode)/2}

def structured_score(parts,protocol):
    weights=[protocol[k] for k in ['skill_weight','field_weight','preference_weight']]
    if any(w<0 for w in weights) or not math.isclose(sum(weights),1):raise ValueError('Weights must be nonnegative and sum to one')
    return weights[0]*parts['skill_coverage']+weights[1]*parts['field_match']+weights[2]*parts['preference_match']

def ordered(rows,score):
    return sorted(rows,key=lambda r:(-r[score],r['opportunity_id']))

def precision_at_k(grades,k):
    if k<1 or len(grades)<k:raise ValueError('Invalid k')
    return sum(g>=1 for g in grades[:k])/k

def ndcg_at_k(grades,k):
    if k<1 or len(grades)<k:raise ValueError('Invalid k')
    def dcg(gs):return sum((2**g-1)/math.log2(i+2) for i,g in enumerate(gs[:k]))
    ideal=dcg(sorted(grades,reverse=True))
    return dcg(grades)/ideal if ideal else 0.0

def validate_inputs(profiles,opportunities,labels):
    ps={p['student_id'] for p in profiles};os={o['opportunity_id'] for o in opportunities}
    pairs=[(r['student_id'],r['opportunity_id']) for r in labels]
    checks={'unique_student_ids':len(ps)==len(profiles),'unique_opportunity_ids':len(os)==len(opportunities),'unique_labeled_pairs':len(set(pairs))==len(pairs),'complete_pair_grid':set(pairs)=={(p,o) for p in ps for o in os},'valid_relevance_grades':all(type(r['grade']) is int and r['grade'] in {0,1,2} for r in labels),'required_profile_fields':all(isinstance(p.get('skills'),list) and all(p.get(k) for k in ['student_id','field','preferred_type','preferred_modes']) for p in profiles),'required_opportunity_fields':all(normalize(o.get('required_skills',[])) and all(o.get(k) for k in ['opportunity_id','title','accepted_fields','type','mode']) for o in opportunities),'pair_rationales_present':all(r.get('rationale','').strip() for r in labels)}
    if not all(checks.values()):raise ValueError(checks)
    return checks
