from django.urls import path
from bepocartBackend.views import *


urlpatterns = [
    path('register/',CustomerRegistration.as_view(), name="customer-register"),
    path('',CustomerLogin.as_view(), name="customer-login"),
    path('category/',CategoryView.as_view(), name="category"),
    path('category/<int:pk>/',SubcategoryView.as_view(), name="subcategory"),
    path('products/',CustomerProductView.as_view(), name="product"),
    path('subcategory/<int:pk>/',SubcategoryBasedProducts.as_view(), name="SubcategoryBasedProducts"),


    path('wishlist/',CustomerWishlist.as_view(), name="CustomerWishlist"),
    path('wishlist/<int:pk>/',CustomerAddProductInWishlist.as_view(), name="CustomerWishlist"),









    
]