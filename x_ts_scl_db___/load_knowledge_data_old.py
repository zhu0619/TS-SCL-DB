#load_data.py

import csv
import os
from django.core.exceptions import ObjectDoesNotExist
import requests

#disable warnings of request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
import gc


from django.db import IntegrityError
import mygene
mg = mygene.MyGeneInfo()

from ts_scl_db.models import *


TAGSERVER_API = 'https://tagging.markovchain.de'
#TAGSERVER_AUTH = None # for unauthenticated endpoints
TAGSERVER_AUTH = ('ubi', 'cl2p3qv7Q')
TAGSERVER_SSLVERIFY = False # in case ssl verification fails
json_dir = "/Users/zhulu/Desktop/Lu_work/text-mining-project/Frank_API/New_experiments_17_11/json_1511"


with open('ts_scl_db/raw_data/benchmark170.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	ensg_id = list(set([x['ENTREZ'] for x in reader ]))
	data = mg.getgenes(ensg_id,fields="entrezgene,ensemblgene,uniprot,'symbol', 'name'",species=9606)
	import_protein(data)
csvfile.close()


# # load more pmid
# with open('ts_scl_db/raw_data/benchmark170.csv') as csvfile:
# 	reader = csv.DictReader(csvfile, delimiter=';')
# 	pmid_id = list(set([x['PMID'] for x in reader ]))
# 	save_to_json(pmid_id)
# csvfile.close()



with open('ts_scl_db/raw_data/benchmark170.csv') as csvfile:
	reader = csv.DictReader(csvfile,delimiter=";")
	for row in reader:
		print(row)
		bto_obj = Tissue.objects.get(BTO_id=row['BTO'])
		protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
		go_obj = SCLocalization.objects.get(GO_id=row['GO'])
		source_obj = Data_source.objects.get(source = "Knowledge")

		try:
			t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = 9999,source = source_obj)
			print('exists!')
		except ObjectDoesNotExist:
			t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = 9999,source = source_obj, review = "Yes")
			t.save()
			print('new!')

		try:
			pmid_obj = PubMed_entry.objects.get(pmid=row['PMID'])
		except ObjectDoesNotExist:
			# check if pub annotation exists
			annotation  = load_json(row['PMID'])
			pmid_obj = import_annotation(annotation)

		tp = Tissue_triple_relation_pmid(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
		tp.save()
	csvfile.close()

# protein_obj = Gene_Protein.objects.get(EntrezID='13982')



def load_json(pmid):
	json_dir = "/Users/zhulu/Desktop/Lu_work/text-mining-project/Frank_API/New_experiments_17_11/json_1511"
	"""saves the results from the server to json files, but only if a json file for a specific pmid doesn't exist"""
	# for pmid in pmid_list:
		#check if file already exists
	if not os.path.isfile(json_dir + "/{}.json".format(pmid)):
		response_data=request_tagged(pmid)
		if response_data:
			with open(json_dir+"/{}.json".format(pmid), 'w') as outfile:
				json.dump(response_data,outfile)
			gc.collect()
	else:
		save_to_json(pmid)
		print('new pmid')
		with open(json_dir+"/{}.json".format(pmid), 'r') as outfile:
				response_data = json.load(outfile)
	return response_data


def save_to_json(pmid_list):
    """saves the results from the server to json files, but only if a json file for a specific pmid doesn't exist"""
    for pmid in pmid_list:
            #check if file already exists
            if not os.path.isfile("json/{}.json".format(pmid)):
                response_data=request_tagged(pmid)
                if response_data:
                    with open("json/{}.json".format(pmid), 'w') as outfile:
                        json.dump(response_data,outfile)

def request_tagged(pmid):
	"""download json files from specified server"""
	#pmid = unicode(pmid)
#	logging.debug('Requesting tagged text for pmid #%s' % pmid)
	print('Requesting tagged text for pmid {}'.format(pmid))
	uri = TAGSERVER_API + '/tags/%s/' % pmid
	r = None
	if TAGSERVER_AUTH is None:
		r = requests.get(uri, verify=TAGSERVER_SSLVERIFY)
	else:
		r = requests.get(uri, auth=TAGSERVER_AUTH, verify=TAGSERVER_SSLVERIFY)
	#logging.debug('Request to %s returned status %s' % (uri, r.status_code))
	
	if r.status_code == 200:
		print('OK! '.format(pmid))
		return r.json()
	else:
		print("Failed to get json for {}".format(pmid))
		return None

def import_annotation(reader):
	if reader['hits'] == 1:			
		results = reader['results']
		taggers = list(results.values())[0]
		pmid = int(taggers['pmid'])
		fulltext = taggers['fulltext']
		annotaions  = taggers['annotations']
		tokens = taggers['tokenized']
		
		p = PubAnnotation(annotaion = annotaions ,pmid = pmid )
		p.save()

		q = PubTokens(tokens = tokens,pmid = pmid )
		q.save()

		o = PubFulltext(fulltext = fulltext,pmid = pmid  )
		o.save()

		r = Relation_Pub_Anno(id_pub_anno = p, id_pub_token= q,id_pub_fulltext=o, pmid = pmid)
		r.save()
		
		l = PubMed_entry(pmid = pmid,id_Pub_Anno= r)
		l.save()
		return l
	else:
		print('No annotation !' )
		return None	



def import_protein(data):
	entrezgene_list = list(Gene_Protein.objects.values_list('EntrezID', flat=True))
	for datum in data: 
		try:
			if 'notfound' not in datum.keys() and 'entrezgene' in datum.keys():
				entrez_id = datum['entrezgene']
				if 'uniprot' in datum.keys():
					uniprot = datum['uniprot']
					if uniprot and 'Swiss-Prot' in uniprot.keys():
						uniprot_acc = uniprot['Swiss-Prot']
					elif 'TrEMBL' in uniprot.keys():
						uniprot_acc = uniprot['TrEMBL']
					if type(uniprot_acc) == list:
						uniprot_acc = ';'.join(uniprot_acc)
				gene_name = datum['name']
				gene_symbol =  datum['symbol']
				if entrez_id not in entrezgene_list :
					try:
						g = Gene_Protein(EntrezID = entrez_id, UniprotACC = uniprot_acc ,GeneName = gene_name, GeneSymbol = gene_symbol  )
						g.save()
					except IntegrityError as e: 
						if 'unique constraint' in e.message:
							pass
		except IntegrityError as e:
			raise e		



