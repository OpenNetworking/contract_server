# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 07:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oracles', '0008_auto_20160817_0518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='i_o',
            name='indexed',
        ),
    ]
