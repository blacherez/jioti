# Generated by Django 2.1.4 on 2019-01-03 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0016_auto_20190103_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etape',
            name='etape_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='licorne',
            name='creation_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Date de création'),
        ),
    ]