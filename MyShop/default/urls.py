from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('tables/', views.tables),
    path('add_to_basket/<int:product_id>/', views.add_to_basket),
    path('stats/', views.get_products_statistics),
]
