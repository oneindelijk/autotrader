from django.shortcuts import render
from django.views import generic

# Create your views here.

from .models import Portofolio, Company

def get_pages_list(active_id):
    pages = ['index', 'companies']
    Pages = []
    for i,p in enumerate(pages):
        Pages.append({'active': i + 1 == active_id,
                      'id': i + 1, 
                      'link':'portofolio:' + p,
                      'title': p[0].upper() + p[1:]
                      })
    return Pages


def index(request):
    pages_list = get_pages_list(1)
    context = {'Portofolio': Portofolio, 'pages_list': pages_list}
    return render(request, 'portofolio/index.html', context)

class CompanyListing(generic.ListView):
    template_name = 'portofolio/companies.html'
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages_list = get_pages_list(2)
        context.update({'pages_list': pages_list})
        print(context)
        return context