# from django.http import Http404
# from django.shortcuts import render
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

import os


def health(request):
    return HttpResponse(PageView.objects.count())


# class IndexView(generic.ListView):
#     template_name = 'ts_scl_db/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]

# class IndexView(generic.ListView):
#     template_name = 'ts_scl_db/index.html'
#     # context_object_name = 'latest_question_list'
#     context_object_name  = 'all_bto_obj'

#     def get_queryset(self):
#         return .objects.order_by('-pmid')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'ts_scl_db/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class DetailView_2(generic.DetailView):
    model = PubFulltext
    template_name = 'ts_scl_db/detail_2.html'
    context_object_name  = 'fulltext_obj'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return PubFulltext.objects.order_by('-pmid')


class DetailView_3(generic.DetailView):
    template_name = 'ts_scl_db/detail_3.html'
    context_object_name  = 'query_gene_obj'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Gene_Protein.objects.order_by('idGene_Protein')


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ts_scl_db/results.html'


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'ts_scl_db/index.html', context)

def index(request):
    print('i am index')
    all_bto = Tissue_triple_relation.objects.order_by().values('id_BTO__BTO_id','id_BTO__BTO_term').distinct()
    # print(all_bto)
    all_go = Tissue_triple_relation.objects.order_by().values('id_GO__GO_id','id_GO__SCL_term').distinct()
      # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    return render(request, 'ts_scl_db/index.html', {"all_bto_obj": all_bto,"all_go_obj":all_go})


def about(request):
    all_bto = None;
    return render(request, 'ts_scl_db/about.html',{"test":all_bto})

def download(request):
    return render(request, 'ts_scl_db/download.html')

def contact(request):
    return render(request, 'ts_scl_db/contact.html')

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'ts_scl_db/detail.html', {'question': question})
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'ts_scl_db/detail.html', {'question': question})

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


def detail_2(request, idPubFulltext):
    fulltext_obj = get_object_or_404(PubFulltext, pk=idPubFulltext)
    return render(request, 'ts_scl_db/detail_2.html', {'fulltext_obj':fulltext_obj})

def unhighlight(text):
    text = text.replace("<span class='highlight'>","")
    text = text.replace("</span>","")
    return text
    # return mark_safe(text.replace(word, "<span class='highlight'>%s</span>" % word))

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
    # return mark_safe(text.replace(word, "<span class='gene'><mark>%s</mark></span>" % word))

# class PubtagView(generic.DetailView):
#     # model = fa
#     template_name = 'ts_scl_db/show_pub_tags.html'
#     context_object_name  = 'fulltext_obj'
#     # context_object_name  = 'abstract'

#     def get_queryset(self):
#         return self

# a function to check our new vocabulary 
def check_vocabulary(word,categ):
    if categ == 'tissue':
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

def show_pub_tags(request, pk ):
    try:
        pub_obj = get_object_or_404(PubMed_entry, pk=pk)
        # pubanno_obj = get_object_or_404(Relation_Pub_Anno, pmid = pub_obj.pmid)
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
        abstract = '.'.join(text.split('.')[1:])
        tagger_obj={}
        tagger_obj['title']=title
        tagger_obj['abstract'] = abstract
        tagger_obj['pmid'] = fulltext_obj.pmid
        return render(request, 'ts_scl_db/show_pub_tags.html', {'tagger_obj':tagger_obj})
    except:
        raise('Sorry, the annotation of this article is not available.')




def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'ts_scl_db/results.html', {'question': question})

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ts_scl_db/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ts_scl_db:results', args=(question.id,)))


def vote_2(request):
    if request.method == 'POST':
        form = searchIDForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['search_id'])
            question = get_object_or_404(Question, pk=form.cleaned_data['search_id'])
        else:
            # print(form.errors)
            question = get_object_or_404(Question, pk=1)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ts_scl_db/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ts_scl_db:results', args=(question.id,)))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def combine_queryset():
    result_list = list(chain(page_list, article_list, post_list))




