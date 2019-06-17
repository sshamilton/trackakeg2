from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Keg
# Create your views here.
def index(request):
    template = loader.get_template('kegerator/index.html')
    keg = Keg()
    pints = keg.pints()
    percent = keg.percent()
    context = {
            'pints': pints,
            'percent': percent,
            }
    return HttpResponse(template.render(context))

