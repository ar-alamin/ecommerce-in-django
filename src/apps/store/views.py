from django.shortcuts import render, get_object_or_404
from .models import Product
from apps.carts.models import CartItem
from apps.category.models import Category
from apps.carts.views import _cart_id

from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count() 

    context = {
        'products': paged_products,
        'product_count': product_count
    }
    return render(request, 'pages/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product= single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    
    return render(request, 'pages/product_detail.html', context)
    

def search(request):
    keyword = request.GET.get('keyword')

    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword),
            is_available=True
        ).order_by('-created_date')
        product_count = products.count() 

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'pages/store.html', context)