def select_protein(request):
    # print(request.POST['query_bto'])
    ''' Show the table of triplets'''
    if request.method == 'POST':
        # print(request.POST)
        form = searchIDForm(request.POST)
        # print(form)
        if form.is_valid():
            search_id = form.cleaned_data['search_id']
            bto_id = form.cleaned_data['query_bto']
            go_id = form.cleaned_data['query_go']
            scoreRange = form.cleaned_data['scoreRange']
            print('select_protein:',form.cleaned_data) 	           
       		# data types.    
            if "yes" in form.cleaned_data['query_tm']:
                pk_tm = Data_source.objects.get(source='Text-mining').pk
            else:
            	pk_tm = 0
            if "yes" in form.cleaned_data['query_kn']:
                pk_kn = Data_source.objects.get(source='Knowledge').pk
            else:
            	pk_kn = 0
            if "yes" in form.cleaned_data['query_exp']:
                pk_exp = Data_source.objects.get(source="Experiment").pk
            else:
            	pk_exp = 0
            if "yes" in  form.cleaned_data['query_pred']:
            	pk_pred = Data_source.objects.get(source="Prediction").pk
            else:
            	pk_pred = 0
            # get gene object
            query_gene_objs = [] 
            if is_number(search_id):
                query_gene_objs = list(chain(query_gene_objs,Gene_Protein.objects.filter( EntrezID__contains = search_id)))
                # query_gene_objs.append(Gene_Protein.objects.filter( EntrezID__contains = search_id))
            else:
                # uniprot acc
                query_gene_objs = list(chain(query_gene_objs,Gene_Protein.objects.filter(UniprotACC__contains = search_id)))
                # Gene symbol
                query_gene_objs = list(chain(query_gene_objs,Gene_Protein.objects.filter(GeneSymbol__contains = search_id)))
                # Gene name
                # query_gene_objs = list(chain(query_gene_objs,Gene_Protein.objects.filter( GeneName__contains = search_id)))
            # print(query_gene_objs)
            query_gene_objs_out = []
            query_gene_objs_out = query_gene_objs
            return render(request, 'ts_scl_db/select_protein.html', {'query_gene_obj':query_gene_objs_out,"bto_id":bto_id,"go_id":go_id, 'pk_exp': pk_exp,'pk_kn': pk_kn,'pk_pred': pk_pred,'pk_tm': pk_tm, 'scoreRange':scoreRange})
            # else:
            #     return render(request, 'ts_scl_db/exception.html')
        else:
            return render(request, 'ts_scl_db/exception.html')


