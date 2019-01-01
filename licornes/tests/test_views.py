from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from licornes.models import Licorne
from licornes.models import User

from bs4 import BeautifulSoup

class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # On crée des utilisateurs et on leur attribue x licornes à chacun
        number_of_creators = 2
        number_of_licornes = 3
        cls.total_licornes = number_of_creators * number_of_licornes

        for user_id in range(number_of_creators):
            User.objects.create(username=f"utilisateur {user_id}")
            u = User.objects.get(username=f"utilisateur {user_id}")

            for licorne_id in range(number_of_licornes):
                Licorne.objects.create(
                    nom=f'Licorne {licorne_id} de {user_id}',
                    identifiant=f'{user_id}-{licorne_id}',
                    createur=u,
                    )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/licornes/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'licornes/index.html')

    def test_licornes_are_present(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('meslicornes' in response.context)
        #self.assertTrue(response.context['meslicornes'] == True)
        self.assertTrue(len(response.context['meslicornes']) == self.total_licornes)
        #print(str(response.content))
        self.assertInHTML("Licorne 0 de 0", str(response.content))

    def test_titres_present(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Mes licornes", str(response.content))
        self.assertInHTML("Trajet", str(response.content))

    def test_bouton_ajouter_present(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("+ Ajouter une licorne" in str(response.content))


    # def test_lists_all_authors(self):
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(reverse('authors')+'?page=2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertTrue(len(response.context['author_list']) == 3)
class AddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/licornes/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'licornes/licorne_form.html')

    def test_view_titre(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Ajouter une licorne" in str(response.content))

    def test_view_fields_presents(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Nom" in str(response.content))
        self.assertTrue("Identifiant" in str(response.content))
        self.assertTrue("Photo" in str(response.content))
        self.assertFalse("+ Ajouter une licorne" in str(response.content))

class EtapeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.identifiant_existant = "777"
        cls.identifiant_inexistant = "666"
        User.objects.create(username=f"kuala")
        u = User.objects.get(username=f"kuala")

        Licorne.objects.create(
            nom=f'Licorne de {u}',
            identifiant=f'{cls.identifiant_existant}',
            createur=u,
            )

    # On ne peut plus utiliser la version sans argument
    def test_view_url_returns_404_if_no_licorne(self):
        response = self.client.get('/licornes/etape/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_by_name_404_if_no_licorne(self):
        response = self.client.get(reverse('etape'))
        self.assertEqual(response.status_code, 404)

    # Version avec argument
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/licornes/etape/%s/' % (self.identifiant_existant))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'licornes/etape_form.html')

    def test_view_titre(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        h1 = soup.h1.string
        self.assertEqual(h1, "Ajouter une étape")

    def test_view_fields_presents(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        lbls = soup.find_all("label")
        labels = []
        for l in lbls:
            labels.append(l["for"])
        self.assertTrue("id_licorne" in labels)
        self.assertTrue("id_localisation" in labels)
        self.assertTrue("id_current" in labels)
        self.assertTrue("id_auteur" in labels)
        self.assertTrue("id_media" in labels)

    def test_view_autocomplete_present(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        scripts = soup.find_all("script")
        autocomplete_in_src = False
        #print(scripts)
        for s in scripts:
            if s.has_attr("src"):
                src = s["src"]
                if "autocomplete.js" in src:
                    autocomplete_in_src = True
            #autocomplete_in_src = True
        self.assertTrue(autocomplete_in_src)

    def test_view_creer_si_inexistante(self):
        # Si l'identifiant de licorne fourni ne correspond pas à une licorne
        # existante, on propose de la créer
        response = self.client.get(reverse('etape', args=[self.identifiant_inexistant]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'licornes/creer.html')
        soup = BeautifulSoup(response.content, features="html.parser")
        t = soup.title
        self.assertTrue("J'irai où tu iras" in t)
        h1 = soup.h1.string
        self.assertTrue("Licorne inexistante" in h1)
