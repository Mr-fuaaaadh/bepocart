from django.urls import path
from  bepocartAdmin.views import *

urlpatterns = [
    path("register/",AdminRegister.as_view()),
    path("",AdminLogin.as_view()),


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






]