from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from polls.models import CustomUser

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Lấy người dùng từ cơ sở dữ liệu dựa trên tên đăng nhập
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            # Trả về None nếu không tìm thấy người dùng
            return None

        # Kiểm tra mật khẩu sử dụng hàm check_password của Django
        if check_password(password, user.password) and self.user_can_authenticate(user):
            # Trả về người dùng nếu mật khẩu hợp lệ và người dùng có thể xác thực
            return user
