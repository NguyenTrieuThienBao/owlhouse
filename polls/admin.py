# Import các module và lớp từ Django
from django.contrib import admin
from .models import CustomUser, Category, Product, Cart, Order, OrderItem, WebsiteStats

# Đăng ký CustomUser với Admin và tùy chỉnh nếu cần
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Thêm cấu hình quản trị người dùng tùy chỉnh nếu cần
    pass

# Đăng ký Cart với Admin và tùy chỉnh nếu cần
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Thêm cấu hình quản trị giỏ hàng nếu cần
    pass

# Đăng ký Order với Admin và tùy chỉnh các hiển thị trong danh sách
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone_num', 'address', 'date_order', 'paid']

# Đăng ký OrderItem với Admin và tùy chỉnh các hiển thị trong danh sách
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'date_added']

# Đăng ký Category với Admin và tùy chỉnh các hiển thị và trường trước điền
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Đăng ký Product với Admin và tùy chỉnh các hiển thị, trường lọc và trường trước điền
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}

# Đăng ký WebsiteStats với Admin và tùy chỉnh các hiển thị và trường chỉ đọc
@admin.register(WebsiteStats)
class WebsiteStatsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'total_visits', 'total_registered_users', 'total_sales', 'total_sold_products')
    readonly_fields = ('timestamp', 'total_visits', 'total_registered_users', 'total_sales', 'total_sold_products')
