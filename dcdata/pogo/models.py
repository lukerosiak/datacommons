from django.db import models

class Contractor(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    contractor_ext_id = models.SmallIntegerField(null=True)

class Misconduct(models.Model):
    contractor = models.ForeignKey(Contractor)
    instance = models.CharField(max_length=255, blank=False, null=False)

    penalty_amount = models.BigIntegerField(null=True)

    contracting_party = models.CharField(max_length=255, blank=False, null=False)
    court_type = models.CharField(max_length=20, blank=True, null=True)

    date = models.DateField()
    date_significance = models.CharField(max_length=50, blank=True, null=False)
    date_year = models.SmallIntegerField(null=True)

    disposition = models.CharField(max_length=30, blank=True, null=False)
    enforcement_agency = models.CharField(max_length=255, blank=True, null=False)
    misconduct_type = models.CharField(max_length=32, blank=False, null=False)

    synopsis = models.TextField(blank=True)

    url = models.URLField(blank=False, null=False)

