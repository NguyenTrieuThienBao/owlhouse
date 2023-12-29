# Imports
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db import transaction
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_page

from .forms import RegistrationForm, PaymentForm, LoginForm
from .models import Category, Product, CustomUser, Cart, Order, OrderItem, WebsiteStats
from .vnpay import vnpay

# View cho việc đăng ký người dùng
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                logout(request)
            return JsonResponse({'result': "Thành công"})
    else:
        form = RegistrationForm()
    return render(request, 'polls/register_index.html', {'form': form})

# View cho việc quên mật khẩu
def forgot_pass_view(request):
    return render(request, 'polls/forgot_pass_index.html')

# Cache trang chủ trong vòng 15 phút
@cache_page(60 * 15)
def homepage_view(request):
    # Lấy và tăng số lượng lượt truy cập tổng
    total_visits = increment_total_visits()

    # Lấy sản phẩm nổi bật
    feature_products = Product.objects.all()[:4]

    return render(request, 'polls/homepage_index.html', {'feature_products': feature_products, 'total_visits': total_visits})

# Hàm tăng số lượng lượt truy cập tổng
def increment_total_visits():
    new_stats = WebsiteStats.objects.create(total_visits=1)
    total_visits = new_stats.total_visits if new_stats else 0
    return total_visits

# View cho việc đăng nhập người dùng
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Xác thực thành công
            user = form.get_user()
            login(request, user)
            return homepage_view(request)
        else:
            messages.error(request, 'Tên người dùng hoặc mật khẩu không hợp lệ')
    else:
        form = LoginForm()

    return render(request, 'polls/login_index.html', {'form': form})

# View cho giỏ hàng của người dùng
@login_required
def cart_view(request):
    user = request.user
    list_item = []
    cart = Cart.objects.filter(user=user)
    for c in cart:
        list_item.append(c.product_id)

    item = Product.objects.filter(
        id__in=list_item
    )
    return render(request, 'polls/shopping_cart_index.html', {'items': item, 'cart': cart})

# View cho việc liệt kê tất cả sách
def listbooks_view(request):
    products = Product.objects.all()
    return render(request, 'polls/list_book_index.html', {'products': products})

# View cho việc đăng xuất
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

# View cho việc hiển thị chi tiết của một sản phẩm
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related_products = Product.objects.filter(category=product.category)[:4]
    return render(request, 'polls/onlybooks.html', {'product': product, 'related_products': related_products})

# View cho việc liệt kê sản phẩm trong một danh mục cụ thể
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'polls/list_book_index.html', {'category': category, 'products': products})

# View cho việc tìm kiếm sản phẩm
def search(request):
    search_product = request.GET.get('search')
    uppercase_product = str(search_product).upper()
    products = ''
    if search_product:
        products = Product.objects.filter(Q(title__icontains=uppercase_product) & Q(description__icontains=uppercase_product))
    else:
        products = ''
    if products:
        count = products.count()
    else:
        count = 0
    return render(request, 'polls/search_product.html', {'products': products, 'search_product': search_product, 'count': count})

# View cho việc thêm một sản phẩm vào giỏ hàng
@login_required
def add_cart(request, product_id, quantity):
    user = request.user
    cart = Cart.objects.filter(user=user, product_id=product_id)
    if request.POST.get('amount'):
        quantity = request.POST.get('amount')
        quantity = int(quantity)

    if cart.exists():
        existed_cart = Cart.objects.get(user=user, product_id=product_id)
        existed_cart.quantity += quantity
        existed_cart.save()
    else:
        new_cart = Cart.objects.create(user=user, product_id=product_id, quantity=1)
    return homepage_view(request)

# View cho việc cập nhật số lượng sản phẩm trong giỏ hàng
@login_required
def update_from_cart(request, product_id, quantity):
    user = request.user
    cart = Cart.objects.get(user=user, product_id=product_id)

    quantity = int(quantity)
    cart.quantity = quantity
    cart.save()
    return homepage_view(request)

# View cho việc xóa một sản phẩm khỏi giỏ hàng
@login_required
def remove_from_cart(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    if request.method == 'POST':
        cart.delete()
    return render(request, 'polls/shopping_cart_index.html')

# View cho tài khoản người dùng
@login_required
def account_view(request):
    user = request.user
    orders = Order.objects.filter(user=user, paid=True)
    items = OrderItem.objects.filter(order__in=orders)
    total_order = len(orders)
    return render(request, 'polls/account_index.html', {'total_order': total_order, 'orders': orders, 'items': items, 'user': user})

# Hàm để tạo OrderItem instances
def create_order_item(request, order_id):
    user = request.user