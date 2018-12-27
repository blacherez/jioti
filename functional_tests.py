from selenium import webdriver
import os
import unittest

# Pour gecko
os.environ["PATH"] += ":."
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_connect_to_the_app(self):
        # On accède à la page d'accueil
        self.browser.get('http://localhost:8000')
        # Il y a Jiji dans le titre de la page
        self.assertIn('Jiji', self.browser.title) #
        self.fail('Finish the test!') #



if __name__ == '__main__': #
    unittest.main(warnings='ignore')
