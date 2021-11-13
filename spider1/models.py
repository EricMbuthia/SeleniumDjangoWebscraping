from typing import ChainMap
from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# from datetime import datetime
# from dateutil import tz
# Create your models here.
class ScrapeRecordsInventory(models.Model):
    rec_date = CharField( max_length=30)
    time_rec =  DateTimeField(default= timezone.now, blank=True )#CharField(max_length=150, default = "None")


    def __str__(self):
        return self.id 
 
class ScrapeRecords(models.Model):
    owners_name =CharField(max_length= 100)
    property_value_current_year =  CharField(max_length=100)
    property_value_next_year = CharField(max_length=100)
    tax_value = CharField(max_length=100)
    billing_address =  CharField( max_length= 500, default="None")
    link = CharField(max_length= 300, default="None")
    borough = CharField(max_length = 100, default="None")
    block = CharField(max_length=100, default="None")
    lot = CharField(max_length= 100, default="None")
    record_ref = ForeignKey(ScrapeRecordsInventory, on_delete=models.CASCADE)

    def __str__(self):
        return self.owners_name
class UndoneNotices(models.Model):
    borough = CharField(max_length= 100, default="None")
    block = CharField(max_length= 100, default = "None")
    lot = CharField(max_length=100, default = "None" )
    exception_type = CharField(max_length=200, default="None")
    billing_address =  CharField( max_length= 500, default="None")
    # time_exception =  DateTimeField(default= datetime.now(tz=tz.gettz()), blank=True )#CharField(max_length=150, default = "None")
    time_exception =  DateTimeField(default= timezone.now, blank=True)#CharField(max_length=150, default = "None")

    scrape_rec = ForeignKey(ScrapeRecordsInventory, on_delete = models.CASCADE )
    exception_info = TextField(default = "NULL")

    def __str__(self):
        return str(self.exception_type)