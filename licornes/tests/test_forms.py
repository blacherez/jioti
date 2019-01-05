from django.test import TestCase

# Create your tests here.
#import datetime

#from django.utils import timezone
from licornes.models import Licorne
from licornes.models import User
from licornes.models import Etape

from licornes.forms import EtapeForm

class EtapeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username="prof")
        u = User.objects.get(username="prof")
        cls.u = u
        cls.identifiant_utilise = '77898787676867'
        Licorne.objects.create(nom='Chamallow', identifiant=cls.identifiant_utilise, createur=u)
        cls.l = Licorne.objects.get(nom="Chamallow")

    def test_etape_form_complet_valide(self):
        form = EtapeForm({"localisation": "Pau, France", "auteur": self.u.id, "licorne": self.l.id, "media": "Tagalok"})
        self.assertTrue(form.is_valid())

    def test_etape_form_localisation_label(self):
        form = EtapeForm()
        self.assertTrue(form.fields['localisation'].label == None or form.fields['localisation'].label == 'Localisation')

    def test_etape_form_localisation_help_text(self):
        form = EtapeForm()
        self.assertEqual(form.fields['localisation'].help_text, '<br />Saisissez une ville ou un pays, le champ se complètera automatiquement.')

    def test_etape_form_localisation_non_vide(self):
        form = EtapeForm({"localisation": "", "auteur": self.u.id, "licorne": self.l.id})
        self.assertFalse(form.is_valid())

    def test_etape_form_auteur_label(self):
        form = EtapeForm()
        self.assertEqual(form.fields['auteur'].label, 'Auteur')

    def test_etape_form_auteur_help_text(self):
        form = EtapeForm()
        self.assertEqual(form.fields['auteur'].help_text, "<br />Ce champ n'existe que pendant le temps de développement. Par la suite, il sera rempli automatiquement.")

    def test_etape_form_auteur_non_vide(self):
        form = EtapeForm({"localisation": "Pau, France", "auteur": "", "licorne": self.l.id})
        self.assertFalse(form.is_valid())

    def test_etape_form_media_label(self):
        form = EtapeForm()
        self.assertEqual(form.fields['media'].label, "Media")

    def test_etape_form_media_label(self):
        form = EtapeForm()
        self.assertEqual(form.fields['media'].help_text, "<br />Ecrivez ici le code embed d'une vidéo.")

    def test_etape_form_media_peut_etre_vide(self):
        form = EtapeForm({"localisation": "Pau, France", "auteur": self.u.id, "licorne": self.l.id, "media": ""})
        self.assertTrue(form.is_valid())

    def test_etape_form_licorne_field(self):
        form = EtapeForm()
        self.assertTrue(form.fields['licorne'].widget.is_hidden)

    def test_etape_form_licorne_non_vide(self):
        form = EtapeForm({"localisation": "Pau, France", "auteur": self.u.id, "": self.l.id, "media": "Tagalok"})
        self.assertFalse(form.is_valid())
