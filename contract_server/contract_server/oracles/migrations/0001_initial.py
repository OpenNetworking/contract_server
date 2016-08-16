# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 01:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oracle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]