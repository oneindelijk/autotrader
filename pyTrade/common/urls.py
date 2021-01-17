from django.urls import path
from django.conf.urls.static import static


# from . import views
app_name = 'common'
urlpatterns = [
    path('', static, name='index.html'),
    # path('<int:wallet_id>/', views.detail, name='detail'),  
    # path('operations/<int:balance_id>/', views.balance_detail, name='balance'),
    # path('<int:wallet_id>/add_valuta', views.add_valuta, name='add_valuta'),  
]