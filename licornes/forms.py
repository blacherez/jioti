from django.forms import ModelForm
from django.forms import HiddenInput
from licornes.models import Etape

# Create the form class.
class EtapeForm(ModelForm):
    class Meta:
        model = Etape
        fields = ['licorne', 'localisation', 'auteur', 'media']
        widgets = {'licorne': HiddenInput()}
