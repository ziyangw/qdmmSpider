# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdmm', '0002_auto_20160819_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='key',
            field=models.BigIntegerField(db_index=True),
        ),
    ]