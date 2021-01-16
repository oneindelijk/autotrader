from django.shortcuts import render
from .models import Portofolio
# Create your views here.

def index(request):
    
    context = {'Portofolio': Portofolio}
    return render(request, 'portofolio/index.html', context)