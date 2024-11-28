from django.urls import path
from . import views


app_name = 'clients'

urlpatterns = [
    path('', views.listar_clientes, name='list_clients'),
    path('crear/', views.crear_cliente, name='create_client'),
    path('actualizar/<int:pk>/', views.actualizar_cliente, name='update_client'),
    path('borrar/<int:pk>/', views.borrar_cliente, name='erase_client'),
]