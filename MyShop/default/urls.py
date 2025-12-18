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
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('basket/', views.view_basket, name='view_basket'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('update-basket-item/<int:item_id>/', views.update_basket_item, name='update_basket_item'),
]