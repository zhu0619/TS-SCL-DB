# ts_scl_db/tables.py
import django_tables2 as tables
from .models import *
from django_tables2.utils import Accessor

class TripleRelationTable(tables.Table):
    # idTissue_triple_relation = models.AutoField(primary_key=True)
    # id_BTO_id = models.CharField(max_length=50,default='EMPTY')
    # id_Entrez_id = models.IntegerField(default=-1)
    # id_GO_id = models.CharField(max_length=50,default='EMPTY')
    # id_pmid_id = models.IntegerField(default=-1)
    # Zscore = models.FloatField(default= -1)
	id_BTO_id = tables.Column(verbose_name='BTO', accessor=Accessor('Tissue_triple_relation.id_BTO'))
	id_GO_id = tables.Column(verbose_name='GO',accessor=Accessor('sclocalization.GO_id'))
	id_pmid_id = tables.Column(verbose_name='PMID',accessor=Accessor('pubmed_entry.pmid'))
    # Zscore = tables.FloatField(default= -1)
	class Meta:
		model = Tissue_triple_relation
		fields = ('id_BTO_id','id_GO_id','id_pmid_id')
		template = 'django_tables2/bootstrap.html'
		# template = 'django_tables2/table.html'
