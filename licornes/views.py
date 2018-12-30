#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy


from django.views.generic.edit import CreateView

from .models import Licorne
from django.conf import settings


def index(request):
    #return HttpResponse("Hello, world. You're at the unicorns index.")

    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    meslicornes = Licorne.objects.order_by("creation_date")
    template = loader.get_template('licornes/index.html')
    context = {
        'meslicornes': meslicornes,
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
    }
    return HttpResponse(template.render(context, request))


class Add(CreateView):
    model = Licorne
    fields = ['nom', 'identifiant', 'photo', 'createur']
    success_url = reverse_lazy('index')
