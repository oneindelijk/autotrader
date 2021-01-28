from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
# Create your views here.

from .models import Portofolio, Company

items_per_page = 25 # Todo: get value from settings database

def get_extra_content(active_id):
    pages = ['index', 'companies']
    Pages = []
    for i,p in enumerate(pages):
        Pages.append({'active': i + 1 == active_id,
                      'id': i + 1, 
                      'link':'portofolio:' + p,
                      'title': p[0].upper() + p[1:]
                      })
    return {'pages_list':Pages, 'app':'portofolio'}


def index(request):
    context = {'Portofolio': Portofolio.objects.all()}
    context.update(get_extra_content(1))
    # model = Portofolio
    # print(context)
    return render(request, 'portofolio/index.html', context)

class CompanyListing(generic.ListView):
    template_name = 'portofolio/companies.html'
    model = Company
    #paginate_by = items_per_page
    # if 'order' in kwargs:
    #     print('KWARGS:', kwargs)

    def get_context_data(self, **kwargs):
        # print('KWARGS:', kwargs)
        context = super().get_context_data(**kwargs)
        # print(self.__dict__)
        context.update(get_extra_content(2))
        # print(context['view'].request.GET)
        return context

    def get_queryset(self, **kwargs):
        # print(self.__dict__)
        filter = self.request.GET.get('filter')
        if filter:
            if '%' in filter or '*' in filter:
                if filter[0] == '%' and filter[-1] == '%':
                    return Company.objects.filter(symbol__icontains = filter.strip('%').strip('*'))
                elif filter[-1] == '%':
                    return Company.objects.filter(symbol__istartswith = filter.strip('%').strip('*'))
                elif filter[0] == '%':
                    return Company.objects.filter(symbol__iendswith = filter.strip('%').strip('*'))
                else:
                    return Company.objects.filter(symbol = filter)
            else:
                return Company.objects.filter(symbol = filter)
        else:
            return Company.objects.all()
    # def get_ordering(self):
    #     ordering = self.request.GET.get('ordering', 'symbol')
    #     return ordering

def refresh_companies(request):
    C = Company()
    C.refresh_companies()
    print('Companies refreshed')
    return HttpResponseRedirect(reverse('portofolio:companies'))

def filter_companies(request, filter = ''):
    if 'filter' in request.GET:
        # Todo: subroutine om complexe filters te formuleren
        Filter = request.GET['filter']
    return HttpResponse(reverse('portofolio:filter_companies')) #, args=('filter=' + Filter,) )) # 
