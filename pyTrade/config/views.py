from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
# Create your views here.

from .models import SettingsPage, Setting

# def index(request):
    
#     context = {'SettingsPage': SettingsPage}
#     return render(request, 'config/index.html', context)

def debug_dict(dct, extra = ''):
    ''' temp method to display dictionaries a little nicer '''
    xtra_len = len(extra)
    if xtra_len > 0:
        print(extra)
    for key in dct.keys():
        print("{}'{}'".format(''.ljust(xtra_len),key), dct[key])

class IndexView(generic.ListView):
    model = SettingsPage
    template_name = 'config/pageslist.html'
    context_object_name = 'pages'
    
class SettingsPageView(generic.DetailView):
    context_object_name = 'pages'
    template_name = 'config/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print (self.__dict__)
        settings = Setting.objects.filter(settingsPage = self.page)
        pages = SettingsPage.objects.all()
        context.update({'app':'config','settings': settings, 'pages': pages, 'active_page': self.page })
        
        debug_dict(context, 'CONTEXT')
        return context
    
    def get_queryset(self):
        self.page = get_object_or_404(SettingsPage, id=self.kwargs['pk'])
        return Setting.objects.filter(settingsPage=self.page)

class EditSettings(generic.UpdateView):
    queryset = Setting.objects.all()
    template_name = 'config/edit.html'