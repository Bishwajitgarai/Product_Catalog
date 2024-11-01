from django.urls import path
from . import views

urlpatterns = [
    # Category URLs
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:pk>/', views.retrieve_category, name='retrieve_category'),
    path('category/<int:pk>/update/', views.update_category, name='update_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    
    # Product URLs
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.retrieve_product, name='retrieve_product'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/search/', views.search_products, name='search_products'),
    path('product/list/', views.list_products, name='list_products'),

    path('sales/create/', views.create_sale, name='create-sale'),
    path('sales/list/', views.list_sales, name='list-sales'),

]
