# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-22 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_reports', '0002_auto_20180321_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_field',
            name='link_description',
            field=models.CharField(blank=True, max_length=255, verbose_name='описание ссылки'),
        ),
    ]
