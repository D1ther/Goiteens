from django.shortcuts import render, redirect
from django.db.models import Max, Min, Count, Avg, Q
from django.core.paginator import Paginator
from .models import Basket, Product, User, BasketItem
from django.contrib import messages
from .forms import RegisterForm, AddProduct

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

def add_product(request):
    if request.method == 'POST':
        form = AddProduct(request.POST)
        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                stock=form.cleaned_data['stock'],
                rating=form.cleaned_data['rating']
            )
            messages.success(request, 'Продукт успішно додано!')
            return redirect('home')
    else:
        form = AddProduct()
    
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Продукт не знайдено!')
        return redirect('home')
    
    if request.method == 'POST':
        form = AddProduct(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.stock = form.cleaned_data['stock']
            product.rating = form.cleaned_data['rating']
            product.save()
            messages.success(request, 'Продукт успішно оновлено!')
            return redirect('home')
    else:
        form = AddProduct(initial={
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'rating': product.rating
        })
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Продукт успішно видалено!')
    except Product.DoesNotExist:
        messages.error(request, 'Продукт не знайдено!')
    
    return redirect('home')


def add_to_basket(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        
        # Отримуємо або створюємо кошик для сесії
        basket_id = request.session.get('basket_id')
        if basket_id:
            try:
                basket = Basket.objects.get(id=basket_id)
            except Basket.DoesNotExist:
                basket = Basket.objects.create()
                request.session['basket_id'] = basket.id
        else:
            basket = Basket.objects.create()
            request.session['basket_id'] = basket.id
        
        # Перевіряємо, чи товар вже в кошику
        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            basket_item.quantity += 1
            basket_item.save()
        
        messages.success(request, f'{product.name} додано до кошика!')
    except Product.DoesNotExist:
        messages.error(request, 'Товар не знайдено!')
    
    return redirect('home')

def view_basket(request):
    basket_id = request.session.get('basket_id')
    basket_items = []
    total_price = 0
    total_items = 0
    
    if basket_id:
        try:
            basket = Basket.objects.get(id=basket_id)
            basket_items = basket.basketitem_set.all()
            total_price = sum(item.get_total_price() for item in basket_items)
            total_items = sum(item.quantity for item in basket_items)
        except Basket.DoesNotExist:
            pass
    
    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'total_items': total_items,
    }
    
    return render(request, 'backet.html', context)

def remove_from_basket(request, item_id):
    try:
        basket_item = BasketItem.objects.get(id=item_id)
        product_name = basket_item.product.name
        basket_item.delete()
        messages.success(request, f'{product_name} видалено з кошика!')
    except BasketItem.DoesNotExist:
        messages.error(request, 'Товар не знайдено в кошику!')
    
    return redirect('view_basket')

def update_basket_item(request, item_id):
    try:
        basket_item = BasketItem.objects.get(id=item_id)
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                basket_item.quantity = quantity
                basket_item.save()
                messages.success(request, 'Кошик оновлено!')
            else:
                basket_item.delete()
                messages.success(request, 'Товар видалено з кошика!')
    except BasketItem.DoesNotExist:
        messages.error(request, 'Товар не знайдено!')
    
    return redirect('view_basket')