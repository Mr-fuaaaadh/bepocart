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
        fields = ['name','description','short_description','salePrice','stock','category','image']


class SubcatecoryBasedProductView(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = "__all__"