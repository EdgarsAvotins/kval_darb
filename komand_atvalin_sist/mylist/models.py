from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

MERKIS_CHOICES = (
    ('komandejums', 'Komandejums'),
    ('atvalinajums', 'Atvalinajums'),
)

class Ieraksts(models.Model):
    lietotajs = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    merkis = models.CharField(max_length=20, choices=MERKIS_CHOICES)
    datums_no = models.DateField(null=True, blank=True)
    datums_lidz = models.DateField(null=True, blank=True)

    # tdelta = datums_lidz - datums_no
    # dienas = models.IntegerField(default=tdelta)

    vieta = models.CharField(max_length=50, null=True, blank=True)
    statuss = models.BooleanField(default=False)

    def __str__(self):
        return str(self.lietotajs) + ' ' + str(self.merkis) + ' ' + str(self.datums_no) + ' - ' + str(self.datums_lidz)

class Komandejums(models.Model):
    ieraksts = models.ForeignKey('Ieraksts', on_delete=models.CASCADE)
    atskaite = models.FileField()
    ceks = models.FileField()

    def __str__(self):
        return str(self.ieraksts)

class Atvalinajums(models.Model):
    ieraksts = models.ForeignKey('Ieraksts', on_delete=models.CASCADE)
    iesniegums = models.FileField()

    def __str__(self):
        return str(self.ieraksts)