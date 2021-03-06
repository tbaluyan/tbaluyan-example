# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-13 16:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.current_user


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.ForeignKey(blank=True, default=main.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
