from rest_framework import serializers
from.models import *

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"

class AdminLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()    
    class Meta :
        model = Admin
        fields = ['email','password']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Subcategory
        fields =  "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ['name','description','short_description','salePrice','stock','category','image']



