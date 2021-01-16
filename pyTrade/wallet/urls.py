from django.urls import path

from . import views
app_name = 'wallet'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wallet_id>/', views.detail, name='detail'),  
    path('operations/<int:balance_id>/', views.balance_detail, name='balance'),
    path('<int:wallet_id>/add_valuta', views.add_valuta, name='add_valuta'),  
]