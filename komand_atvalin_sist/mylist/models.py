from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Atvalinajums(models.Model):
    lietotajs = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datums_no = models.DateField(null=True, blank=True)
    datums_lidz = models.DateField(null=True, blank=True)

class Komandejums(models.Model):
    lietotajs = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datums_no = models.DateField(null=True, blank=True)
    datums_lidz = models.DateField(null=True, blank=True)
    valsts = models.CharField(max_length=50)
    pilseta = models.CharField(max_length=50)