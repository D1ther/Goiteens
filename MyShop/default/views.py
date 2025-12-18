from django.shortcuts import render
from django.db.models import Max, Min, Count, Avg, Q
from .models import Basket, Product

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)

def about(request):
    all_products = Product.objects.all()

    total_products = Product.objects.count()

    max_price = Product.objects.aggregate(Max('price'))['price__max']

    min_price = Product.objects.aggregate(Min('price'))['price__min']

    cheap_products = Product.objects.filter(price__lt=10000)

    available_products = Product.objects.filter(stock__gt=5)

    pro_products = Product.objects.filter(name__icontains='pro')

    avg_price = Product.objects.aggregate(Avg('price'))['price__avg']
    expensive_products = Product.objects.filter(price__gt=avg_price)
    
    high_price_and_stock = Product.objects.filter(
        Q(price__gt=avg_price) & Q(stock__gt=10)
    )
    
    context = {
        'all_products': all_products,
        'total_products': total_products,
        'max_price': max_price,
        'min_price': min_price,
        'cheap_products': cheap_products,
        'available_products': available_products,
        'pro_products': pro_products,
        'expensive_products': expensive_products,
        'high_price_and_stock': high_price_and_stock,
        'avg_price': avg_price,
    }
    
    return render(request, 'about_me.html', context)

def tables(request):
    products = Product.objects.all()

    products_count = products.count()

    products_by_price = products.order_by('-price')

    top_expensive = products.order_by('-price')[:5]
    
    context = {
        'products': products,
        'products_count': products_count,
        'products_by_price': products_by_price,
        'top_expensive': top_expensive,
    }
    
    return render(request, 'tables.html', context)

def add_to_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.create()
    basket.products.add(product)
    
    return render(request, 'index.html')

def get_products_statistics(request):
    stats = {
        'total': Product.objects.count(),
        'max_price': Product.objects.aggregate(Max('price'))['price__max'],
        'min_price': Product.objects.aggregate(Min('price'))['price__min'],
        'avg_price': Product.objects.aggregate(Avg('price'))['price__avg'],
        'in_stock': Product.objects.filter(stock__gt=0).count(),
        'out_of_stock': Product.objects.filter(stock=0).count(),
    }
    
    return render(request, 'statistics.html', {'stats': stats})