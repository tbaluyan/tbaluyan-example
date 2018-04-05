# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-21 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actions', '0002_auto_20180313_1627'),
        ('projects', '0023_project_preferences_reports'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='содержание')),
                ('status', models.CharField(blank=True, choices=[('OK', 'Выполнено'), ('PRC', 'Выполняется'), ('MINPR', 'Есть проблемы'), ('MAJPR', 'Требуется решение проблем'), ('NA', 'Не актуально'), ('NN', 'Не требуется')], max_length=10, verbose_name='статус')),
                ('link', models.URLField(blank=True, verbose_name='ссылка')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('actions', models.ManyToManyField(related_name='_report_field_actions_+', to='actions.Action')),
            ],
            options={
                'ordering': ['field_type'],
            },
        ),
        migrations.CreateModel(
            name='Report_Field_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('order', models.IntegerField(default=10, verbose_name='порядок')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'Report_Field_Categories',
            },
        ),
        migrations.CreateModel(
            name='Report_Field_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('placeholder', models.TextField(blank=True, verbose_name='подсказка')),
                ('has_status', models.BooleanField(default=True, verbose_name='имеет статус')),
                ('has_url', models.BooleanField(default=True, verbose_name='имеет ссылку')),
                ('order', models.IntegerField(default=10, verbose_name='порядок')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_reports.Report_Field_Category', verbose_name='категория')),
                ('project_types', models.ManyToManyField(blank=True, to='projects.Project_type', verbose_name='типы проектов')),
            ],
            options={
                'ordering': ['category', 'order'],
            },
        ),
        migrations.AddField(
            model_name='report_field',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_reports.Report_Field_Type', verbose_name='тип поля'),
        ),
        migrations.AddField(
            model_name='report_field',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='проект'),
        ),
        migrations.AlterUniqueTogether(
            name='report_field',
            unique_together=set([('project', 'field_type')]),
        ),
    ]
