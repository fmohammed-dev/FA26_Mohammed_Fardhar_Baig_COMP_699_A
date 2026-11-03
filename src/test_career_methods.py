import unittest,math
from career_methods import components,structured_score,ordered,precision_at_k,ndcg_at_k,normalize,validate_inputs
class MethodTests(unittest.TestCase):
    def setUp(self):
        self.p={'student_id':'S','field':'cs','skills':['Python',' SQL '],'preferred_type':'internship','preferred_modes':['remote']}
        self.o={'opportunity_id':'O','title':'Role','required_skills':['python','git'],'accepted_fields':['cs'],'type':'internship','mode':'remote'}
        self.weights={'skill_weight':.6,'field_weight':.25,'preference_weight':.15}
    def test_normalization(self):self.assertEqual(normalize([' SQL ','sql','']),{'sql'})
    def test_partial_coverage(self):self.assertEqual(components(self.p,self.o)['skill_coverage'],.5)
    def test_score_known(self):self.assertAlmostEqual(structured_score(components(self.p,self.o),self.weights),.7)
    def test_preferences_half(self):self.o['mode']='onsite';self.assertEqual(components(self.p,self.o)['preference_match'],.5)
    def test_no_skills(self):self.p['skills']=[];self.assertEqual(components(self.p,self.o)['skill_coverage'],0)
    def test_empty_required_rejected(self):
        self.o['required_skills']=[]
        with self.assertRaises(ValueError):components(self.p,self.o)
    def test_bad_weights_rejected(self):
        with self.assertRaises(ValueError):structured_score(components(self.p,self.o),dict(self.weights,skill_weight=.9))
    def test_ties(self):self.assertEqual(ordered([{'opportunity_id':'B','s':1},{'opportunity_id':'A','s':1}],'s')[0]['opportunity_id'],'A')
    def test_precision_known(self):self.assertAlmostEqual(precision_at_k([2,0,1],3),2/3)
    def test_ndcg_perfect(self):self.assertEqual(ndcg_at_k([2,1,0],3),1)
    def test_ndcg_zero(self):self.assertEqual(ndcg_at_k([0,0,0],3),0)
    def test_ndcg_hand_calculation(self):self.assertAlmostEqual(ndcg_at_k([0,2,1],3),(3/math.log2(3)+.5)/(3+1/math.log2(3)))
    def test_invalid_k(self):
        with self.assertRaises(ValueError):precision_at_k([1],3)
    def test_label_grid_rejected(self):
        with self.assertRaises(ValueError):validate_inputs([self.p],[self.o],[])
if __name__=='__main__':unittest.main()
