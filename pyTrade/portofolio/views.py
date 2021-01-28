from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import LazyPaginator
# Create your views here.

from .models import Portofolio, Company
from .tables import CompanyTable
from .filters import CompanyFilter, filter_parser

items_per_page = 35 # Todo: get value from settings database

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

class CompanyListing(SingleTableMixin, FilterView):
    template_name = 'portofolio/companies.html'
    model = Company
    table_class = CompanyTable
    filterset_class = CompanyFilter
    paginate_by = items_per_page
    # paginator_class = LazyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_extra_content(2))
        # print ('Request', self.request.GET)
        # Cps = Company.objects.all()
        # company_filter = CompanyFilter(self.request.GET, queryset = Cps)
        # context.update({'filter':company_filter})
        return context

    def get_queryset(self, **kwargs):
        filter_dict = filter_parser(self.request.GET)
        Cps = Company.objects.all()
        print(filter_dict)
        company_filter = CompanyFilter(filter_dict, queryset = Cps)
        # context.update({'table':company_filter.qs})
        # filter = self.request.GET.get('filter')
        # if filter:
        #     if '%' in filter or '*' in filter:
        #         if filter[0] == '%' and filter[-1] == '%':
        #             return Company.objects.filter(symbol__icontains = filter.strip('%').strip('*'))
        #         elif filter[-1] == '%':
        #             return Company.objects.filter(symbol__istartswith = filter.strip('%').strip('*'))
        #         elif filter[0] == '%':
        #             return Company.objects.filter(symbol__iendswith = filter.strip('%').strip('*'))
        #         else:
        #             return Company.objects.filter(symbol = filter)
        #     else:
        #         return Company.objects.filter(symbol = filter)
        # else:
        return company_filter.qs
            

def refresh_companies(request):
    C = Company()
    C.refresh_companies()
    print('Companies refreshed')
    return HttpResponseRedirect(reverse('portofolio:companies'))

def filter_companies(request):
    Cps = Company.objects.all()
    company_filter = CompanyFilter(request.GET, queryset = Cps)
    return render(request, 'search/companies_list.html')