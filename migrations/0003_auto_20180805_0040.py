# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-05 00:40
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0002_initialise_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotes',
            name='customer_notes',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quotes',
            name='quote_terms',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='requirement_scope',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_start_date',
            field=models.DateTimeField(),
        ),
    ]
