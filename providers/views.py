from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Provider, Service

# Página principal
def v_index(request):
    """Página principal que lista todos los proveedores."""
    all_providers = Provider.objects.all()
    return render(request, 'providers/index.html', {'providers': all_providers})

# Registro de nuevos proveedores
def v_crear_cuenta(request):
    """Vista para registrar un nuevo proveedor."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'providers/create_account.html', {'form': form})

# Iniciar sesión
def v_iniciar_sesion(request):
    """Vista para iniciar sesión."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'providers/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

# Gestión del perfil del proveedor
@login_required
def v_mi_cuenta(request):
    """Vista para gestionar el perfil del proveedor."""
    provider = request.user
    if request.method == 'POST':
        provider.first_name = request.POST.get('first_name', provider.first_name)
        provider.last_name = request.POST.get('last_name', provider.last_name)
        provider.contact_number = request.POST.get('contact_number', provider.contact_number)
        provider.detailed_description = request.POST.get('detailed_description', provider.detailed_description)
        provider.save()
    return render(request, 'providers/account.html', {'provider': provider})

# Detalle del proveedor
def v_detalle_proveedor(request, email):
    """Vista para mostrar el detalle de un proveedor."""
    provider = get_object_or_404(Provider, email=email)
    return render(request, 'providers/provider_detail.html', {'provider': provider})

# Agregar servicio al perfil del proveedor
@login_required
def v_cuenta_incluir_servicio(request):
    """Vista para agregar un servicio al perfil del proveedor."""
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        request.user.services.add(service)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# Quitar servicio del perfil del proveedor
@login_required
def v_cuenta_remover_servicio(request):
    """Vista para eliminar un servicio del perfil del proveedor."""
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        request.user.services.remove(service)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
