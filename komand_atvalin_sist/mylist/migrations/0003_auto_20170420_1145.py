# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0002_remove_atvalinajums_something'),
    ]

    operations = [
        migrations.AddField(
            model_name='atvalinajums',
            name='datums_lidz',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='atvalinajums',
            name='datums_no',
            field=models.DateField(blank=True, null=True),
        ),
    ]
