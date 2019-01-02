from django.test import TestCase

from django.db import IntegrityError

# Create your tests here.
from licornes.models import Licorne
from licornes.models import User
from licornes.models import Etape

from datetime import date

def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

class LicorneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username="prof")
        u = User.objects.get(username="prof")
        cls.u = u
        cls.identifiant_utilise = '77898787676867'
        Licorne.objects.create(nom='Chamallow', identifiant=cls.identifiant_utilise, createur=u)

    def test_label_nom(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        field_label = licorne._meta.get_field('nom').verbose_name
        self.assertEquals(field_label, 'nom')

    def test_label_creation_date(self):
        licorne=Licorne.objects.get(identifiant=self.identifiant_utilise)
        field_label = licorne._meta.get_field('creation_date').verbose_name
        self.assertEquals(field_label, 'Date de création')

    def test_max_length_nom(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        max_length = licorne._meta.get_field('nom').max_length
        self.assertEquals(max_length, 50)

    def test_no_photo_field(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        self.assertFalse(hasattr(licorne, "photo"))

    def test_max_length_identifiant(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        max_length = licorne._meta.get_field('identifiant').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_nom(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        expected_object_name = f'{licorne.nom}'
        self.assertEquals(expected_object_name, str(licorne))

    def test_creation_date_est_date_du_jour_par_defaut(self):
        licorne = Licorne.objects.get(identifiant=self.identifiant_utilise)
        expected_date = date.today()
        self.assertEquals(expected_date, licorne.creation_date)
        # def test_get_absolute_url(self):

    def test_identifiant_est_unique(self):
        creation_echoue = False
        try:
            Licorne.objects.create(nom='Chabooky', identifiant=self.identifiant_utilise, createur=self.u)
        except IntegrityError:
            creation_echoue = True
        self.assertTrue(creation_echoue)

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
        Etape.objects.create(licorne=l, auteur=u, localisation="Paris, France")

    def test_object_name(self):
        licorne = Licorne.objects.get(identifiant='77898787676867')
        etape = Etape.objects.get(id=1)
        expected_object_name = f'Etape de {licorne.nom} ({etape.etape_date})'
        self.assertEquals(expected_object_name, str(etape))

    def test_max_length_localisation(self):
        etape = Etape.objects.get(id=1)
        max_length = etape._meta.get_field('localisation').max_length
        self.assertEquals(max_length, 200)

    def test_max_length_media(self):
        etape = Etape.objects.get(id=1)
        max_length = etape._meta.get_field('media').max_length
        self.assertEquals(max_length, None)

    def test_latitude_est_numerique(self):
        etape = Etape.objects.get(id=2)
        lat = etape.latitude
        self.assertTrue(is_number(lat))

    def test_longitude_est_numerique(self):
        etape = Etape.objects.get(id=2)
        long = etape.latitude
        self.assertTrue(is_number(long))


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username="prof")

    def test_common_name_est_prenom_et_initiale_du_nom(self):
        u = User.objects.get(username="prof")
        #initiale = u.last_name[0]
        u.first_name = "Maîtresse"
        u.last_name = "Lucie"
        u.save()
        expected_name = f'{u.first_name} {u.last_name[0]}.'
        self.assertEquals(expected_name, u.CommonName())

    def test_common_name_est_login_si_prenom_vide(self):
        u = User.objects.get(username="prof")
        expected_name = f'{u.username}'
        self.assertEquals(expected_name, u.CommonName())
