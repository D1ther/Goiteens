from django.shortcuts import render, redirect
from django.db.models import Max, Min, Count, Avg, Q
from django.core.paginator import Paginator
from .models import Basket, Product, User
from django.contrib import messages
from .forms import RegisterForm

def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list
    }
    return render(request, 'index.html', context)

def about(request):
    all_products = Product.objects.all()
    total_products = Product.objects.count()
    
    max_price = Product.objects.aggregate(Max('price'))['price__max'] or 0
    min_price = Product.objects.aggregate(Min('price'))['price__min'] or 0
    avg_price = Product.objects.aggregate(Avg('price'))['price__avg'] or 0
    
    cheap_products = Product.objects.filter(price__lt=10000)
    available_products = Product.objects.filter(stock__gt=5)
    pro_products = Product.objects.filter(name__icontains='pro')
    
    expensive_products = Product.objects.filter(price__gt=avg_price) if avg_price else []
    
    high_price_and_stock = Product.objects.filter(
        Q(price__gt=avg_price) & Q(stock__gt=10)
    ) if avg_price else []
    
    context = {
        'all_products': all_products,
        'total_products': total_products,
        'max_price': max_price if max_price else "N/A",
        'min_price': min_price if min_price else "N/A",
        'cheap_products': cheap_products,
        'available_products': available_products,
        'pro_products': pro_products,
        'expensive_products': expensive_products,
        'high_price_and_stock': high_price_and_stock,
        'avg_price': avg_price if avg_price else "N/A",
    }
    
    return render(request, 'about_me.html', context)

def tables(request):
    products = Product.objects.all()
    products_count = products.count()
    products_by_price = products.order_by('-price')
    top_expensive = products.order_by('-price')[:5]
    
    max_price = Product.objects.aggregate(Max('price'))['price__max'] or 0
    min_price = Product.objects.aggregate(Min('price'))['price__min'] or 0
    avg_price = Product.objects.aggregate(Avg('price'))['price__avg'] or 0
    
    context = {
        'products': products,
        'products_count': products_count,
        'products_by_price': products_by_price,
        'top_expensive': top_expensive,
        'max_price': max_price if max_price else "N/A",
        'min_price': min_price if min_price else "N/A",
        'avg_price': avg_price if avg_price else "N/A",
    }
    
    return render(request, 'tables.html', context)

def add_to_basket(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        basket = Basket.objects.create()
        basket.products.add(product)
        messages.success(request, f'{product.name} додано до кошика!')
    except Product.DoesNotExist:
        messages.error(request, 'Товар не знайдено!')
    
    return redirect('home')

def get_products_statistics(request):
    stats = {
        'total': Product.objects.count(),
        'max_price': Product.objects.aggregate(Max('price'))['price__max'] or 0,
        'min_price': Product.objects.aggregate(Min('price'))['price__min'] or 0,
        'avg_price': Product.objects.aggregate(Avg('price'))['price__avg'] or 0,
        'in_stock': Product.objects.filter(stock__gt=0).count(),
        'out_of_stock': Product.objects.filter(stock=0).count(),
    }
    
    return render(request, 'statistics.html', {'stats': stats})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Це ім\'я користувача вже зайнято!')
                return render(request, 'register.html', {'form': form})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Цей email вже зареєстрований!')
                return render(request, 'register.html', {'form': form})
            
            user = User.objects.create(username=username, email=email)
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})