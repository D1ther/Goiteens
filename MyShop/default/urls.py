from django.contrib import admin
from django.urls import path
from default import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tables/', views.tables, name='tables'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('statistics/', views.get_products_statistics, name='statistics'),
]