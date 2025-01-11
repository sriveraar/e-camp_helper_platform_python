from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Provider, Service, ProviderProfile, Message
from .forms import ProviderForm, ProviderProfileForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

# Vista para iniciar sesión
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


# Página principal que lista todos los proveedores
def v_index(request):
    all_providers = Provider.objects.all()
    return render(request, 'providers/index.html', {'providers': all_providers})


# Registro de nuevos proveedores
def v_crear_cuenta(request):
    if request.method == 'POST':
        provider_form = ProviderForm(request.POST, request.FILES)
        profile_form = ProviderProfileForm(request.POST)

        if provider_form.is_valid() and profile_form.is_valid():
            email = provider_form.cleaned_data['email']
            password = provider_form.cleaned_data['password']

            # Verificar si el usuario ya existe
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Ya existe un usuario con este correo.')
                return redirect('create_account')

            # Crear usuario
            user = User.objects.create_user(username=email, password=password)

            # Guardar el proveedor
            provider = provider_form.save(commit=False)
            provider.user = user
            provider.save()

            # Guardar el perfil
            provider_profile = profile_form.save(commit=False)
            provider_profile.provider = provider
            provider_profile.user = user
            provider_profile.save()

            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')

        else:
            messages.error(request, 'Hubo errores en los formularios. Intenta nuevamente.')
            return render(request, 'providers/create_account.html', {
                'provider_form': provider_form,
                'profile_form': profile_form,
            })
    else:
        provider_form = ProviderForm()
        profile_form = ProviderProfileForm()

    return render(request, 'providers/create_account.html', {
        'provider_form': provider_form,
        'profile_form': profile_form,
    })


# Vista para crear el perfil de proveedor
@login_required
def v_crear_perfil_proveedor(request):
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
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        messages.warning(request, 'No tienes un perfil de proveedor. Por favor, crea uno.')
        return redirect('create_provider_profile')

    if request.method == 'POST':
        provider.nombres = request.POST.get('nombres', provider.nombres)
        provider.apellidos = request.POST.get('apellidos', provider.apellidos)
        provider.descripcion = request.POST.get('descripcion', provider.descripcion)
        provider.telefono = request.POST.get('telefono', provider.telefono)
        provider.atencion = request.POST.get('atencion', provider.atencion)
        
        # Actualizar la foto si se subió una nueva
        if 'foto' in request.FILES:
            provider.foto = request.FILES['foto']
        
        provider.save()
        messages.success(request, "Tu información ha sido actualizada correctamente.")
        return redirect('account')

    return render(request, 'providers/account.html', {'provider': provider})



# Detalle del proveedor
def v_detalle_proveedor(request, email):
    provider = get_object_or_404(Provider, email=email)
    return render(request, 'providers/provider_detail.html', {'provider': provider})


# Agregar servicio al perfil del proveedor
@login_required
def v_cuenta_incluir_servicio(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        provider = request.user.provider_profile
        service = get_object_or_404(Service, id=service_id)
        
        if service not in provider.services.all():
            provider.services.add(service)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'El servicio ya está asociado al proveedor.'})

    return JsonResponse({'status': 'error'})


# Quitar servicio del perfil del proveedor
@login_required
def v_cuenta_remover_servicio(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        provider = request.user.provider_profile
        service = get_object_or_404(Service, id=service_id)

        if service in provider.services.all():
            provider.services.remove(service)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Este servicio no está asociado al proveedor.'})

    return JsonResponse({'status': 'error'})


@login_required
def editar_datos(request):
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        provider = None

    messages_received = Message.objects.filter(provider=provider) if provider else []

    if request.method == 'POST':
        provider.nombres = request.POST.get('nombres', provider.nombres)
        provider.telefono = request.POST.get('telefono', provider.telefono)
        provider.apellidos = request.POST.get('apellidos', provider.apellidos)
        provider.descripcion = request.POST.get('descripcion', provider.descripcion)
        provider.atencion = request.POST.get('atencion', provider.atencion)

        # Verificar si se ha subido una nueva foto
        if request.FILES.get('foto'):
            provider.foto = request.FILES['foto']

        # Actualizar la contraseña si se ha proporcionado una nueva
        password = request.POST.get('password')
        if password:
            provider.user.set_password(password)
            provider.user.save()
            update_session_auth_hash(request, provider.user)  # Mantener al usuario logueado después de cambiar la contraseña
        
        provider.save()
        
        messages.success(request, "Tus datos han sido actualizados exitosamente.")
        return redirect('editar_datos')
    
    return render(request, 'editar_datos.html', {
        'provider': provider,
        'messages': messages_received
    })

# Obtener todos los proveedores registrados
def index(request):
    all_providers = Provider.objects.all()
    return render(request, 'providers/providers_list.html', {'all_providers': all_providers})

def ver_proveedor(request, id):
    # Obtener el proveedor por su id
    provider = get_object_or_404(Provider, id=id)

    return render(request, 'ver_proveedor.html', {'provider': provider})

# Cerrar sesión
def v_cerrar_sesion(request):
    logout(request)
    return redirect('index')
