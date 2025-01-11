from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.v_index, name='index'),
    path('crear-cuenta/', views.v_crear_cuenta, name='create_account'),
    path('iniciar-sesion/', views.v_iniciar_sesion, name='login'),
    path('cerrar-sesion/', views.v_cerrar_sesion, name='logout'),
    path('mi-cuenta/', views.v_mi_cuenta, name='account'),
    path('proveedor/<str:email>/', views.v_detalle_proveedor, name='provider_detail'),
    path('mi-cuenta/incluir-servicio/', views.v_cuenta_incluir_servicio, name='add_service'),
    path('mi-cuenta/remover-servicio/', views.v_cuenta_remover_servicio, name='remove_service'),
    path('crear-perfil/', views.v_crear_perfil_proveedor, name='create_provider_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
