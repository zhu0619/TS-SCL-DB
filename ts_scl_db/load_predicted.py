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

from polls.models import *

##==========================#
##Tissue_triple_relation	#
##==========================#
# Tissue_triple_relation.objects.all().delete()

# gene 
with open('polls/raw_data/Predicted.protein.tissue.scl.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	ensg_id = list(set([x['EntrezID'] for x in reader ]))
	data = mg.getgenes(ensg_id,fields="entrezgene,ensemblgene,uniprot,'symbol', 'name'",species=9606)
	import_protein(data)

# go
# with open("polls/raw_data/SCL_mapping_table.csv") as csvfile:
# 	go_map_reader = csv.DictReader(csvfile, delimiter=';')
# 	go_map = {}
# 	for row in go_map_reader:
# 	   go_map[row['HPA SCL']] = row['HPA SCL GO']
# csvfile.close()
# with open('polls/raw_data/aal3321_Thul_SM_table_S7.txt') as csvfile:
# 	reader = csv.DictReader(csvfile, delimiter='\t')
# 	import_go(reader)
# csvfile.close()

# with open('polls/raw_data/Goal_cell_line.csv') as csvfile:
# 	map_reader = csv.DictReader(csvfile, delimiter=';')
# 	bto_map = {}
# 	for row in map_reader:
# 	   bto_map[row['CellLine']] = row['BTO']
# csvfile.close()
# # bto
# import_bto()


# HPA triplet
# with open('polls/raw_data/Goal_cell_line.csv') as csvfile:
# 	map_reader = csv.DictReader(csvfile, delimiter=';')
# 	bto_map = {}
# 	for row in map_reader:
# 	   bto_map[row['CellLine']] = row['BTO']
# csvfile.close()	

with open('polls/raw_data/Predicted.protein.tissue.scl.csv') as csvfile:
	reader = csv.DictReader(csvfile,delimiter=";")
	line = 0
	for row in reader:
		line +=1
		if line > 0:
			print(line)
			bto_obj = Tissue.objects.get(BTO_id=row['Tissue'])
			entrez = row['EntrezID']
			protein_obj = Gene_Protein.objects.get(EntrezID=entrez)
			source_obj = Data_source.objects.get(source = "Prediction")
			go_obj = SCLocalization.objects.get(GO_id=row['SCL'])
			try:
				t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,source = source_obj)
				print('exists!')
			except ObjectDoesNotExist:
				t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,source = source_obj)
				t.save()
				print('new!')


def import_go(csvreader):
	go_list = list(SCLocalization.objects.values_list('GO_id', flat=True))
	i = 0
	for row in csvreader:
		# print(row)
		if len(row)==3:
			try:
				go = SCLocalization(GO_id = row['GO_term'],SCL_term=row['SCL_term'])
				go.save()
				i +=1
			except IntegrityError as e: 
				if 'unique constraint' in e.message:
					raise e
	print(str(i)+ 'GO terms are loaded')		


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
						print('new')
					except IntegrityError as e: 
						if 'unique constraint' in e.message:
							pass
				else:
					print('EXIST')
		except IntegrityError as e:
			raise e		



