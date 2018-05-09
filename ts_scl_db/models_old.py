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
    Tissue_term = models.CharField(max_length=50)
    BTO_id = models.CharField(max_length=50,unique=True,)
    def __str__(self):
        return self.Tissue_term    


class CellLine(models.Model):
    idCellLine = models.AutoField(primary_key=True)
    CellLine_term = models.CharField(max_length=50)
    BTO_id = models.CharField(max_length=50,unique=True,)
    def __str__(self):
        return self.CellLine_term


class Gene_Protein(models.Model):
    idGene_Protein = models.AutoField(primary_key=True)
    EntrezID = models.IntegerField(unique=True)
    UniprotACC = models.CharField(max_length=50,unique=True,)
    GeneName = models.CharField(max_length=50)
    def __str__(self):
        return self.GeneName
   

class SCLocalization(models.Model):
    idSCL = models.AutoField(primary_key=True)
    GO_id = models.CharField(max_length=50,unique=True,)
    SCL_term = models.CharField(max_length=50)
    def __str__(self):
        return self.SCL_term

class PubAnnotation(models.Model):
    idPubAnnotation = models.AutoField(primary_key=True)
    annotaion = models.CharField(max_length=50) 
    typeAnno = models.CharField(max_length=50)
    def __str__(self):
        return self.typeAnno    

#-------------------------------------------------------------
# pair relations
#-------------------------------------------------------------
class Relation_tissue_gene(models.Model):
    idRelation_tissue_gene = models.AutoField(primary_key=True)
    index_tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    index_gene = models.ForeignKey(Gene_Protein, on_delete=models.CASCADE)


class Relation_CL_gene(models.Model):
    idRelation_CL_gene = models.AutoField(primary_key=True)
    index_CL = models.ForeignKey(CellLine, on_delete=models.CASCADE)
    index_gene = models.ForeignKey(Gene_Protein, on_delete=models.CASCADE)


class Relation_gene_SCL(models.Model):
    idRelation_gene_SCL = models.AutoField(primary_key=True)
    index_gene = models.ForeignKey(Gene_Protein, on_delete=models.CASCADE)
    index_scl = models.ForeignKey(SCLocalization, on_delete=models.CASCADE)


class Relation_Pub_Anno(models.Model):
    idRelation_Pub_Anno = models.AutoField(primary_key=True)
    id_pub_anno = models.ForeignKey(PubAnnotation, on_delete=models.CASCADE)

class PubMed_entry(models.Model):
    idPubMed_entry = models.AutoField(primary_key=True)
    PMID = models.IntegerField(unique=True)
    id_relation_Pub_Anno = models.ForeignKey(Relation_Pub_Anno, on_delete=models.CASCADE)


class TableListPMID(models.Model):
    idTableListPMID = models.AutoField(primary_key=True)
    # id_triplet = models.ForeignKey(Tissue_triple_relation, on_delete=models.CASCADE)
    id_PudMed = models.ForeignKey(PubMed_entry, on_delete=models.CASCADE)



#-------------------------------------------------------------
# triple relations
#-------------------------------------------------------------

class Tissue_triple_relation(models.Model):
    idTissue_triple_relation = models.AutoField(primary_key=True)
    id_tissue_gene = models.ForeignKey(Relation_tissue_gene, on_delete=models.CASCADE)
    id_gene_SCL = models.ForeignKey(Relation_gene_SCL, on_delete=models.CASCADE)
    id_list_pmid = models.ForeignKey(TableListPMID, on_delete=models.CASCADE)

class CL_triple_relation(models.Model):
    idCL_triple_relation = models.AutoField(primary_key=True)
    id_CL_gene = models.ForeignKey(Relation_CL_gene, on_delete=models.CASCADE)
    id_gene_SCL = models.ForeignKey(Relation_gene_SCL, on_delete=models.CASCADE)
    id_list_pmid = models.ForeignKey(TableListPMID, on_delete=models.CASCADE)





