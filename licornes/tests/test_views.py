from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from licornes.models import Licorne
from licornes.models import User

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
