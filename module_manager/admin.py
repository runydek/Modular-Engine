from django.contrib import admin
from .models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'latest_version', 'is_installed')
    list_editable = ('latest_version',)

admin.site.register(Module, ModuleAdmin)