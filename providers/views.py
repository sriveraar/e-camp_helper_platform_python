from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Provider, Service
from .forms import ProviderForm
from django.contrib.auth import logout


# Página principal
def v_index(request):
    """Página principal que lista todos los proveedores."""
    all_providers = Provider.objects.all()
    return render(request, 'providers/index.html', {'providers': all_providers})

# Registro de nuevos proveedores
def v_crear_cuenta(request):
    """Vista para registrar un nuevo proveedor."""
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después de crear la cuenta
    else:
        form = ProviderForm()
    return render(request, 'providers/create_account.html', {'form': form})

# Vista para crear el perfil de proveedor
@login_required
def v_crear_perfil_proveedor(request):
    """Vista para que un usuario cree su perfil de proveedor."""
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            # Asignar el perfil de proveedor al usuario actual
            provider = form.save(commit=False)
            provider.user = request.user
            provider.save()
            return redirect('account')  # Redirige a la página de cuenta del proveedor
    else:
        form = ProviderForm()

    return render(request, 'providers/create_provider_profile.html', {'form': form})


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
    return render(request, 'providers/login.html')

# Gestión del perfil del proveedor
@login_required
def v_mi_cuenta(request):
    """Vista para gestionar el perfil del proveedor."""
    try:
        provider = request.user.provider_profile
    except Provider.DoesNotExist:
        # Redirige a la página de creación de perfil de proveedor
        return redirect('create_provider_profile')  # Redirige si no existe el perfil de proveedor

    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ProviderForm(instance=provider)
    messages = provider.messages.all()
    return render(request, 'providers/account.html', {'form': form, 'messages': messages})


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
        provider = request.user.provider_profile
        service = get_object_or_404(Service, id=service_id)
        provider.services.add(service)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# Quitar servicio del perfil del proveedor
@login_required
def v_cuenta_remover_servicio(request):
    """Vista para quitar un servicio del perfil del proveedor."""
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        provider = request.user.provider_profile
        service = get_object_or_404(Service, id=service_id)
        provider.services.remove(service)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


# Cerrar sesión
def v_cerrar_sesion(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('index')  # Redirige a la página principal después de cerrar sesión