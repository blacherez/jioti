#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404

from django.template import loader
from django.urls import reverse_lazy


from django.views.generic.edit import CreateView

from .models import Licorne
from .models import Etape
from .forms import EtapeForm
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

def etape(request, licorne=""):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EtapeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse_lazy("index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        if not licorne:
            raise Http404("Un identifiant de licorne doit être fourni.")
        else:
            try:
                licorne_active = Licorne.objects.get(identifiant=licorne)
            except Licorne.DoesNotExist:
                template = loader.get_template('licornes/creer.html')
                context = {"licorne": licorne}
                return HttpResponse(template.render(context, request))
            form = EtapeForm(initial={'licorne': licorne_active})
            context = {"form": form, "licorne": licorne_active}
            template = loader.get_template('licornes/etape_form.html')
    return HttpResponse(template.render(context, request))

class Add(CreateView):
    model = Licorne
    fields = ['nom', 'identifiant', 'photo', 'createur']
    success_url = reverse_lazy('index')
