from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from module_manager.models import Role

from module_manager.models import Module

def product_list(request):
    if not Module.objects.filter(name="products", is_installed=True).exists():
        return redirect('module_list')
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    role = Role.objects.get(user=request.user).role
    if role in ['manager', 'user']:
        if request.method == 'POST':
            name = request.POST['name']
            barcode = request.POST['barcode']
            price = request.POST['price']
            stock = request.POST['stock']
            Product.objects.create(name=name, barcode=barcode, price=price, stock=stock)
            return redirect('product_list')
        return render(request, 'products/product_form.html')
    return redirect('product_list')

@login_required
def product_update(request, product_id):
    role = Role.objects.get(user=request.user).role
    if role in ['manager', 'user']:
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            product.name = request.POST['name']
            product.barcode = request.POST['barcode']
            product.price = request.POST['price']
            product.stock = request.POST['stock']
            product.save()
            return redirect('product_list')
        return render(request, 'products/product_form.html', {'product': product})
    return redirect('product_list')

@login_required
def product_delete(request, product_id):
    role = Role.objects.get(user=request.user).role
    if role == 'manager':
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            product.delete()
            return redirect('product_list')
        return render(request, 'products/product_confirm_delete.html', {'product': product})
    return redirect('product_list')