def detail_3(request):
    # print(request.POST['query_bto'])
    ''' Show the table of triplets'''
    if request.method == 'POST':
        # print(request.POST)
        form = searchIDForm(request.POST)
        if form.is_valid():
            print('detail_3:',form.cleaned_data)
            search_id = form.cleaned_data['search_id']
            bto_id = form.cleaned_data['query_bto']
            go_id = form.cleaned_data['query_go']
            scoreRange = form.cleaned_data['scoreRange']
            data_sc = []
       		# data types.    
            if form.cleaned_data['query_tm'] != '0':
                data_sc.append(form.cleaned_data['query_tm'])
            if form.cleaned_data['query_kn'] != '0':
                data_sc.append(form.cleaned_data['query_kn'])
            if form.cleaned_data['query_exp'] != '0':
                data_sc.append(form.cleaned_data['query_exp'])
            if form.cleaned_data['query_pred'] != '0':
            	data_sc.append(form.cleaned_data['query_pred'])
            # print('data_sc:',data_sc)                  
            # get gene object
            # uniprot acc
            if scoreRange == None:
                scoreRange = 0
            query_gene_obj = Gene_Protein.objects.get(pk = search_id)
            # query_gene_obj = Gene_Protein.objects.get(pk = 5115)
            if query_gene_obj != None:
                # query_gene_obj = query_gene_obj[0]
                try:
                    if bto_id =='all' and go_id =='all':
                        query = Tissue_triple_relation.objects.filter(id_Entrez= query_gene_obj.pk, source__in = data_sc , Zscore__gte = scoreRange)
                    if bto_id !='all' and go_id !='all':
                        query = Tissue_triple_relation.objects.filter(id_Entrez = query_gene_obj.pk, id_BTO__BTO_id =bto_id, id_GO__GO_id= go_id, source__in= data_sc, Zscore__gte = scoreRange)
                    elif bto_id !='all' and go_id =='all':
                        query = Tissue_triple_relation.objects.filter(id_Entrez = query_gene_obj.pk, id_BTO__BTO_id =bto_id, source__in= data_sc, Zscore__gte = scoreRange)
                    elif bto_id =='all' and go_id !='all':
                        query = Tissue_triple_relation.objects.filter(id_Entrez = query_gene_obj.pk, id_GO__GO_id= go_id, source__in= data_sc, Zscore__gte = scoreRange)
                    query_distinct = query.values('idTissue_triple_relation','id_Entrez','id_BTO','id_GO','Zscore','review','source').distinct().order_by('Zscore').reverse()

                    triple_relation_obj = []
                    for each in query_distinct:
                        to_add = each
                        to_add['id_Entrez'] = Gene_Protein.objects.get(pk=each['id_Entrez']).EntrezID                        
                        bto_obj = Tissue.objects.get(pk=each['id_BTO'])
                        to_add['id_BTO'] = bto_obj.BTO_id
                        to_add['BTO_term'] = bto_obj.BTO_term.capitalize()
                        
                        go_obj = SCLocalization.objects.get(pk=each['id_GO'])
                        to_add['id_GO'] = go_obj.GO_id
                        to_add['SCL_term'] = go_obj.SCL_term.title()
                        # print(to_add['SCL_term']+' and')
                        to_add['source'] = Data_source.objects.get(pk=each['source']).source
                        if to_add['source'] != 'Text-mining':
                            to_add['Zscore'] = '-'
                        else:
                            to_add['Zscore'] = format(each['Zscore'] , '.2f')
                        # if to_add['source'] == 'Knowledge':
                        # get information of publications for the triplets
                        pmids_pk = Tissue_triple_relation_pmid.objects.filter(Tissue_triple_relation_id = each['idTissue_triple_relation']).distinct().values_list('id_pmid',flat=True)
                        # for pk in pmids_pk:
                        pmids_list = PubMed_entry.objects.filter(pk__in  = pmids_pk).distinct()
                        # if to_add['source'] != 'Knowledge' and to_add['BTO_term'] == "Bladder":
                        #     print('idTissue_triple_relation:',each['idTissue_triple_relation'])
                        #     print(to_add['id_Entrez'], pmids_list.values())
                        #     print('pmid number:',len(pmids_list))
                        #     print('--------------------------------------')
                        if to_add['source'] in ['Predicted']:
                            to_add['pmid_count'] = '-'
                        elif to_add['source'] in ['Experiment']:
                            to_add['pmid_count'] = 'HPA'
                        else:
                            to_add['pmid_count'] = len(pmids_list)
                        triple_relation_obj.append(to_add)
                        # print(triple_relation_obj)
                    return render(request, 'ts_scl_db/triplet_details.html', {'query_gene_obj':query_gene_obj,'triple_relation_obj':triple_relation_obj})
                except Gene_Protein.DoesNotExist:
                    raise "Gene/Protein is not found! Please try another search name."
                    return render(request, 'ts_scl_db/exception.html')
            else:
                return render(request, 'ts_scl_db/exception.html')
        else:
            return render(request, 'ts_scl_db/exception.html')
    else:
        return render(request, 'ts_scl_db/exception.html')
# def detail_3(request):
#     if request.method == 'POST':
#         form = searchIDForm(request.POST)
#         if form.is_valid():
#             search_id = form.cleaned_data['search_id']
#         else:
#             search_id = -1
#         try:
#             # query_gene_obj = Gene_Protein.objects.get(EntrezID = form)
#             query_gene_obj = get_object_or_404(Gene_Protein, EntrezID = search_id)

#             triple_relation_obj = Tissue_triple_relation.objects.filter(id_Entrez = search_id)

#             if query_gene_obj:
#                 table = TripleRelationTable(triple_relation_obj)
#                 RequestConfig(request).configure(table)
#                 # return render(request, 'ts_scl_db/detail_3.html', {'query_gene_obj':query_gene_obj,'triple_relation_obj':triple_relation_obj})
#                 return render(request, 'ts_scl_db/detail_3.html', {'table': table})
#         except Gene_Protein.DoesNotExist:
#             return HttpResponse("no such user")  
#     else:
#         return render(request, 'index.html')


