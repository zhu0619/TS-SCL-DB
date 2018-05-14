#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""

from django.db import IntegrityError
import csv
from ts_scl_db.models import *




def load_dictionary():
	BTO_vocabulary.objects.all().delete()
	with open('ts_scl_db/raw_data/bto_filtered_090118.vocab.txt','r') as fin:
		csvreader = csv.reader(fin, delimiter='\t')
		i=0
		for row in csvreader:
			if len(row)==2:
				try:
					bto = BTO_vocabulary(BTO_id = row[0],words = row[1])
					bto.save()
					i +=1
				except IntegrityError as e: 
					if 'unique constraint' in e.message:
						raise e
		print(str(i)+' BTO terms are loaded')

	SCL_vocabulary.objects.all().delete()
	with open('ts_scl_db/raw_data/subcellular_go_090118.vocab.txt','r') as fin:
		csvreader = csv.reader(fin, delimiter='\t')
		i=0
		for row in csvreader:
			if len(row)==2:
				try:
					go = SCL_vocabulary(GO_id = row[0],words = row[1])
					go.save()
					i +=1
				except IntegrityError as e: 
					if 'unique constraint' in e.message:
						raise e
		print(str(i)+' GO terms are loaded')
