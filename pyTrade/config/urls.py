from django.urls import path

from . import views
app_name = 'config'
urlpatterns = [
    path('<int:pk>/', views.SettingsPageView.as_view(), name='settingspage'),
    path('edit/<int:pk>', views.EditSettings.as_view(), name='edit'),  
    # path('operations/<int:balance_id>/', views.balance_detail, name='balance'),
    # path('<int:wallet_id>/add_valuta', views.add_valuta, name='add_valuta'),  
]