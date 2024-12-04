from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import json


def index(request):
    print(request.session.get('cart'))
    return render(request, 'shop/index.html')


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    context = {
        'product': product,
    }
    print(request.session.get('cart'))
    return render(request, 'shop/product_detail.html', context)


def insert(reqeust):
    with open('data.json') as file:
        data = json.load(file)

    category = Category.objects.get_or_create(name='لپ تاپ')[0]

    for d in data:
        brand = Brand.objects.get_or_create(name=d['brand'])[0]
        product = Product.objects.create(name=d['name'],
                                         description=d['description'],
                                         price=d['price'],
                                         off_percent=d['off'],
                                         new_price=0,
                                         inventory=d['inventory'],
                                         brand=brand,
                                         category=category)
        for feature in d['features']:
            ProductFeature.objects.create(product=product,
                                          name=feature['name'],
                                          value=feature['value'])

        ProductImage.objects.create(product=product,
                                    image_file=f'product_images/2024-11-11/{d["id"]}_{d["name"]}.jpg',
                                    title='laptop')

    return redirect('shop:index')


