from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from django.contrib.auth import authenticate, login
from account.models import User
from account.password_generator import random_password_generator
from cart.cart import Cart
from .models import OrderItem, Order


def order_create(request):
    user = request.user
    if user.is_authenticated:
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = user
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                             price=item['price'], weight=item['weight'])
                return redirect('order:confirm_order', order_id=order.id)
        else:
            form = OrderCreateForm()
        context = {
            'cart': cart,
            'user': user,
            'form': form,
        }
        return render(request, 'order/order_create.html', context)
    else:
        request.session['next_url'] = '/order/order-create/'
        return redirect('account:verify_phone')


def confirm_order(request, order_id):
    cart = Cart(request)
    order = Order.objects.get(id=order_id)
    context = {
        'cart': cart,
        'order': order,
    }
    return render(request, 'order/confirm_order.html', context)


def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return redirect('order:confirm_order', order_id=order.id)
    else:
        form = OrderCreateForm(instance=order)
    return render(request, 'order/order_edit.html', {'form': form})
