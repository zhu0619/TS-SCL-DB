from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.html import *
from django import forms
from django_tables2 import RequestConfig
import ast
from haystack.utils import Highlighter
from itertools import chain

from ts_scl_db.models import *
from ts_scl_db.forms import *
from ts_scl_db.tables import TripleRelationTable
# Tissue_triplet_relation.objects.filter()
objets = Tissue_triple_relation.objects.filter(source__source='text-mining-test')
list = Tissue_triple_relation.objects.values('id_Entrez','id_Entrez__GeneSymbol').annotate(count_protein=Count('id_Entrez')).order_by('-count_protein')
list[0].count

list = Tissue_triple_relation.objects.values('id_Entrez__GeneSymbol').annotate(count_protein=Count('id_Entrez'),count_tissue = Count('id_BTO',distinct=True),count_go=Count('id_GO',distinct=True)).order_by('-count_go')


# diverse scl protein 
prot_scl_list=Tissue_triple_relation.objects.filter(source__source='Text-mining').values('id_Entrez__EntrezID','id_Entrez__GeneSymbol').annotate(all_go_count = Count('id_GO'),rate_count_go=Count('id_GO',distinct=True)*100/Count('id_GO'), all_tissue_count = Count('id_BTO'),tissue_count_dist = Count('id_BTO',distinct=True),rate_count_bto =Count('id_BTO',distinct=True)*100/Count('id_BTO')).filter(all_go_count__gt=2,rate_count_go__gt = 80,rate_count_bto__gt=80).order_by('-rate_count_go')

print(len(prot_scl_list))
print(prot_scl_list)

# find out which protein are specific in different tissues. 
list_protein  = Tissue_triple_relation.objects.filter(source__source='Text-mining').values('id_Entrez')

for prot in list_protein:
	tis = Tissue_triple_relation.objects.filter(id_Entrez= prot['id_Entrez']).values('id_BTO').distinct()
	break



