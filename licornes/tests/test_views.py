from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from licornes.models import Licorne
from licornes.models import User
from licornes.models import Etape

from bs4 import BeautifulSoup
import re
import os

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
        self.assertTrue("Licorne 0 de 0" in str(response.content))

    def test_licornes_ont_badge(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        h2s = soup.find_all("h2")
        badges_de_licornes = 0
        for h2 in h2s:
            if h2.span and "badge" in h2.span["class"]:
                badges_de_licornes += 1
        self.assertTrue(badges_de_licornes)
        self.assertEqual(badges_de_licornes, self.total_licornes)


    def test_titres_present(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Mes licornes", str(response.content))
        self.assertInHTML("Trajet", str(response.content))

    def test_bouton_ajouter_present(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("+ Ajouter une licorne" in str(response.content))

    def test_div_map_present(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        divs = soup.find_all("div")
        div_map_in_divs = False
        for d in divs:
            if d.has_attr("id") and d["id"] == "map":
                div_map_in_divs = True
        self.assertTrue(div_map_in_divs)

    def test_liens_vers_licornes_presents(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        a = soup.find_all("a")
        lien_vers_1_dans_liens = False
        for l in a:
            if "licorne/1" in l["href"]:
                lien_vers_1_dans_liens = True
                break
        self.assertTrue(lien_vers_1_dans_liens)

    def test_aucune_licorne_nest_active(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        a = soup.find_all("a")
        active_in_a_class = 0
        for l in a:
            if l.has_attr("class"):
                classes = l["class"]
                if "active" in classes:
                    active_in_a_class += 1
        self.assertFalse(active_in_a_class)

    def test_pas_de_polyline(self):
        response = self.client.get(reverse('index'))
        self.assertFalse("google.maps.Polyline" in str(response.content))


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
        self.assertFalse("Photo" in str(response.content))
        self.assertTrue("Image" in str(response.content))
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
        cls.u = u
        cls.l = Licorne.objects.get(identifiant=cls.identifiant_existant)

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
        licorne = Licorne.objects.get(identifiant=self.identifiant_existant)
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        h1 = soup.h1.string
        self.assertEqual(h1, "Ajouter une étape pour %s" % (licorne))

    def test_view_fields_presents(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        lbls = soup.find_all("label")
        labels = []
        for l in lbls:
            labels.append(l["for"])
        self.assertTrue("id_localisation" in labels)
        self.assertFalse("id_current" in labels)
        self.assertTrue("id_auteur" in labels)
        self.assertTrue("id_media" in labels)

        # Champ input hidden pour la licorne
        inputs = soup.find_all("input")
        licorne_in_hidden_field = False
        for i in inputs:
            if i["type"] == "hidden" and i["name"] == "licorne":
                licorne_in_hidden_field = True
                break
        self.assertTrue(licorne_in_hidden_field)

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
        a = soup.find_all("a")
        add_in_href = False
        for l in a:
            if "/add" in l["href"]:
                add_in_href = True
        self.assertTrue(add_in_href)
        self.assertTrue(f"{self.identifiant_inexistant}" in str(response.content))

    def test_form_etape_valeur_initiale_licorne(self):
        response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        self.assertEqual(response.status_code, 200)
        licorne = Licorne.objects.get(identifiant=self.identifiant_existant)
        self.assertEqual(response.context['form'].initial['licorne'], licorne)

    def test_redirects_to_index_on_success(self):
        #response = self.client.get(reverse('etape', args=[self.identifiant_existant]))
        #self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('etape', args=[self.l.identifiant]), {"localisation": "Pau, France", "auteur": self.u.id, "media": "Tagalok", "licorne": self.l.id})
        self.assertRedirects(response, reverse('index'))

    def test_form_invalid_licorne(self):
        wrong_id = 78787897873
        response = self.client.post(reverse('etape', args=[self.l.identifiant]), {"localisation": "Pau, France", "auteur": self.u.id, "media": "Tagalok", "licorne": wrong_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'licorne', 'Sélectionnez un choix valide. Ce choix ne fait pas partie de ceux disponibles.')

    def test_form_invalid_localisation(self):
        response = self.client.post(reverse('etape', args=[self.l.identifiant]), {"localisation": "", "auteur": self.u.id, "media": "Tagalok", "licorne": self.l.id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'localisation', 'Ce champ est obligatoire.')

    def test_form_invalid_auteur(self):
        wrong_id = 78787897873
        response = self.client.post(reverse('etape', args=[self.l.identifiant]), {"localisation": "Pau, France", "auteur": wrong_id, "media": "Tagalok", "licorne": self.l.id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'auteur', 'Sélectionnez un choix valide. Ce choix ne fait pas partie de ceux disponibles.')
    # def test_form_invalid_renewal_date_future(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
    #     response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')


class LicorneViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # On crée des utilisateurs et on leur attribue x licornes à chacun
        number_of_creators = 2
        number_of_licornes = 3
        cls.total_licornes = number_of_creators * number_of_licornes

        cls.licornes_de_test = []

        for user_id in range(number_of_creators):
            User.objects.create(username=f"utilisateur {user_id}")
            u = User.objects.get(username=f"utilisateur {user_id}")

            for licorne_id in range(number_of_licornes):
                Licorne.objects.create(
                    nom=f'Licorne {licorne_id} de {user_id}',
                    identifiant=f'{user_id}-{licorne_id}',
                    createur=u,
                    image=f'{licorne_id}.png',
                    )
                cls.licornes_de_test.append(Licorne.objects.latest("id"))

    def test_view_url_exists_at_desired_location(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(f'/licornes/licorne/{id_lic}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirected_if_no_trailing_slash(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(f'/licornes/licorne/{id_lic}')
        self.assertEqual(response.status_code, 301)


    def test_view_url_accessible_by_name(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'licornes/licorne.html')

    def test_licornes_are_present(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('meslicornes' in response.context)
        #self.assertTrue(response.context['meslicornes'] == True)
        self.assertTrue(len(response.context['meslicornes']) == self.total_licornes)
        #print(str(response.content))
        self.assertTrue("Licorne 0 de 0" in str(response.content))

    def test_titres_present(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Mes licornes" in str(response.content))
        self.assertInHTML("Trajet", str(response.content))

    def test_bouton_ajouter_present(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("+ Ajouter une licorne" in str(response.content))

    def test_div_map_present(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        soup = BeautifulSoup(response.content, features="html.parser")
        divs = soup.find_all("div")
        div_map_in_divs = False
        for d in divs:
            if d.has_attr("id") and d["id"] == "map":
                div_map_in_divs = True
        self.assertTrue(div_map_in_divs)

    def test_liens_vers_licornes_presents(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        soup = BeautifulSoup(response.content, features="html.parser")
        a = soup.find_all("a")
        lien_vers_1_dans_liens = False
        for l in a:
            if "licorne/1" in l["href"]:
                lien_vers_1_dans_liens = True
                break
        self.assertTrue(lien_vers_1_dans_liens)

    def test_une_licorne_est_active(self):
        id_lic = self.licornes_de_test[3].id
        response = self.client.get(reverse('licorne', args=[id_lic]))
        soup = BeautifulSoup(response.content, features="html.parser")
        a = soup.find_all("a")
        active_in_a_class = 0
        for l in a:
            if l.has_attr("class"):
                classes = l["class"]
                if "active" in classes:
                    active_in_a_class += 1
        self.assertTrue(active_in_a_class)
        self.assertEqual(active_in_a_class, 1)

    def test_licornes_ont_badge(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        h2s = soup.find_all("h2")
        badges_de_licornes = 0
        for h2 in h2s:
            if h2.span and "badge" in h2.span["class"]:
                badges_de_licornes += 1
        self.assertTrue(badges_de_licornes)
        self.assertEqual(badges_de_licornes, self.total_licornes)

    def test_licornes_ont_image(self):
        response = self.client.get(reverse('index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        lics = soup.find_all(attrs={"class": "list-group-item"})
        lic_img = 0
        bons_noms_dimages = 0
        for l in lics:
            numero = re.sub("Licorne ([0-9]+).*", "\\1", l.h2.text, re.M)[0:4].strip()
            if l.img:
                lic_img += 1
                if os.path.basename(l.img["src"]) == f'{numero}.png':
                    bons_noms_dimages += 1
        self.assertTrue(lic_img)
        self.assertTrue(bons_noms_dimages)
        self.assertEqual(lic_img, len(lics))
        self.assertEqual(bons_noms_dimages, len(lics))



class MediaViewTest(TestCase):
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
        l = Licorne.objects.get(nom=f'Licorne de {u}')
        e0 = Etape.objects.create(licorne=l, auteur=u, localisation="Paris, France")
        e0.save()
        e1 = Etape.objects.create(licorne=l, auteur=u, localisation="Berlin, Allemagne")
        e1.save()
        e2 = Etape.objects.create(licorne=l, auteur=u, localisation="San Francisco")
        e2.save()

    # Version avec argument
    def test_view_url_exists_at_desired_location(self):
        e1 = Etape.objects.get(localisation="Berlin, Allemagne")
        u = '/licornes/media/%s/' % (e1.id)
        response = self.client.get(u)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        e1 = Etape.objects.get(localisation="Berlin, Allemagne")
        response = self.client.get(reverse('media', args=[e1.id]))
        self.assertEqual(response.status_code, 200)

    def test_404_if_nonexistant_id(self):
        response = self.client.get(reverse('media', args=[11111111]))
        self.assertEqual(response.status_code, 404)
