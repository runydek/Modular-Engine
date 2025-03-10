from django.urls import path
from . import views

urlpatterns = [
    path('modules/', views.module_list, name='module_list'),
    path('module/install/<str:module_name>/', views.install_module, name='install_module'),
    path('module/uninstall/<str:module_name>/', views.uninstall_module, name='uninstall_module'),
    path("upgrade/<str:module_name>/", views.upgrade_module, name="upgrade_module"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]