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





##==========================#
##Tissue_triple_relation	#
##==========================#
# Tissue_triple_relation.objects.all().delete()

# with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-24_a_0.8_ws_3_wa_0.2_human copy.csv') as csvfile:

# def main():

with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_CellLine_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
# with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_CellLine_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv') as csvfile:
# 	reader = csv.DictReader(csvfile)
	# import entrez
	entrez_ids = [int(row['ENTREZ']) for row in reader]
	fold = round(len(entrez_ids)/1000)
	for i in range(53,fold):
		start = i*1000
		if i == fold-1:
			stop = len(entrez_ids)-1
		else:
			stop = (i+1)*1000-1
		print(start,'-',stop)
		import_genes(entrez_ids[start:stop])

# with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_CellLine_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv') as csvfile:
# 	reader = csv.DictReader(csvfile, delimiter=',')
# 	for row in reader:
# 		print(row)
# 		bto_obj = Tissue.objects.get(BTO_id=row['BTO'])
# 		# protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
# 		go_obj = SCLocalization.objects.get(GO_id=row['GO'])
# 		source_obj = Data_source.objects.get(source = "Text-mining")
# 		if int(row['ENTREZ']) in Gene_Protein.objects.values_list('EntrezID',flat=True):
# 			protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
# 			print(row['ENTREZ'] , 'exists')
# 			try:
# 				t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = row['score'],source = source_obj)
# 				print('triplet exists!')
# 			except Tissue_triple_relation.DoesNotExist:
# 				t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = row['score'],source = source_obj)
# 				t.save()
# 				print('new triplet!')
# 				try:
# 				 PubMed_entry.objects.values_list('pmid',flat=True):
# 					pmid_obj = PubMed_entry.objects.get(pmid=row['PMID'])
# 					print('pmid exists!')	
# 				else:			
# 					# check if pub annotation exists
# 					annotation  = load_json(row['PMID'])
# 					reader = annotation
# 					pmid_obj = import_annotation(annotation)
# 					try: 
# 						tp = Tissue_triple_relation_pmid(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
# 						tp.save()
# 						print("new treiplet pmid")
# 					except IntegrityError:
# 						print("triplet pmid exists!")
# 		else:
# 			print(row['ENTREZ'] , 'not exist')
# 			pass

# Tissue_triple_relation.objects.all().delete()
with open('ts_scl_db/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_CellLine_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		print(row)
		bto_obj = Tissue.objects.get(BTO_id=row['BTO'])
		# protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
		go_obj = SCLocalization.objects.get(GO_id=row['GO'])
		source_obj = Data_source.objects.get(source = "Text-mining")
		try:
			protein_obj = Gene_Protein.objects.get(EntrezID=row['ENTREZ'])
			try:
				t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = row['score'],source = source_obj)
				print('Tissue_triple_relation exists!')
			except Tissue_triple_relation.DoesNotExist:
				t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,Zscore = row['score'],source = source_obj)
				t.save()
				print('Tissue_triple_relation new!')
				try:
					pmid_obj = PubMed_entry.objects.get(pmid=row['PMID'])
					print('PubMed_entry exists')
				except PubMed_entry.DoesNotExist:
					# check if pub annotation exists
					annotation  = load_json(row['PMID'])
					pmid_obj = import_annotation(annotation)
					print('PubMed_entry new')
				try: 
					Tissue_triple_relation_pmid.objects.get(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
					print("Tissue_triple_relation_pmid exists!")
				except Tissue_triple_relation_pmid.DoesNotExist:
					tp = Tissue_triple_relation_pmid(Tissue_triple_relation_id = t ,id_pmid = pmid_obj)
					tp.save()
					print('Tissue_triple_relation_pmid new!')
		except Gene_Protein.DoesNotExist:
			print('Gene_Protein does not exists')
			pass

# def load_json(pmid):
# 	json_dir = "/Users/zhulu/Desktop/Lu_work/text-mining-project/Frank_API/New_experiments_17_11/json_1511"
# 	"""saves the results from the server to json files, but only if a json file for a specific pmid doesn't exist"""
# 	# for pmid in pmid_list:
# 		#check if file already exists
# 	if not os.path.isfile(json_dir + "/{}.json".format(pmid)):
# 		response_data=request_tagged(pmid)
# 		if response_data:
# 			with open(json_dir+"/{}.json".format(pmid), 'w') as outfile:
# 				json.dump(response_data,outfile)
# 			gc.collect()
# 	else:
# 		with open(json_dir+"/{}.json".format(pmid), 'r') as outfile:
# 				response_data = json.load(outfile)
# 	return response_data
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
#########################		
# def import_annotation(reader):
# 	if reader['hits'] == 1:			
# 		results = reader['results']
# 		taggers = list(results.values())[0]
# 		pmid = int(taggers['pmid'])
# 		fulltext = taggers['fulltext']
# 		annotaions  = taggers['annotations']
# 		tokens = taggers['tokenized']		
# 		if pmid in PubAnnotation.objects.values_list('pmid',flat=True):
# 			p = PubAnnotation.objects.get(pmid = pmid)
# 		else:
# 			print('annotaions nb:',len(str(annotaions)))
# 			p = PubAnnotation(annotaion = annotaions ,pmid = pmid )
# 			p.save()
# 		if pmid in PubTokens.objects.values_list('pmid',flat=True):
# 			q = PubTokens.objects.get(pmid = pmid )
# 		else:
# 			print('PubTokens nb:',len(str(tokens)))
# 			q = PubTokens(tokens = tokens,pmid = pmid )
# 			q.save()
# 		if pmid in PubFulltext.objects.values_list('pmid',flat=True):
# 			o = PubFulltext.objects.get(pmid = pmid)
# 		else:
# 			print('PubFulltext nb:',len(str(fulltext)))
# 			o = PubFulltext(fulltext = fulltext,pmid = pmid  )
# 			o.save()
# 		if pmid in Relation_Pub_Anno.objects.values_list('pmid',flat=True) :
# 			r = Relation_Pub_Anno.objects.get(pmid = pmid)
# 		else:
# 			r = Relation_Pub_Anno(id_pub_anno = p, id_pub_token= q,id_pub_fulltext=o, pmid = pmid)
# 			r.save()
# 		l = PubMed_entry(pmid = pmid,id_Pub_Anno= r)
# 		l.save()
# 		return l
# 	else:
# 		print('No annotation !' )
# 		return None
#########################	
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
					except ObjectDoesNotExist:
						g = Gene_Protein(EntrezID = entrez_id, UniprotACC = uniprot_acc ,GeneName = gene_name, GeneSymbol = gene_symbol  )
						g.save()
						print('ok!')
			except IntegrityError as e:
				raise e
		
if __name__ == '__main__':
	main()