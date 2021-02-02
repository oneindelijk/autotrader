import django_tables2 as tables
from .models import Company

class CompanyTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='marked', attrs={
            'th':{"class": "column-header select-column",
                'input':{"id": "select-all"}},
            'td':{"class": "column-header select-column"},
            # 'tr':{"class": "coompanyrow"}

    })
    symbol = tables.Column(accessor='symbol', attrs={
                'td':{"class": "column-header symbol-column"},
                'th':{"class": "column-header symbol-column "}})
    name = tables.Column(accessor='name',initial_sort_descending = True, attrs={
                'td':{"class": "name-column"},
                'th':{"class": "name-column"}})
    class Meta:
        model = Company
        # template_name = "django_tables2/bootstrap.html"
        fields = ("select","symbol","name", "last_sale","sector" ,"industry" ,"country" )

        # symbol_cqs
        # symbol_nasdaq
        # etf
        # market_category
        # last_sale
        # net_change
        # relative_change
        # country
        # ipo_year
        # volume
        # sector
        # industry
        # marked
        # favorite
        # bought
        # sell
        # watched