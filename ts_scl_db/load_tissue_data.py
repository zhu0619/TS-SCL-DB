#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""

from django.db import IntegrityError
import csv
from ts_scl_db.models import *


with open('ts_scl_db/raw_data/BTO_filtered.csv','r') as fin:
	csvreader = csv.reader(fin, delimiter=';')

	bto_list = list(Tissue.objects.values_list('BTO_id', flat=True))
	i = 0
	for row in csvreader:
		print(row)
		if len(row)==3:
			try:
				bto = Tissue(BTO_id = row[0],BTO_term=row[1],BTO_link = row[2] )
				bto.save()
				i +=1
			except IntegrityError as e: 
				if 'unique constraint' in e.message:
					raise e
	print(str(i)+' BTO terms are loaded')