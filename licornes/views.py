#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Licorne

def index(request):
    #return HttpResponse("Hello, world. You're at the unicorns index.")

    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('licornes/index.html')
    context = {
        'latest_question_list': 0,
    }
    return HttpResponse(template.render(context, request))
