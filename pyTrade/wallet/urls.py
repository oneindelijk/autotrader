from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wallet_id>/', views.detail, name='detail'),  
    path('bal<int:balance_id>/', views.balance_detail, name='balance'),  
]