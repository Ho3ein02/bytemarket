from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import *


def order_create(request):
    """Create an order from user cart"""
    user = request.user
    # Check that the user is logged in, if not redirect user to login page
    if user.is_authenticated:
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            
            # Get province and city names from request
            province_id = request.POST.get('province')
            city_id = request.POST.get('city')
            if form.is_valid():
                order = form.save(commit=False)
                order.user = user
                order.province = Province.objects.get(id=province_id)
                order.city = City.objects.get(id=city_id)
                order.save()
                
                # Create order item from cart products
                for item in cart:
                    OrderItem.objects.create(order=order, 
                                             product=item['product'], 
                                             quantity=item['quantity'],
                                             price=item['price'], 
                                             weight=item['weight'])
                return redirect('order:confirm_order', order_id=order.id)
        else:
            form = OrderCreateForm()
        context = {
            'cart': cart,
            'user': user,
            'form': form,
            'provinces': Province.objects.all(),
        }
        return render(request, 'order/order_create.html', context)
    else:
        # Add the current url to the session to redirect to it after login
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
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        if form.is_valid():
            order = form.save(commit=False)
            order.province = Province.objects.get(id=province_id)
            order.city = City.objects.get(id=city_id)
            order.save()
            return redirect('order:confirm_order', order_id=order_id)
    else:
        form = OrderCreateForm(instance=order)
    context = {
        'form': form,
        'provinces': Province.objects.all()
    }
    return render(request, 'order/order_edit.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_detail.html', {'order': order})


def get_cities(request):
    """Return cities of a specified province"""
    province = request.GET.get('province')
    if province:
        cities = Province.objects.get(id=province).cities.all()
        return render(request, 'order/city_ajax.html', {'cities': cities})
