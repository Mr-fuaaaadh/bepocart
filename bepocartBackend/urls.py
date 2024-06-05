from django.urls import path
from bepocartBackend.views import *


urlpatterns = [
    path('register/',CustomerRegistration.as_view(), name="customer-register"),
    path('',CustomerLogin.as_view(), name="customer-login"),
    path('category/',CategoryView.as_view(), name="category"),
    path('category/<int:pk>/',SubcategoryView.as_view(), name="subcategory"),
    path('products/',CustomerProductView.as_view(), name="product"),
    path('subcategory/<int:pk>/',SubcategoryBasedProducts.as_view(), name="SubcategoryBasedProducts"),
    path('banners/',CustomerCarousalView.as_view(), name="CustomerCarousalView"),
    path('offer-banner/',CustomerOfferBannerView.as_view(), name="CustomerOfferBannerView"),




    path('wishlist/',CustomerWishlist.as_view(), name="CustomerWishlist"),
    path('add-wishlist/<int:pk>/',CustomerAddProductInWishlist.as_view(), name="Customer-add-Wishlist"),
    path('wishlist-delete/<int:pk>/',CustomerProductDeleteInWishlist.as_view(), name="CustomerProductDeleteInWishlist"),



    path('cart/<int:pk>/',CustomerProductInCart.as_view(), name="CustomerProductInCart"),
    path('cart-products/',CustomerCartProducts.as_view(), name="CustomerCartProducts"),
    path('cart-delete/<int:pk>/',CartProductDelete.as_view(), name="CartProductDelete"),
    path('cart/increment/<int:pk>/', IncrementProductQuantity.as_view(), name='increment-quantity'),
    path('cart/decrement/<int:pk>/', DecrementProductQuantity.as_view(), name='decrement-quantity'),


    path('offer-banner/<int:pk>/products/', OfferBanerBasedProducts.as_view(), name='offer-banner-products'),
    path('product/<int:pk>/',ProductBigView.as_view(), name="ProductBigView"),
    path('category/<int:pk>/products/',MianCategoryBasedProducts.as_view(), name="MianCategoryBasedProducts"),














    
]