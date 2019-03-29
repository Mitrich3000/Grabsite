from django.contrib import admin
from django.urls import path
from grabsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('result/', views.index, name='result'),
    path('', views.index, name='index'),
]
