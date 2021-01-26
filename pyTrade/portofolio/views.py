from django.shortcuts import render

# Create your views here.

from .models import Portofolio

def index(request):
    pass
    context = {'Portofolio': Portofolio}
    return render(request, 'portofolio/index.html', context)

