#load abstract 
import json
import os

from ts_scl_db.models import *

PubAnno_list = list(PubAnnotation.objects.values_list('pmid', flat=True))
PubTokens_list = list(PubTokens.objects.values_list('pmid', flat=True))
PubFulltext_list = list(PubFulltext.objects.values_list('pmid', flat=True))
Relation_Pub_Anno_list = list(Relation_Pub_Anno.objects.values_list('pmid', flat=True))
PubMed_entry_list = list(PubMed_entry.objects.values_list('pmid', flat=True))


# list of json id
jsdir = '/Users/zhulu/Desktop/Lu_work/text-mining-project/Frank_API/New_experiments_17_11/json_1511/'
# dirlist = os.listdir('ts_scl_db/json/')
dirlist = os.listdir(jsdir)

for js in dirlist:
	if '.json' in js:
		with open(jsdir+ js) as jsonfile:
			reader = json.load(jsonfile)
			if reader['hits'] == 1:			
				results = reader['results']
				taggers = list(results.values())[0]
				pmid = int(taggers['pmid'])
				fulltext = taggers['fulltext']
				annotaions  = taggers['annotations']
				tokens = taggers['tokenized']

				if pmid not in PubAnno_list:			
					p = PubAnnotation(annotaion = annotaions ,pmid = pmid )
					p.save()
				else:
					p = PubAnnotation.objects.get(pmid = pmid)

				if pmid not in PubTokens_list:
					q = PubTokens(tokens = tokens,pmid = pmid )
					q.save()
				else:
					q = PubTokens.objects.get(pmid = pmid)

				if pmid not in PubFulltext_list:
					o = PubFulltext(fulltext = fulltext,pmid = pmid  )
					o.save()
				else:
					o = PubFulltext.objects.get(pmid = pmid)

				if pmid not in Relation_Pub_Anno_list:
					r = Relation_Pub_Anno(id_pub_anno = p, id_pub_token= q,id_pub_fulltext=o, pmid = pmid)
					r.save()
				else:
					r  = Relation_Pub_Anno.objects.get(pmid = pmid)
				
				if pmid not in PubMed_entry_list:
					l = PubMed_entry(pmid = pmid,id_Pub_Anno= r)
					l.save()



