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

##==========================#
##Tissue_triple_relation	#
##==========================#
# Tissue_triple_relation.objects.all().delete()

# gene 
with open('ts_scl_db/raw_data/HPA_Cell_Line_benchmark_table.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	ensg_id = list(set([x['Ensembl_ID'] for x in reader ]))
	data = mg.getgenes(ensg_id,fields="entrezgene,ensemblgene,uniprot,'symbol', 'name'",species=9606)
	import_protein(data)
csvfile.close()

# go
with open('ts_scl_db/raw_data/HPA_Cell_Line_benchmark_table.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	import_go(reader)
csvfile.close()


# bto
import_bto()


# HPA triplet

with open('ts_scl_db/raw_data/Goal_cell_line.csv') as csvfile:
	map_reader = csv.DictReader(csvfile, delimiter=';')
	bto_map = {}
	for row in map_reader:
	   bto_map[row['CellLine']] = row['BTO']
csvfile.close()	

with open('ts_scl_db/raw_data/HPA_Cell_Line_benchmark_table.csv') as csvfile:
	reader = csv.DictReader(csvfile,delimiter="\t")
	i=0
	for row in reader:
		i += 1
		print(i)
		cell_line = bto_map[row['CellLine']]
		bto_obj = Tissue.objects.get(BTO_id=cell_line)

		entrez = get_entrez_id(data, dict(row)['Ensembl_ID'])
		if entrez is None:
			continue
		protein_obj = Gene_Protein.objects.get(EntrezID=entrez)
		
		go_obj = SCLocalization.objects.get(GO_id=row['GO_term'])

		source_obj = Data_source.objects.get(source = "Experiment")
		try:
			t = Tissue_triple_relation.objects.get(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,reliability=row['reliability'],source = source_obj, Zscore = 9999)
			print('exists!')
		except ObjectDoesNotExist:
			t = Tissue_triple_relation(id_BTO = bto_obj ,id_Entrez =protein_obj,id_GO = go_obj,reliability=row['reliability'],source = source_obj, Zscore = 9999)
			t.save()
			print('new!')

def get_entrez_id(data, ensg):
	x = list(filter(lambda person: person['query'] == ensg, data))[0]
	if 'entrezgene' in x.keys():
		return x['entrezgene']
	else:
		return None

def get_bto_id(cell_line):
	with open('ts_scl_db/raw_data/Goal_cell_line.csv') as csvfile:
		map_reader = csv.DictReader(csvfile, delimiter=';')
		bto_map = {}
		for row in map_reader:
		   bto_map[row['CellLine']] = row['BTO']
	csvfile.close()	
	return bto_map[cell_line]

def import_bto():
	with open('ts_scl_db/raw_data/Goal_cell_line.csv') as csvfile:
		map_reader = csv.DictReader(csvfile, delimiter=';')
		bto_map = {}
		for row in map_reader:
		   bto_map[row['CellLine']] = row['BTO']
	csvfile.close()
	with open('ts_scl_db/raw_data/HPA_Cell_Line_benchmark_table.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter='\t')
		bto_id = list(set([x['CellLine'] for x in reader ]))
		bto_list = list(Tissue.objects.values_list('BTO_id', flat=True))
		i=0
		for bto in bto_id:
			id_bto = bto_map[bto]
			if id_bto not in bto_list:
				try:
					link = "http://purl.obolibrary.org/obo/"+id_bto
					link = link.replace(":","_")
					bto = Tissue(BTO_id = id_bto,BTO_term=row['CellLine'],BTO_link = link )
					bto.save()
					i +=1
				except IntegrityError as e: 
					if 'unique constraint' in e.message:
						pass
		print(str(i)+' BTO terms are loaded')
	csvfile.close()

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
					except IntegrityError as e: 
						if 'unique constraint' in e.message:
							pass
		except IntegrityError as e:
			raise e		



