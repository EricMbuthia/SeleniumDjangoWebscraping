# Generated by Django 3.2.4 on 2021-11-01 06:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('spider1', '0003_undonenotices'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraperecordsinventory',
            name='time_rec',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 1, 6, 37, 10, 289980, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='undonenotices',
            name='billing_address',
            field=models.CharField(default='None', max_length=500),
        ),
        migrations.AddField(
            model_name='undonenotices',
            name='exception_info',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='undonenotices',
            name='scrape_rec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider1.scraperecordsinventory'),
        ),
        migrations.AlterField(
            model_name='undonenotices',
            name='time_exception',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 1, 6, 37, 10, 290978, tzinfo=utc)),
        ),
    ]
