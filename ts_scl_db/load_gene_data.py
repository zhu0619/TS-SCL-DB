#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""

from django.db import IntegrityError
import mygene
mg = mygene.MyGeneInfo()


from ts_scl_db.models import *

#Gene_Protein.objects.all().delete()
with open('ts_scl_db/human_genes.txt','r') as fin:
    sp_genes = fin.read().splitlines() 
    data = mg.getgenes(sp_genes,fields="entrezgene,ensemblgene,uniprot,'symbol', 'name'",species=9606)

entrezgene_list = list(Gene_Protein.objects.values_list('EntrezID', flat=True))

for datum in data:
	# print(datum)
	try:
		if 'notfound' not in datum.keys():
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
			entrezgene_list = list(Gene_Protein.objects.values_list('EntrezID', flat=True))
			if entrez_id not in entrezgene_list :
				try:
					g = Gene_Protein(EntrezID = entrez_id, UniprotACC = uniprot_acc ,GeneName = gene_name, GeneSymbol = gene_symbol  )
					g.save()
					# print('ok!')
				except IntegrityError as e: 
					if 'unique constraint' in e.message:
						pass
	except IntegrityError as e:
		raise e
	




# Gene_Protein.objects.get('EntrezID'=284578)



