# Generated by Django 2.1.4 on 2019-01-02 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0014_licorne_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licorne',
            name='photo',
        ),
    ]