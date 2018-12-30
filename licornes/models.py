from django.db import models
from datetime import date

# Create your models here.

#from django.contrib.auth.models import User
from django.conf import settings


class Licorne(models.Model):
    nom = models.CharField(max_length=50)
    creation_date = models.DateField('Date de création', default=date.today)
    photo = models.CharField(max_length=200, null=True)
    identifiant = models.CharField(max_length=50)
    createur = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nom

class Etape(models.Model):
    licorne = models.ForeignKey(Licorne, on_delete=models.CASCADE)
    etape_date = models.DateField(default=date.today)
    localisation = models.CharField(max_length=200, null=True)
    current = models.BooleanField(default=False)
    auteur = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
    media = models.CharField(max_length=200, null=True)

    def __str__(self):
        return ("Etape de %s (%s)" % (self.licorne.nom, self.etape_date))

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def CommonName(self):
        return "%s %s." % (self.first_name, self.last_name[0])
