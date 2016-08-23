# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oracles', '0006_auto_20160816_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='I_O',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('type', models.CharField(max_length=16)),
                ('indexed', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(blank=True, max_length=16)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterField(
            model_name='contract',
            name='interface',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oracles.Interface'),
        ),
        migrations.AddField(
            model_name='i_o',
            name='inputs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='oracles.Interface'),
        ),
        migrations.AddField(
            model_name='i_o',
            name='outputs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='oracles.Interface'),
        ),
    ]
