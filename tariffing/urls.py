from django.urls import path
from . import views

app_name = "tariffing"

urlpatterns = [
    path("", views.consultar_tarifas, name="consultar_tarifas"),
]