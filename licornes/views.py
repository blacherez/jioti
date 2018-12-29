#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Licorne

def index(request):
    #return HttpResponse("Hello, world. You're at the unicorns index.")

    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    meslicornes = Licorne.objects.order_by("creation_date")
    template = loader.get_template('licornes/index.html')
    context = {
        'meslicornes': meslicornes,
    }
    return HttpResponse(template.render(context, request))
