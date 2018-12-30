from django.test import TestCase

# Create your tests here.
from licornes.models import Licorne
from licornes.models import User
from licornes.models import Etape

from datetime import date

class LicorneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username="prof")
        u = User.objects.get(username="prof")
        Licorne.objects.create(nom='Chamallow', identifiant='77898787676867', createur=u)

    def test_label_nom(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        field_label = licorne._meta.get_field('nom').verbose_name
        self.assertEquals(field_label, 'nom')

    def test_label_creation_date(self):
        licorne=Licorne.objects.get(identifiant='77898787676867')
        field_label = licorne._meta.get_field('creation_date').verbose_name
        self.assertEquals(field_label, 'Date de création')

    def test_max_length_nom(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        max_length = licorne._meta.get_field('nom').max_length
        self.assertEquals(max_length, 200)

    def test_max_length_photo(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        max_length = licorne._meta.get_field('photo').max_length
        self.assertEquals(max_length, 200)

    def test_max_length_identifiant(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        max_length = licorne._meta.get_field('identifiant').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_nom(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        expected_object_name = f'{licorne.nom}'
        self.assertEquals(expected_object_name, str(licorne))

    def test_creation_date_est_date_du_jour_par_defaut(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        expected_date = date.today()
        self.assertEquals(expected_date, licorne.creation_date)
        # def test_get_absolute_url(self):

    #     author = Author.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(author.get_absolute_url(), '/catalog/author/1')

class EtapeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username="prof")
        u = User.objects.get(username="prof")
        Licorne.objects.create(nom='Chamallow', identifiant='77898787676867', createur=u)
        l = Licorne.objects.get(identifiant='77898787676867')
        Etape.objects.create(licorne=l, auteur=u)

    def test_object_name(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        etape = Etape.objects.get(id=1)
        expected_object_name = f'Etape de {licorne.nom} ({etape.etape_date})'
        self.assertEquals(expected_object_name, str(etape))

    def test_max_length_localisation(self):
        etape = Etape.objects.get(id=1)
        max_length = etape._meta.get_field('localisation').max_length
        self.assertEquals(max_length, 100)

    def test_max_length_localisation(self):
        etape = Etape.objects.get(id=1)
        max_length = etape._meta.get_field('media').max_length
        self.assertEquals(max_length, 200)
