from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from django.contrib.sessions.models import Session
from polls.models import WebsiteStats, CustomUser, Product, OrderItem

class Command(BaseCommand):
    # Mô tả của lệnh
    help = 'Update website statistics'

    def handle(self, *args, **options):
        # Gọi hàm để tính toán và cập nhật thống kê trang web
        self.update_stats()

    def update_stats(self):
        # Lấy dữ liệu từ các mô hình khác nhau
        total_visits = self.calculate_total_visits()
        total_registered_users = CustomUser.objects.count()
        total_sales = self.calculate_total_sales()
        total_sold_products = self.calculate_total_sold_products()

        # Tạo hoặc cập nhật một instance của WebsiteStats
        stats, created = WebsiteStats.objects.get_or_create(
            timestamp=timezone.now(),
            defaults={
                'total_visits': total_visits,
                'total_registered_users': total_registered_users,
                'total_sales': total_sales,
                'total_sold_products': total_sold_products,
            }
        )

        if not created:
            # Cập nhật instance hiện tại
            stats.total_visits = total_visits
            stats.total_registered_users = total_registered_users
            stats.total_sales = total_sales
            stats.total_sold_products = total_sold_products
            stats.save()

        self.stdout.write(self.style.SUCCESS('Website statistics updated successfully.'))

    def calculate_total_visits(self):
        # Tính tổng số lượt truy cập từ các phiên hoạt động
        total_visits = Session.objects.filter(expire_date__gte=timezone.now()).count()
        return total_visits

    def calculate_total_sales(self):
        # Thực hiện hàm này để tính tổng doanh số bán hàng từ tất cả các đơn hàng
        # Ví dụ: Sử dụng mô hình OrderItem để lấy thông tin về doanh số bán hàng
        total_sales = OrderItem.objects.aggregate(sum_sales=models.Sum('price'))['sum_sales']
        return Decimal(total_sales) if total_sales else Decimal(0.0)

    def calculate_total_sold_products(self):
        # Thực hiện hàm này để tính tổng số sản phẩm đã bán
        total_sold_products = OrderItem.objects.count()
        return total_sold_products
