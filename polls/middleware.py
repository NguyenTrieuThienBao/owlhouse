from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Gọi hàm xử lý chính của middleware
        response = self.get_response(request)

        # Kiểm tra xem người dùng có đăng nhập và đang truy cập trang 'polls:cart' không
        if not request.user.is_authenticated and request.path == reverse('polls:cart'):
            # Nếu không đăng nhập, chuyển hướng người dùng đến trang đăng nhập
            return redirect('http://127.0.0.1:8000/login/')

        # Trả về phản hồi
        return response

