#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import csv
from ts_scl_db.models import *

SCLocalization.objects.all().delete()
with open('ts_scl_db/raw_data/goose_go_data.txt','r') as fin:
	csvreader = csv.reader(fin, delimiter='\t')
	go_list = list(SCLocalization.objects.values_list('GO_id', flat=True))
	i = 0
	for row in csvreader:
		# print(row)
		if len(row)==3:
			try:
				go = SCLocalization.objects.get(GO_id = row[2],SCL_term=row[0])
			except ObjectDoesNotExist:
				go = SCLocalization(GO_id = row[2],SCL_term=row[0])
				go.save()
				i +=1
	print(str(i)+ 'GO terms are loaded')