# def show_pmid_list_old(request):
#     if request.method == 'POST':
#         # print('post')
#         form = pmid_listForm(request.POST)
#         # print(request.POST)
#         # print(form)
#         if form.is_valid():
#             # get list of pmids 
#             id_Entrez = form.cleaned_data['id_Entrez']
#             id_BTO = form.cleaned_data['id_BTO']
#             id_GO = form.cleaned_data['id_GO']
#             id_Entrez_pk = Gene_Protein.objects.get(EntrezID =id_Entrez).pk
#             id_BTO_pk = Tissue.objects.get(BTO_id =id_BTO).pk
#             id_GO_pk = SCLocalization.objects.get(GO_id = id_GO).pk
#             triple_relation_pk = Tissue_triple_relation.objects.get(id_Entrez = id_Entrez_pk,id_BTO =id_BTO_pk ,id_GO =id_GO_pk).pk
#             pmids_pk = Tissue_triple_relation_pmid.objects.filter(Tissue_triple_relation_id = triple_relation_pk).values_list('id_pmid',flat=True)
#             pmids_list = PubMed_entry.objects.filter(pk__in  = pmids_pk)
#             # print(pmids_list)
#             return render(request, 'ts_scl_db/show_pmid_list.html', {'query_pmid_list': pmids_list})
#         else:
#             return render(request, 'index.html')
        
#     else:
#         return render(request, 'index.html')

def show_pmid_list(request):
    if request.method == 'POST':
        # print('post')
        form = pmid_listForm(request.POST)
        print(request.POST)
        # print(form)
        if form.is_valid():
            print("show_pmid_list:",form.cleaned_data)
            # get list of pmids 
            id_Entrez = form.cleaned_data['id_Entrez']
            id_BTO = form.cleaned_data['id_BTO']
            id_GO = form.cleaned_data['id_GO']
            term_source = form.cleaned_data['term_source']
            search_id = form.cleaned_data['search_id']
            query_gene_obj = Gene_Protein.objects.get(pk = search_id)
            # print(form.cleaned_data)
            id_Entrez_pk = Gene_Protein.objects.get(EntrezID =id_Entrez).pk
            id_BTO_pk = Tissue.objects.get(BTO_id = id_BTO).pk
            id_GO_pk = SCLocalization.objects.get(GO_id = id_GO).pk
            term_source_pk = Data_source.objects.get(source = term_source).pk
            # id_BTO_pk = Tissue.objects.get(BTO_term = id_BTO).pk
            # id_GO_pk = SCLocalization.objects.get(SCL_term = id_GO).pk
            triple_relation_pk = Tissue_triple_relation.objects.get(id_Entrez = id_Entrez_pk,id_BTO =id_BTO_pk ,id_GO =id_GO_pk, source = term_source_pk).pk
            pmids_pk = Tissue_triple_relation_pmid.objects.filter(Tissue_triple_relation_id = triple_relation_pk).values_list('id_pmid',flat=True).distinct()
            # pmids_list = PubMed_entry.objects.filter(pk__in  = pmids_pk)
            # print(pmids_list)
            # generate the objets of pmid taggers
            tagger_objs = []
            for pmid_pk in pmids_pk:
                triplet_pmid_pk= Tissue_triple_relation_pmid.objects.filter(Tissue_triple_relation_id = triple_relation_pk,id_pmid=pmid_pk).values_list('pk',flat=True)[0]
                tagger = show_pub_tags(pmid_pk)
                if tagger is not None:
                    tagger['triplet_pmid_pk'] = triplet_pmid_pk
                    tagger_objs.append(tagger)
                    # print(tagger_objs)
            # print(tagger_objs)
            return render(request, 'ts_scl_db/show_pmid_list.html', {'query_gene_obj':query_gene_obj,'tagger_objs':tagger_objs})
            # return render(request, 'ts_scl_db/show_pmid_list.html', {'query_pmid_list': pmids_list})
        else:
            return render(request, 'index.html')
        
    else:
        return render(request, 'index.html')

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
        return tagger_obj
    except:
        # return 'Sorry, the annotation of this article is not available.'
        return None

def endose(request):
    if request.method == 'POST':
        # print('post')
        form = endosorForm(request.POST)
        # print(form)
        if form.is_valid():
            print(form.cleaned_data)
            id_triple_pmid = form.cleaned_data['triple_relation_pmid_pk']
            try: 
                triple_pmid_obj = Tissue_triple_relation_pmid.objects.get(pk = id_triple_pmid)
                endosor =  form.cleaned_data['endosor']
                try:
                    triple_pmid_endosor = Tissue_triple_relation_pmid_endose(idTissue_triple_relation_pmid = triple_pmid_obj, endosor = endosor)
                    triple_pmid_endosor.save()
                except IntegrityError:
                    pass
            except Tissue_triple_relation_pmid.DoesNotExist:
                pass
        return render(request, 'ts_scl_db/endose.html')

