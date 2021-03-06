from django.urls import path

from . import views
app_name = 'portofolio'
urlpatterns = [
    path('', views.index, name='index'),
    path('company-listing/', views.CompanyListing.as_view(), name = 'companies'),
    path('company-listing/comp_upd', views.refresh_companies, name='refresh_companies'), 
    # path('company-listing/?filter=', views.filter_companies, name='filter_companies'),  
    # path('<int:wallet_id>/', views.detail, name='detail'),  
    # path('operations/<int:balance_id>/', views.balance_detail, name='balance'),
    # path('<int:wallet_id>/add_valuta', views.add_valuta, name='add_valuta'),  
]

# 