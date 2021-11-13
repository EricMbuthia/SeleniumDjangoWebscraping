from django.contrib import admin
from .models import ScrapeRecordsInventory,ScrapeRecords,UndoneNotices

# Register your models here.

admin.site.register(ScrapeRecordsInventory)
admin.site.register(ScrapeRecords)
admin.site.register(UndoneNotices)