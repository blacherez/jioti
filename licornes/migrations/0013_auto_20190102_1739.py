# Generated by Django 2.1.4 on 2019-01-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0012_auto_20190102_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etape',
            name='media',
            field=models.TextField(blank=True, null=True),
        ),
    ]