# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pagos', views.listar_pagos, name='listar_pagos'),
    path('crear/', views.crear_pago, name='crear_pago'),
]