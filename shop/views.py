from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Max, Sum
from django.contrib.postgres.search import TrigramSimilarity
from .models import *
from order.models import *
from .forms import *
from itertools import chain


def index(request):
    return render(request, 'shop/index.html')


def filter_products(request, products):
    """Returns the filtered and sorted products"""
    # Filter products
    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():
        available = filter_form.cleaned_data.get('available')
        max_price = filter_form.cleaned_data.get('max_price')
        min_price = filter_form.cleaned_data.get('min_price')
        brand = filter_form.cleaned_data.get('brand')
        category = filter_form.cleaned_data.get('category')
        if available:
            products = products.filter(inventory__gt=0)
        if min_price:
            products = products.filter(price__gt=min_price)
        if max_price:
            products = products.filter(price__lt=max_price)
        if brand:
            products = products.filter(brand__in=brand)
        if category:
            products = products.filter(category__in=category)
    
    # Sort products based on user selection
    
    ordering = request.GET.get('ordering')
    # In order for the unavailable part of the products to be at the end of the list and to sort the available part of the products, we must separate them
    available_inventory_products = products.filter(inventory__gt=0)  # Separate the available products section
    unavailable_inventory_products = products.filter(inventory=0)    # Separate the unavailable products section
    # Sort the available products section
    if ordering == 'newest':
        available_inventory_products = available_inventory_products.order_by('-created')
    elif ordering == 'price_asc':
        available_inventory_products = available_inventory_products.order_by('price')
    elif ordering == 'price_desc':
        available_inventory_products = available_inventory_products.order_by('-price')
    elif ordering == 'off_desc':
        available_inventory_products = available_inventory_products.order_by('-off_percent')
    
    products = list(chain(available_inventory_products, unavailable_inventory_products))  # Combination of available and unavailable parts
    
    return products


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    comments = Comment.objects.filter(product=product, active=True, parent=None)
    context = {
        'product': product,
        'comments': comments,
    }
    return render(request, 'shop/product_detail.html', context)


def products_list(request, category_slug=None):
    if category_slug:
        products = get_object_or_404(Category, slug=category_slug).products.all().order_by('-inventory')
    else:
        products = Product.objects.all()
    brands = Brand.objects.all()
    price_max = products.aggregate(Max('price', default=0))
    
    products = filter_products(request, products)
    
    # Product pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        products = paginator.page(1)
    
    # Send the response as json if the request is ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product_list_ajax.html', {'products': products})
    
    context = {
        'products': products,
        'brands': brands,
        'price_max': price_max['price__max'],
    }
    
    return render(request, 'shop/product_list.html', context)


def product_search(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    price_max = products.aggregate(Max('price', default=0))
    categories = Category.objects.all()

    query = ''
    
    # Find products that the user has searched for
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        if query:
            trigram1 = products.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.1)            # Search by name
            trigram2 = products.annotate(similarity=TrigramSimilarity('brand__name', query)).filter(similarity__gt=0.1)     # Search by brand
            trigram3 = products.annotate(similarity=TrigramSimilarity('category__name', query)).filter(similarity__gt=0.1)  # Search by category
            products = trigram1 | trigram2 | trigram3
    
    products = filter_products(request, products)
    
    # Product pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        products = paginator.page(1)

    # Send the response as json if the request is ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product_list_ajax.html', {'products': products})
    
    context = {
        'products': products,
        'brands': brands,
        'price_max': price_max['price__max'],
        'categories': categories,
        'query': query,
    }
    return render(request, 'shop/product_search.html', context)


@require_POST
def add_comment(request, product_id):
    user = request.user
    if user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment_text = cd['comment']
            parent_id = cd['parent']
            if parent_id == 'None':
                parent = None
            else:
                parent = get_object_or_404(Comment, id=parent_id)
            product = get_object_or_404(Product, id=product_id)
            Comment.objects.create(user=user, product=product, parent=parent, content=comment_text)
            data = {
                'success': True,
                'message': 'نظر شما با موفقیت ثبت شد.\nپس از بررسی توسط ادمین منتشر خواهد شد.',
            }
            return JsonResponse(data)
    else:
        data = {
            'success': False,
            'message': 'برای ثبت نظر لطفا ابتدا وارد شوید.'
        }
        return JsonResponse(data)


def products_portion(request, portion):
    if portion == 'suggestion':
        products = Product.objects.filter(off_percent__gt=0, inventory__gt=0).order_by('-off_percent')
    elif portion == 'best_seller':
        order_items = OrderItem.objects.filter(order__is_paid=True)
        products = Product.objects.filter(order_items__in=order_items).annotate(sell_count=Sum('order_items__quantity')).order_by('-sell_count')
    elif portion == 'newest':
        products = Product.objects.all().order_by('-created')
    brands = Brand.objects.all()
    price_max = products.aggregate(Max('price', default=0))
    
    products = filter_products(request, products)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        products = paginator.page(1)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product_list_ajax.html', {'products': products})
    
    context = {
        'products': products,
        'brands': brands,
        'price_max': price_max['price__max'],
    }
    return render(request, 'shop/product_list.html', context)
