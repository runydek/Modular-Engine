import subprocess
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect


from .models import Module
from .utils import check_latest_version

MODULES_AVAILABLE = ["products"]

def reload_server():
    os.utime("manage.py", None)

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'module_manager/module_list.html', {'modules': modules})

def install_module(request, module_name):
    module = get_object_or_404(Module, name=module_name)

    if not module.is_installed:
        module.is_installed = True
        module.save()
        messages.success(request, f"Module {module_name} berhasil diinstall!")
    else:
        messages.warning(request, "Module sudah terinstall.")

    reload_server() 
    return redirect('module_list')

def uninstall_module(request, module_name):
    module = Module.objects.filter(name=module_name).first()
    if module:
        module.is_installed = False
        module.save()
        messages.info(request, f"Module {module_name} berhasil di-uninstall!")
        reload_server()
    return redirect('module_list')


def upgrade_module(request, module_name):
    try:
        module = Module.objects.get(name=module_name)
        
        if module.has_update:
            subprocess.run(["python3", "manage.py", "makemigrations"], check=True)
            subprocess.run(["python3", "manage.py", "migrate"], check=True)

            module.version = module.latest_version
            module.save(update_fields=["version"])

            messages.success(request, f"Module {module.name} berhasil di-upgrade ke versi {module.version}")
        else:
            messages.info(request, f"Module {module.name} sudah versi terbaru")

    except Module.DoesNotExist:
        messages.error(request, "Module tidak ditemukan")

    return redirect("module_list") 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username dan password wajib diisi.')
            return render(request, 'registration/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('module_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
    
def update_latest_version(request, module_name):
    if request.method == "POST":
        module = get_object_or_404(Module, name=module_name)
        new_version = request.POST.get("latest_version").strip()

        if new_version:
            module.latest_version = new_version
            module.save(update_fields=["latest_version"])
            messages.success(request, f"Latest version {module.name} berhasil diperbarui ke {new_version}")
        else:
            messages.error(request, "Latest version tidak boleh kosong.")

    return redirect("module_list")