from django.forms import ModelForm
from licornes.models import Etape

# Create the form class.
class EtapeForm(ModelForm):
    class Meta:
        model = Etape
        fields = ['licorne', 'localisation', 'current', 'auteur', 'media']

