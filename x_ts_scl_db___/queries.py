# set all triplets which are manuel curated as reviewed.
from ts_scl_db.models import *
from django.shortcuts import get_object_or_404, render
import ast
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

obj = Tissue_triple_relation.objects.filter(source__source = 'Knowledge')
print(len(obj))
obj = Tissue_triple_relation.objects.filter(source__source = 'Text-mining')
print(len(obj))
obj = Tissue_triple_relation.objects.filter(source__source = 'Experiment')
print(len(obj))

# load hpa data 
pyhton load_HPA.py





# update value of objects
kd_obj = Tissue_triple_relation.objects.filter(source__source = "Knowledge")

kd_obj.update(review='Yes')




#debug

id_Entrez= '7157'
id_BTO='BTO:0000763'
id_GO= 'GO:0005634'
id_Entrez_pk = Gene_Protein.objects.get(EntrezID =id_Entrez).pk
id_BTO_pk = Tissue.objects.get(BTO_id = id_BTO).pk
id_GO_pk = SCLocalization.objects.get(GO_id = id_GO).pk


triple_relation_objs= Tissue_triple_relation.objects.filter(id_Entrez = id_Entrez_pk,id_BTO =id_BTO_pk ,id_GO =id_GO_pk)

id_Entrez = '7157'
id_BTO = 'BTO:0000123'
id_GO = 'GO:0005634'
id_Entrez_pk = Gene_Protein.objects.get(EntrezID =id_Entrez).pk
id_BTO_pk = Tissue.objects.get(BTO_id = id_BTO).pk
id_GO_pk = SCLocalization.objects.get(GO_id = id_GO).pk


triple_relation_objs = Tissue_triple_relation.objects.filter(id_Entrez = id_Entrez_pk,id_BTO =id_BTO_pk ,id_GO =id_GO_pk)
# triple_relation_objs.values_list('idTissue_triple_relation')

query = triple_relation_objs
query_distinct = query.values('idTissue_triple_relation','id_Entrez','id_BTO','id_GO','Zscore','review','source').distinct().order_by('Zscore').reverse()

each = query_distinct[0]
# combine all pmids 


pmids_pk = Tissue_triple_relation_pmid.objects.filter(Tissue_triple_relation_id = each['idTissue_triple_relation']).distinct().values_list('id_pmid',flat=True)

pmids_list = PubMed_entry.objects.filter(pk__in= pmids_pk).distinct()

# pmids_list_2=[]
# for pk in pmids_pk:
# 	pmids_list_2.append(PubMed_entry.objects.filter(pk= pk).distinct())
pmids = []
for pmid_pk in pmids_pk:
	pmids.append(PubMed_entry.objects.filter(pk__in  = pmid_pk).distinct())

each = query_distinct[1]

tagger_objs = []
for pmid_pk in pmids_pk:
	print('-----------------------')
	print(pmid_pk)
	tagger = show_pub_tags(pmid_pk)
	if tagger is not None:
		tagger_objs.append(tagger)

pub_obj = get_object_or_404(PubMed_entry, pk=pmid_pk)
rel_pubanno_obj = pub_obj.id_Pub_Anno
pubanno_obj = rel_pubanno_obj.id_pub_anno
fulltext_obj= rel_pubanno_obj.id_pub_fulltext
text = fulltext_obj.fulltext
annotation = ast.literal_eval(pubanno_obj.annotaion)

pk = '27661'
def show_pub_tags(pk):
    try:
        pub_obj = get_object_or_404(PubMed_entry, pk=pk)
        # pubanno_obj = get_object_or_404(Relation_Pub_Anno, pmid = pub_obj.pmid)
        # print("pk:",pk)  #               debug
        rel_pubanno_obj = pub_obj.id_Pub_Anno
        pubanno_obj = rel_pubanno_obj.id_pub_anno
        fulltext_obj= rel_pubanno_obj.id_pub_fulltext
        text = fulltext_obj.fulltext
        annotation = ast.literal_eval(pubanno_obj.annotaion)
        # text = unhighlight(text)
        # to_high_light = list(set([x['surfaceForm'] for x in annotation]))
        to_high_light={}
        for x in annotation:
            to_high_light[x['surfaceForm']] = x['source']
        for word, category in to_high_light.items():
            text = highlight(text, word , category)
        
        title = text.split('.')[0]+'.'
        replaced = re.sub('^\[', '', title)
        replaced = re.sub('.\]', '.', replaced)
        tagger_obj={}
        tagger_obj['title']= replaced
        # print(replaced)  # debug
        abstract = '.'.join(text.split('.')[1:])
        tagger_obj['abstract'] = abstract
        
        tagger_obj['pmid'] = fulltext_obj.pmid
        # get authors
        tagger_obj['authors']= pub_obj.authors
        # get journal 
        tagger_obj['journal']=  pub_obj.journal
        print(tagger_obj)
        return tagger_obj
    except:
        # return 'Sorry, the annotation of this article is not available.'
        return None

def highlight(text, word, categ):
    if categ in ['tissue','tissues']:
        categ = 'bto_filtered'
    clss ={'bto_filtered' : 'tissue',
           'genementions': 'gene',
           'subcellular_go' : 'SCL'}
    if check_vocabulary(word,clss[categ]):
        return mark_safe(text.replace(word, "<span class='"+clss[categ]+"'>%s</span>" % word))
    else:
        return text

def check_vocabulary(word,categ):
    if categ in ['tissue','tissues']:
        words = list(BTO_vocabulary.objects.all().values('words'))
        word_list = [x['words'] for x in words]
        return word in word_list
    elif categ == 'SCL':
        # try:
        #     scl_obj = get_object_or_404(SCL_vocabulary, words=word)
        #     return True
        # except (KeyError, SCL_vocabulary.DoesNotExist):
        #     return False
        words = list(SCL_vocabulary.objects.all().values('words'))
        word_list = [x['words'] for x in words]
        return word in word_list
    elif categ == 'gene':
        return True       