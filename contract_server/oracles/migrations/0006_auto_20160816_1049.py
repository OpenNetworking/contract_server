# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 10:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oracles', '0005_contract_abi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='abi',
            new_name='interface',
        ),
    ]