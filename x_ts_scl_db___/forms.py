from django import forms
from django.forms import ModelForm

class searchIDForm(forms.Form):
    search_id = forms.CharField(max_length=50)
    query_bto = forms.CharField(max_length=20)
    query_go = forms.CharField(max_length=20)
    query_tm = forms.CharField(max_length=20)
    query_exp = forms.CharField(max_length=20)
    query_kn  = forms.CharField(max_length=20)
    query_pred = forms.CharField(max_length=20)
    scoreRange = forms.FloatField(required=False, max_value=100, min_value=-10)

class pmid_listForm(forms.Form):
    id_Entrez = forms.CharField(max_length=50)
    id_BTO = forms.CharField(max_length=50)
    id_GO = forms.CharField(max_length=50)
    term_source = forms.CharField(max_length=50)
    search_id = forms.CharField(max_length=50)