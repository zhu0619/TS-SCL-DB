import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

#--------------------------------------------------------------#
#--------------------------------------------------------------#
#--------------------------------------------------------------#

class Tissue(models.Model):
    idTissue = models.AutoField(primary_key=True)
    BTO_id = models.CharField(max_length=50,unique=True)
    BTO_term = models.CharField(max_length=50, default = 'EMPTY')
    BTO_link = models.CharField(max_length=50,default = 'EMPTY')
    def __str__(self):
        return self.BTO_id


class Gene_Protein(models.Model):
    idGene_Protein = models.AutoField(primary_key=True)
    EntrezID = models.IntegerField(unique=True)
    UniprotACC = models.CharField(max_length=150,default='EMPTY')
    GeneName = models.CharField(max_length=150,default='EMPTY')
    GeneSymbol = models.CharField(max_length=150,default='EMPTY')
    def __int__(self):
        return self.EntrezID
   

class SCLocalization(models.Model):
    idSCL = models.AutoField(primary_key=True)
    GO_id = models.CharField(max_length=50,unique=True)
    SCL_term = models.CharField(max_length=100)
    def __str__(self):
        return self.GO_id


class PubAnnotation(models.Model):
    ''' detailed annotation'''
    idPubAnnotation = models.AutoField(primary_key=True)
    annotaion = models.CharField(max_length=10000) 
    pmid = models.IntegerField(default=-1,unique=True)
    def __int__(self):
        return self.pmid   

class PubTokens(models.Model):
    '''tokenized sentences'''
    idPubTokens = models.AutoField(primary_key=True)
    tokens = models.CharField(max_length=10000) 
    pmid = models.IntegerField(default=-1,unique=True)
    def __int__(self):
        return self.pmid 

class PubFulltext(models.Model):
    '''full text of abstract'''
    idPubFulltext = models.AutoField(primary_key=True)
    fulltext = models.CharField(max_length=10000) 
    pmid = models.IntegerField(default=-1,unique=True)
    def __str__(self):
        return self.fulltext

class TempHighLightedText(models.Model):
    '''full text of abstract'''
    idPubFulltext = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200) 
    fulltext = models.CharField(max_length=10000) 
    pmid = models.IntegerField(default=-1,unique=True)
    def __str__(self):
        return self.title 

class Relation_Pub_Anno(models.Model):
    idRelation_Pub_Anno = models.AutoField(primary_key=True)
    id_pub_anno = models.ForeignKey(PubAnnotation,default=-1 ,on_delete = models.CASCADE)
    id_pub_token = models.ForeignKey(PubTokens, default=-1,on_delete = models.CASCADE)
    id_pub_fulltext = models.ForeignKey(PubFulltext, default=-1, on_delete = models.CASCADE)
    pmid = models.IntegerField(default=-1,unique=True)
    def __int__(self):
        return self.pmid

class PubMed_entry(models.Model):
    idPubMed_entry = models.AutoField(primary_key=True)
    pmid = models.IntegerField(unique=True)
    id_Pub_Anno = models.ForeignKey(Relation_Pub_Anno, on_delete=models.CASCADE)
    authors = models.CharField(max_length=200,default = "No details")
    journal = models.CharField(max_length=100,default = "No details")
    def __int__(self):
        return self.pmid


class SCL_vocabulary(models.Model):
    idSCL_vocab = models.AutoField(primary_key=True)
    words = models.CharField(max_length=200, unique=True)
    GO_id = models.CharField(max_length=50)

class BTO_vocabulary(models.Model):
    idBTO_vocab = models.AutoField(primary_key=True)
    words = models.CharField(max_length=200,unique=True)
    BTO_id = models.CharField(max_length=50)

class Data_source(models.Model):
    idSource =  models.AutoField(primary_key=True)
    source = models.CharField(max_length=20,unique=True)

#-------------------------------------------------------------
# triple relations
#-------------------------------------------------------------

# class Tissue_triple_relation(models.Model):
#     idTissue_triple_relation = models.AutoField(primary_key=True)
#     id_BTO = models.ForeignKey(Tissue,on_delete=models.CASCADE)
#     id_Entrez = models.ForeignKey(Gene_Protein, on_delete = models.CASCADE)
#     id_GO = models.ForeignKey(SCLocalization, on_delete = models.CASCADE)
#     # id_pmid = models.ForeignKey(PubMed_entry, on_delete=models.CASCADE)
#     Zscore = models.FloatField(default= -1)
#     source = models.CharField(max_length=20,default="TM")
#     def __int__(self):
#         return self.idTissue_triple_relation

class Tissue_triple_relation(models.Model):
    idTissue_triple_relation = models.AutoField(primary_key=True)
    id_BTO = models.ForeignKey(Tissue,on_delete=models.CASCADE)
    id_Entrez = models.ForeignKey(Gene_Protein, on_delete = models.CASCADE)
    id_GO = models.ForeignKey(SCLocalization, on_delete = models.CASCADE)
    # id_pmid = models.ForeignKey(PubMed_entry, on_delete=models.CASCADE)
    Zscore = models.FloatField(default= -1)
    reliability =  models.CharField(max_length=10,default= "")
    source = models.ForeignKey(Data_source,on_delete=models.CASCADE,default= -1)
    review = models.CharField(max_length=10,default='No') # later change to reference
    def __int__(self):
        return self.idTissue_triple_relation


class Tissue_triple_relation_pmid(models.Model):
    idTissue_triple_relation_pmid = models.AutoField(primary_key=True)
    Tissue_triple_relation_id = models.ForeignKey(Tissue_triple_relation,on_delete=models.CASCADE)
    id_pmid = models.ForeignKey(PubMed_entry, on_delete=models.CASCADE)
    def __int__(self):
        return self.idTissue_triple_relation_pmid

# class Tissue_triple_relation(models.Model):
#     idTissue_triple_relation = models.AutoField(primary_key=True)
#     id_BTO = models.CharField(max_length=50,default='EMPTY')
#     id_Entrez = models.IntegerField(default=-1)
#     id_GO = models.CharField(max_length=50,default='EMPTY')
#     id_pmid = models.IntegerField(default=-1)
#     Zscore = models.FloatField(default= -1)
#     def __int__(self):
#         return self.idTissue_triple_relation



