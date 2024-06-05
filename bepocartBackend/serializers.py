from rest_framework import serializers
from bepocartBackend.models import *
from bepocartAdmin.models import *



class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = "__all__"



class CustomerLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta :
        model = Customer
        fields = ['email','password']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 



class SubcatecorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Subcategory
        fields = "__all__"


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ['id','name','description','short_description','salePrice','stock','category','image','created_at',]


class SubcatecoryBasedProductView(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = "__all__"


class WishlistSerializers(serializers.ModelSerializer):
    class Meta :
        model = Wishlist
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source ='product.name')
    salePrice = serializers.CharField(source ='product.salePrice')
    image = serializers.ImageField(source ='product.image')
    mainCategory = serializers.CharField(source ='product.category.pk')


    class Meta :
        model = Cart
        fields = ['id','customer','product','name','salePrice','image','mainCategory','quantity']



class CartModelSerializers(serializers.ModelSerializer):
    class Meta :
        model = Cart
        fields = "__all__"


class ProductViewSerializers(serializers.ModelSerializer):
    mainCategory = serializers.CharField(source ='category.category.pk')
    class Meta :
        model = Product
        fields = ['id','name','image','salePrice','mainCategory','category','short_description','description','offer_type','price']