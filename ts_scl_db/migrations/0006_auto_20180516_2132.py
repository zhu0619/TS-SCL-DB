# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ts_scl_db', '0005_auto_20180513_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tissue_triple_relation_pmid_endose',
            fields=[
                ('idendose', models.AutoField(primary_key=True, serialize=False)),
                ('endosor', models.CharField(default='anonymous', max_length=100)),
                ('idTissue_triple_relation_pmid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ts_scl_db.Tissue_triple_relation_pmid')),
            ],
        ),
        migrations.AlterField(
            model_name='pubmed_entry',
            name='authors',
            field=models.CharField(default='No details', max_length=1000),
        ),
        migrations.AlterField(
            model_name='pubmed_entry',
            name='journal',
            field=models.CharField(default='No details', max_length=1000),
        ),
        migrations.AlterField(
            model_name='tissue',
            name='BTO_term',
            field=models.CharField(default='EMPTY', max_length=200),
        ),
    ]