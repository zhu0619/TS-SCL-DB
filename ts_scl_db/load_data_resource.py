#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:08:03 2017

@author: zhulu
"""

from django.db import IntegrityError

from ts_scl_db.models import *


def load_data_resource():
	source_list = list(Data_source.objects.values_list('source', flat=True))
	sources = ["Text-mining","Knowledge","Experiment","Prediction"]
	for source in sources: 
		if source not in source_list:
			try:
				g = Data_source.objects.get(source = source )
			except Data_source.DoesNotExist: 
				g = Data_source(source = source )
				g.save()
		
#Gene_Protein.objects.all().delete()



# Gene_Protein.objects.get('EntrezID'=284578)



