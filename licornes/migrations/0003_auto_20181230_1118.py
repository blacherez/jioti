# Generated by Django 2.1.4 on 2018-12-30 10:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0002_auto_20181229_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licorne',
            name='creation_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date de création'),
        ),
        migrations.AlterField(
            model_name='licorne',
            name='photo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
