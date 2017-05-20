# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 18:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mylist', '0007_auto_20170519_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaglabatieLietotaji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lietotajs_pats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lietotajs_pats', to=settings.AUTH_USER_MODEL)),
                ('saglabatais_lietotajs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saglabatais_lietotajs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]