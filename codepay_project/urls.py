"""codepay_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import viewsets



urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'/', include('core.urls', namespace='core')),
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'api/rpa', viewsets.payment_get, name='payment-get'),
    path(r'api/rpa/<str:status>', viewsets.payment_get, name='payment-filter'),
    path(r'api/rpa/resquest/<str:hashid>', viewsets.payment_request, name='payment-request'),
    path(r'api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
