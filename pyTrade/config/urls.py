from django.urls import path

from . import views
app_name = 'config'
urlpatterns = [
    path('<int:pk>/', views.SettingsPageView.as_view(), name='settingspage'),
    # path('<int:wallet_id>/', views.detail, name='detail'),  
    # path('operations/<int:balance_id>/', views.balance_detail, name='balance'),
    # path('<int:wallet_id>/add_valuta', views.add_valuta, name='add_valuta'),  
]