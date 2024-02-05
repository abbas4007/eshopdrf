from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.GetProducts.as_view(), name="products"),
    path('products/new/', views.NewProduct.as_view(), name="new_product"),
    path('products/upload_images/', views.upload_product_images, name="upload_product_images"),
    path('product/<str:id>/', views.GetProduct.as_view(), name="get_product_details"),
    path('products/<str:pk>/update/', views.update_product, name="update_product"),
    path('products/<str:pk>/delete/', views.delete_product, name="delete_product"),


    path('<str:pk>/reviews/', views.create_review, name = "create_update_review"),
    path('<str:pk>/reviews/delete/', views.delete_review, name = "delete_review"),
]