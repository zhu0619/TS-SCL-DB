#load_data.py

import csv
import os
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import requests

#disable warnings of request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
import gc
import mygene
mg = mygene.MyGeneInfo()

from ts_scl_db.models import *

TAGSERVER_API = 'https://tagging.markovchain.de'
#TAGSERVER_AUTH = None # for unauthenticated endpoints
TAGSERVER_AUTH = ('ubi', 'cl2p3qv7Q')
TAGSERVER_SSLVERIFY = False # in case ssl verification fails


def load_kd_data():
	##==========================#
	##Tissue_triple_relation	#
	##==========================#
	# Tissue_triple_relation.objects.all().delete()

	# with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-24_a_0.8_ws_3_wa_0.2_human copy.csv') as csvfile:
	with open('ts_scl_db/raw_data/benchmark170.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')
	# with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_CellLine_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv') as csvfile:
	# 	reader = csv.DictReader(csvfile)
		# import entrez
		entrez_ids = [int(row['ENTREZ']) for row in reader]
		import_genes(entrez_ids)
	with open('ts_scl_db/raw_data/benchmark170.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')
		for row in reader:
			print(row)
			bto_obj = Tissue.objects.get(BTO_id=row['BTO'])
			go_obj = SCLocalization.objects.get(GO_id=row['GO'])
			source_obj = Data_source.objects.get(source = "Knowledge")
			try:
				protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
				try:
					t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = 9999,source = source_obj)
					print('exists!')
				except Tissue_triple_relation.DoesNotExist:
					t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = 9999,source = source_obj, review = "Yes")
					t.save()
					print('new!')
					try:
						pmid_obj = PubMed_entry.objects.get(pmid=row['PMID'])
					except PubMed_entry.DoesNotExist:
						# check if pub annotation exists
						annotation  = load_json(row['PMID'])
						pmid_obj = import_annotation(annotation)
					try: 
						Tissue_triple_relation_pmid.objects.get(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
						print("triplet exists!")
					except Tissue_triple_relation_pmid.DoesNotExist:
						tp = Tissue_triple_relation_pmid(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
						tp.save()
			except Gene_Protein.DoesNotExist:
				pass

def load_json(pmid):
	# json_dir = "/Users/zhulu/Desktop/Lu_work/text-mining-project/Frank_API/New_experiments_17_11/json_1511"
	"""saves the results from the server to json files, but only if a json file for a specific pmid doesn't exist"""
	# for pmid in pmid_list:
		#check if file already exists:
	response_data=request_tagged(pmid)
	return response_data
						
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
		print('OK!',pmid)
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
		try:
			p = PubAnnotation.objects.get(pmid = pmid)
		except PubAnnotation.DoesNotExist:
			p = PubAnnotation(annotaion = annotaions ,pmid = pmid )
			p.save()
		try:
			q = PubTokens.objects.get(pmid = pmid )
		except PubTokens.DoesNotExist:
			q = PubTokens(tokens = tokens,pmid = pmid )
			q.save()
		try:
			o = PubFulltext.objects.get(pmid = pmid)
		except PubFulltext.DoesNotExist:
			o = PubFulltext(fulltext = fulltext,pmid = pmid  )
			o.save()
		try:
			r = Relation_Pub_Anno.objects.get(pmid = pmid)
		except Relation_Pub_Anno.DoesNotExist:
			r = Relation_Pub_Anno(id_pub_anno = p, id_pub_token= q,id_pub_fulltext=o, pmid = pmid)
			r.save()	
		l = PubMed_entry(pmid = pmid,id_Pub_Anno= r)
		l.save()
		return l
	else:
		print('No annotation !' )
		return None

def import_genes(sp_genes):
	entrezgene_list = list(Gene_Protein.objects.values_list('EntrezID', flat=True))
	genes = list(set(sp_genes).difference(set(entrezgene_list)))
	if len(genes) >0:
		data = mg.getgenes(genes,fields="entrezgene,ensemblgene,uniprot,symbol,name",species=9606)
		for datum in data:
			try:
				if 'notfound' not in datum.keys():
					print(datum['entrezgene'])
					entrez_id = datum['entrezgene']
					if 'uniprot' in datum.keys():
						uniprot = datum['uniprot']
						if uniprot and 'Swiss-Prot' in uniprot.keys():
							uniprot_acc = uniprot['Swiss-Prot']
						elif 'TrEMBL' in uniprot.keys():
							uniprot_acc = uniprot['TrEMBL']
						if type(uniprot_acc) == list:
							uniprot_acc = ';'.join(uniprot_acc)
					else:
						uniprot_acc = 'None'
					gene_name = datum['name']
					gene_symbol =  datum['symbol']
					# entrezgene_list = list(Gene_Protein.objects.values_list('EntrezID', flat=True))
					# if entrez_id not in entrezgene_list :
					try:
						g = Gene_Protein.objects.get(EntrezID = entrez_id, UniprotACC = uniprot_acc ,GeneName = gene_name, GeneSymbol = gene_symbol  )
					except Gene_Protein.DoesNotExist:
						g = Gene_Protein(EntrezID = entrez_id, UniprotACC = uniprot_acc ,GeneName = gene_name, GeneSymbol = gene_symbol  )
						g.save()
						print('ok!')
			except IntegrityError as e:
				raise e

load_kd_data()
# if __name__== "__main__":
	# main()
