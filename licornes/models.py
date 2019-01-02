from django.db import models
from datetime import date

# Create your models here.

#from django.contrib.auth.models import User
from django.conf import settings

import googlemaps


def geocode(lieu):
    gmaps = googlemaps.Client(key=settings.GOOGLE_SECRET)
    # Geocoding an address
    geocode_result = gmaps.geocode(lieu)
    return geocode_result[0]["geometry"]["location"]


class Licorne(models.Model):
    nom = models.CharField(max_length=50)
    creation_date = models.DateField('Date de création', default=date.today)
    photo = models.CharField(max_length=200, null=True, blank=True)
    identifiant = models.CharField(max_length=50, unique=True)
    createur = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nom

    def getEtapes(self):
        etapes = Etape.objects.filter(licorne=self).order_by("-etape_date")
        return etapes

class Etape(models.Model):
    licorne = models.ForeignKey(Licorne, on_delete=models.CASCADE)
    etape_date = models.DateField(default=date.today)
    localisation = models.CharField(max_length=200, null=True, blank=True)
    current = models.BooleanField(default=False)
    auteur = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
    media = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return ("Etape de %s (%s)" % (self.licorne.nom, self.etape_date))

    def getCoords(self):
        return '{lat: %s, lng : %s}' % (self.latitude, self.longitude)

    def save(self, *args, **kwargs):
        if self.localisation:
            coord = geocode(self.localisation)
            self.latitude = coord["lat"]
            self.longitude = coord["lng"]
        else:
            self.latitude = None
            self.longitude = None
        super(Etape, self).save(*args, **kwargs)

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def CommonName(self):
        if self.first_name:
            return "%s %s." % (self.first_name, self.last_name[0])
        else:
            return self.username
