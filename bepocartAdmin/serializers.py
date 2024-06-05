from rest_framework import serializers
from.models import *
from django.contrib.auth import get_user_model
User = get_user_model() 

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class AdminLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()    
    class Meta :
        model = User
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



class CarousalSerializers(serializers.ModelSerializer):
    class Meta :
        model = Carousal
        fields = "__all__"




class OfferBannerSerializers(serializers.ModelSerializer):
    class Meta :
        model = OfferBanner
        fields = "__all__"



class OfferProductSerializers(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = "__all__"


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    
    



