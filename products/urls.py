from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<int:product_id>/', views.product_delete, name='product_delete'),
]