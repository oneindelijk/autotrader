import django_filters
from .models import Company
import re
class CompanyFilter(django_filters.FilterSet):
    symbol = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['id']

def filter_parser(get_request):
    fields=['symbol','name']
    filter_string = get_request.get('filter')
    searchdict = {}
    if filter_string:
        print (filter_string)
        if not '=' in filter_string:
            searchdict['symbol'] = filter_string
    
        else:

            searchdict = split_search_constituents(filter_string)
    
    return searchdict
        
            
def split_search_constituents(filter_string):
    ''' create a dictionnary from a string with 'field = value &' syntax '''
    tmpl = {}
    params = filter_string.split('&')
    for p in params:
        try:
            k, v = p.split('=')
        except:
            print("Error in searchstring `{}`".format(p))
        else:
            tmpl.update({k.strip(' '):v.strip(' ')})
    return tmpl