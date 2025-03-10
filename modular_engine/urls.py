from django.contrib import admin
from django.db import connection
from django.shortcuts import redirect

from django.urls import path, include


def get_dynamic_urls():
    dynamic_urls = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM module_manager_module WHERE is_installed = TRUE;")
            modules = [row[0] for row in cursor.fetchall()]
            for module in modules:
                try:
                    dynamic_urls.append(path(f'{module}/', include(f'{module}.urls')))
                except ModuleNotFoundError:
                    pass
    except Exception:
        pass
    return dynamic_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('module/modules/', permanent=True)),
    path('module/', include('module_manager.urls')),
] + get_dynamic_urls()
