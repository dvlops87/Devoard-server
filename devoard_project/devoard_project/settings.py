"""
Django settings for devoard_project project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
import json
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'secrets.json')

#secret.json 읽기
secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'devoard_app.apps.DevoardAppConfig',
    'rest_framework',
    'knox',
    'corsheaders',
    'rest_framework_jwt',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

ROOT_URLCONF = 'devoard_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'devoard-client', 'build')
        ],
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

WSGI_APPLICATION = 'devoard_project.wsgi.application'

AUTH_USER_MODEL = 'user.user_info'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'devoard-client', 'build', 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # 인증된 유저만 헤더에 access token 을 포함하여 유효한 유저만이 접근이 가능해지는 것을 디폴트로. permission_classes 변수 설정할 필요가 없음.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 인증된 회원만 엑세스 허용
        'rest_framework.permissions.AllowAny',         # 모든 회원 액세스 허용
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', #api 실행시 인증할 클래스 정의
    ),
}

#JWT 환경 설정
REST_USE_JWT = True

from datetime import timedelta

# 추가 설정 부분

SIMPLE_JWT = {
   
   # 여기는 기본 세팅값
   
   'JWT_SECRET_KEY': secrets,   # JWT 에 서명하는데 사용되는 시크릿키. 장고의 시크릿키가 디폴트.
   'JWT_ALGORITHM': 'HS256',       # PyJWT 에서 암호화 서명에 지원되는 알고리즘으로 마찬가지로 이것 또한 기본값.
   'JWT_VERIFY_EXPIRATION' : True, # 토큰 만료 시간 확인. 기본값 True.
    
   # 새로 커스텀한 옵션들
   
   'JWT_ALLOW_REFRESH': True,      # 토큰 새로고침 기능 활성화. 기본값 False.
   'JWT_EXPIRATION_DELTA': timedelta(minutes=30),     # datetime.timedelta 의 만료 시간. 기본값 seconds=300. 
   'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=3), # Refresh Token의 새로 고침 시간. 기본값 days=7
   'JWT_RESPONSE_PAYLOAD_HANDLER': 'accounts.custom_responses.my_jwt_response_handler'  #로그인 또는 새로 고침 후 반환되는 응답 데이터를 제어. 기본값은 {'token' : token } 인데 이건 나중에 우리가 따로 적어줄것임.
}
