from django.urls import path
from  bepocartAdmin.views import *

urlpatterns = [
    path("register/",AdminRegister.as_view()),
    path("",AdminLogin.as_view()),

    path('Bepocart-Banner/',CarousalAdd.as_view()),
    path('Bepocart-Banners/',CarousalView.as_view()),
    path('Bepocart-Banner-delete/<int:pk>/',CarousalDelete.as_view()),
    path('Bepocart-Banner-update/<int:pk>/',CarousalUpdate.as_view()),


    path('Bepocart-Offer-Banner/',OfferBannerAdd.as_view()),
    path('Bepocart-Offer-Banners/',OfferBannerView.as_view()),
    path('Bepocart-Offer-Banner-Delete/<int:pk>/',OfferBannerDelete.as_view()),
    path('Bepocart-Offer-Banner-Update/<int:pk>/',OfferBannerUpdate.as_view()),



    path('Bepocart-category/',CategoryAdd.as_view()),
    path('Bepocart-categories/',Categories.as_view()),
    path('Bepocart-category-delete/<int:pk>/',CategoryDelete.as_view()),
    path('Bepocart-category-update/<int:pk>/',CategoryUpdate.as_view()),


    path('Bepocart-subcategory/',SubcategoryAdd.as_view()),
    path('Bepocart-subcategories/',SubcategoryView.as_view()),
    path('Bepocart-subcategory-update/<int:pk>/',SubcategoryUpdate.as_view()),
    path('Bepocart-subcategory-delete/<int:pk>/',SubcategoryDelete.as_view()),


    path('Bepocart-product/',ProductAdd.as_view()),
    path('Bepocart-products/',ProductView.as_view()),
    path('Bepocart-product-update/<int:pk>/',ProductUpdate.as_view()),
    path('Bepocart-product-delete/<int:pk>/',ProductDelete.as_view()),

    path('Bepocart-Offer-Product/',OfferProductAdd.as_view()),
    path('Bepocart-Offer-Products/',OfferProductView.as_view()),
    path('Bepocart-Offer-Product-Delete/<int:pk>/',OfferProductDelete.as_view()),
    path('Bepocart-Offer-Product-Update/<int:pk>/',OfferProductUpdate.as_view()),


    path('Bepocart-Product-image-add/<int:pk>/',ProductImageCreateView.as_view()),
    path('Bepocart-Product-images/<int:pk>/',ProductBasdMultipleImageView.as_view()),
    path('Bepocart-Product-images-delete/<int:pk>/',ProductMultipleImageDelete.as_view()),


    path('Bepocart-Orders/',AllOrders.as_view()),
    path('Bepocart-Order-Item/<int:customer>/',AllOrderItems.as_view()),


    path('Bepocart-product-size/',ProductSizeAdd.as_view()),
    path('Bepocart-product-size-view/',ProductSizeView.as_view()),

    path('Bepocart-promotion-coupen/',AdminCouponCreation.as_view()),
    path('Bepocart-promotion-coupen-views/',AdminCoupensView.as_view()),







    








]