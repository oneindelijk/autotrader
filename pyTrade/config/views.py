from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
# Create your views here.

from .models import SettingsPage, Setting

def index(request):
    
    context = {'SettingsPage': SettingsPage}
    return render(request, 'config/index.html', context)

class IndexView(generic.ListView):
    context_object_name = 'settings_index_page'
    template_name = 'config/index.html'
    model = SettingsPage

class DetailView(generic.DetailView):
    model = Setting
    template_name = 'config/detail.html'