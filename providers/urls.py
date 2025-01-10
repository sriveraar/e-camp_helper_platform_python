from django.urls import path
from . import views

urlpatterns = [
    path('', views.v_index, name='index'),
    path('crear-cuenta/', views.v_crear_cuenta, name='create_account'),
    path('iniciar-sesion/', views.v_iniciar_sesion, name='login'),
    path('mi-cuenta/', views.v_mi_cuenta, name='account'),
    path('proveedor/<str:email>/', views.v_detalle_proveedor, name='provider_detail'),
    path('mi-cuenta/incluir-servicio/', views.v_cuenta_incluir_servicio, name='add_service'),
    path('mi-cuenta/remover-servicio/', views.v_cuenta_remover_servicio, name='remove_service'),
]
