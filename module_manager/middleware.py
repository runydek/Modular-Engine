from django.conf import settings
from django.db import connection

class LoadModulesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.load_modules()

    def load_modules(self):
        if 'module_manager_module' not in connection.introspection.table_names():
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM module_manager_module WHERE is_installed = TRUE;")
                modules = [row[0] for row in cursor.fetchall()]

            for module in modules:
                if module not in settings.INSTALLED_APPS:
                    settings.INSTALLED_APPS.append(module)

        except Exception as e:
            print(f"⚠ Error loading modules: {e}")

    def __call__(self, request):
        return self.get_response(request)
