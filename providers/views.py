from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Provider, Service, ProviderProfile
from .forms import ProviderForm, ProviderProfileForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


from django.contrib.auth.models import User

def v_iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Email o contraseña incorrectos')
            return redirect('login')

    return render(request, 'providers/login.html')


# Página principal
def v_index(request):
    """Página principal que lista todos los proveedores."""
    all_providers = Provider.objects.all()
    return render(request, 'providers/index.html', {'providers': all_providers})

# Registro de nuevos proveedores
def v_crear_cuenta(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            # Solo crear el perfil de proveedor sin usuario
            provider = form.save()
            return redirect('login')  # Redirige al login después de la creación del proveedor
    else:
        form = ProviderForm()

    return render(request, 'providers/create_account.html', {'form': form})

# Vista para crear el perfil de proveedor
@login_required
def v_crear_perfil_proveedor(request):
    """Vista para que un usuario cree su perfil de proveedor."""
    if hasattr(request.user, 'provider_profile'):
        # El usuario ya tiene un perfil de proveedor
        return redirect('account')

    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user = request.user
            provider.save()
            return redirect('account')  # Redirige a la página de cuenta del proveedor
    else:
        form = ProviderForm()

    return render(request, 'providers/create_provider_profile.html', {'form': form})

# Gestión del perfil del proveedor
@login_required
def v_mi_cuenta(request):
    # Obtén el perfil del proveedor (si no existe, redirige)
    try:
        provider_profile = request.user.provider_profile
    except ProviderProfile.DoesNotExist:
        provider_profile = None

    # Si el proveedor no tiene perfil, puedes redirigir a un formulario de creación de perfil
    if provider_profile is None:
        return redirect('create_provider_profile')

    # Si el proveedor tiene perfil, manejar la edición de servicios
    if request.method == 'POST':
        form = ProviderProfileForm(request.POST, instance=provider_profile)
        if form.is_valid():
            form.save()
            return redirect('mi_cuenta')  # Redirigir después de guardar los cambios
    else:
        form = ProviderProfileForm(instance=provider_profile)

    # Obtener los servicios disponibles
    available_services = Service.objects.all()

    return render(request, 'account.html', {
        'form': form,
        'provider': provider_profile,
        'available_services': available_services,
    })

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
