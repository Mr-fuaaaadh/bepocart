from rest_framework import serializers
from.models import *
from bepocartBackend.models import *

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

class SubcategoryModelSerializer(serializers.ModelSerializer):
    class Meta :
        model = Subcategory
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    categoryName = serializers.CharField(source ='category.name')
    class Meta :
        model = Subcategory
        fields =  ['id','name','image','category','categoryName']

class ProductSerializer(serializers.ModelSerializer):

    class Meta :
        model = Product
        fields = ['id','name','description','short_description','salePrice','stock','category','image',]


class ProductSerializerView(serializers.ModelSerializer):
    categoryName = serializers.CharField(source ='category.name')
    mainCategory = serializers.CharField(source ='category.category.pk')

    class Meta :
        model = Product
        fields = ['id','name','description','short_description','salePrice','stock','category','image','categoryName','mainCategory','price']


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

    
    
class AdminOrderSerializers(serializers.ModelSerializer):
    class Meta :
        model = Order
        fields = "__all__"


class AdminOrderViewsSerializers(serializers.ModelSerializer):
    customerImage = serializers.ImageField(source ='customer.image')
    customerName  = serializers.CharField(source ='customer.username')
    class Meta :
        model = Order
        fields = ['id','customer','total_amount','created_at','updated_at','status','address','customerImage','customerName']


class AdminOrderItemSerializers(serializers.ModelSerializer):
    class Meta :
        model = OrderItem
        fields = "__all__"



class ProductSizeSerializers(serializers.ModelSerializer):
    class Meta :
        model = Size
        fields = "__all__"



class AdminCoupenSerializers(serializers.ModelSerializer):
    class Meta :
        model = Coupon
        fields = "__all__"



class AdminallCoupenSerializers(serializers.ModelSerializer):
    category  = serializers.CharField(source ='discount_category.name')
    class Meta :
        model = Coupon
        fields = ['id','code','coupon_type','discount','start_date','end_date','status','max_uses','used_count','discount_product','discount_category','category']