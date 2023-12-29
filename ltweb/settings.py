from pathlib import Path
import os
from urllib.parse import quote

# Xây dựng đường dẫn trong dự án như sau: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cài đặt phát triển nhanh - không phù hợp cho môi trường sản xuất
# Xem https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# BẢO MẬT CẢNH BÁO: giữ cho khóa bí mật được sử dụng trong sản xuất là bí mật!
SECRET_KEY = 'django-insecure-1piwked@gqk-z_jh4x06+-fv)akxuk0q52ahsqn%et!)63glcz'

# BẢO MẬT CẢNH BÁO: đừng chạy với chế độ debug bật trong sản xuất!
DEBUG = True

ALLOWED_HOSTS = []

# Định nghĩa ứng dụng
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'polls.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'ltweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'polls', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ltweb.wsgi.application'

# Cơ sở dữ liệu
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Kiểm tra mật khẩu
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'polls.backends.CustomUserModelBackend',
]

# Quốc tế hóa
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Tệp tĩnh (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Loại trường khóa chính mặc định
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'polls.CustomUser'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Sessions được lưu trữ trong cơ sở dữ liệu
SESSION_SAVE_EVERY_REQUEST = True  # Lưu phiên mỗi lần yêu cầu
LOGIN_URL = 'login'  # Chuyển hướng người dùng chưa xác thực đến đây
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'  # Chuyển hướng người dùng đã xác thực đến đây

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Cấu hình VNPAY
VNPAY_RETURN_URL = 'http://localhost:8000/payment_return'  # Lấy từ cấu hình
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # Lấy từ cấu hình
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
VNPAY_TMN_CODE = '460XLNUO'  # ID trang web trong hệ thống VNPAY, lấy từ cấu hình
VNPAY_HASH_SECRET_KEY = 'NXWICYVCMPFEIFLXGXDFPBMXOMYEZAHM'  # Khóa bí mật để tạo checksum, lấy từ cấu hình
