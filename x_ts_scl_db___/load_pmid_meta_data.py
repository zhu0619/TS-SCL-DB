#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""
from Bio.Entrez import efetch, read
Entrez.email = "lzhu@uni-bielefeld.de"
from django.db import IntegrityError

from ts_scl_db.models import *
import math

def main():
	all_pmids = PubMed_entry.objects.values('pmid')
	all_pmid_list= [i['pmid'] for i in all_pmids]
	nb_fold = math.ceil(len(all_pmid_list)/10000)
	for f in range(1,nb_fold+1):
		a = (f-1)*10000
		b= f*10000
		if b > len(all_pmid_list):
			b = len(all_pmid_list)
		print(a,b)
		pmid_meta_dict = request_meta(','.join([str(i) for i in all_pmid_list[a:b]]))
		# pmid_meta_dict = request_meta('15711927')
		update_meta_db(pmid_meta_dict)

def update_meta_db(meta_data):
	for pid, met in meta_data.items():
		try:
			obj = PubMed_entry.objects.get(pmid = pid)
			obj.authors= met[0]
			obj.journal = met[1]
			obj.save()
			print(str(pid)+ " update success")
		except:
			raise str(pid)+" update failed"

# x = request_meta("21049,3295")

# use pmid request meta data from bio.entrez 
def request_meta(pmids):
	pmid_meta = {}
	handle = Entrez.esummary(db="pubmed", id=pmids, retmode="xml")
	records = Entrez.parse(handle)
	for record in records:
		pmid_meta[record['Id']] = [', '.join(record['AuthorList']),record['FullJournalName']]
	handle.close()
	return pmid_meta 
		# print(record['AuthorList'])
		# print(record['FullJournalName'])



