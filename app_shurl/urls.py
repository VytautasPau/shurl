from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main', views.MainURL.as_view(), name='main'),
    path('result', views.success, name='success'),
    path('account/', include('django.contrib.auth.urls')),
    path("registration", views.register, name="register"),
    path('<str:shorturl>', views.redirecting, name='redirect'),
]