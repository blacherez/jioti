# Generated by Django 2.1.4 on 2019-01-01 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0009_auto_20190101_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='etape',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etape',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]