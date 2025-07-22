from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.wallet_list,      name='wallet_list'),
    path('new/',              views.wallet_create,    name='wallet_create'),
    path('<int:pk>/',         views.wallet_detail,    name='wallet_detail'),
    path('<int:pk>/add-json/',views.wallet_add_json,  name='wallet_add_json'),
    path('<int:pk>/add/',     views.transaction_create,name='transaction_create'),
    path('<int:pk>/statement/', views.wallet_statement, name='wallet_statement'),
    path('<int:pk>/topup/', views.wallet_topup, name='wallet_topup'),
    path('<int:pk>/delete/', views.wallet_delete, name='wallet_delete'),
]
