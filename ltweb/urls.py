from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Định nghĩa các URL cho ứng dụng

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('polls.urls')),
]

# Nếu ở chế độ DEBUG, thêm cấu hình cho tệp tĩnh
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Nếu ở chế độ DEBUG, thêm cấu hình cho tệp đa phương tiện
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
