#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""

from django.db import IntegrityError

from ts_scl_db.models import *

source_list = list(Data_source.objects.values_list('source', flat=True))

sources = ["Text-mining","Knowledge","Experiment","Prediction"]

for source in sources: 
	if source not in source_list:
		try:
			g = Data_source(source = source )
			g.save()
		except IntegrityError as e: 
			if 'unique constraint' in e.message:
				pass
	
#Gene_Protein.objects.all().delete()



# Gene_Protein.objects.get('EntrezID'=284578)



