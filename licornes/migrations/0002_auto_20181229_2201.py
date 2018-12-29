# Generated by Django 2.1.4 on 2018-12-29 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('licornes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etape',
            name='auteur',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etape',
            name='media',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='licorne',
            name='createur',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]