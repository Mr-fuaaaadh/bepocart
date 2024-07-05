from rest_framework import serializers
from.models import *
from bepocartBackend.models import *
from django.contrib.auth.models import User

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'id', 'email', 'is_active', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove the password confirmation field
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.is_active = validated_data.get('is_active', True)
        user.is_superuser = validated_data.get('is_superuser', False)
        user.save()
        return user


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



class SubCategoryUpdateSerializers(serializers.ModelSerializer):
    class Meta :
        model = Subcategory
        fields = "__all__"

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



class CustomerAllProductSerializers(serializers.ModelSerializer):
    categoryName = serializers.CharField(source="category.name")
    class Meta :
        model = Product
        fields = ['id','name','short_description','description','price','salePrice','stock','category','image','discount','offer_banner','offer_type','categoryName']


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
    # name = serializers.CharField(source='coupon.code')
    class Meta :
        model = Order
        fields = ['id','customer','total_amount','created_at','updated_at','status','address','customerImage','customerName','coupon']



class AdminOrderViewsSerializers(serializers.ModelSerializer):
    customerImage = serializers.ImageField(source='customer.image')
    customerName = serializers.CharField(source='customer.first_name')
    couponName = serializers.SerializerMethodField()  # Use SerializerMethodField for custom logic
    couponType = serializers.SerializerMethodField()  # Adding couponType to handle coupon_type attribute

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'total_amount', 'created_at','coupon' ,
            'updated_at', 'status', 'address', 'customerImage', 
            'customerName', 'couponName', 'couponType', 'payment_method', 'payment_id'
        ]

    def get_couponName(self, obj):
        return obj.coupon.code if obj.coupon else None  # Return the coupon code or None

    def get_couponType(self, obj):
        return obj.coupon.coupon_type if obj.coupon else None 

class AdminOrderItemSerializers(serializers.ModelSerializer):
    class Meta :
        model = OrderItem
        fields = "__all__"



class ProductSizeSerializers(serializers.ModelSerializer):
    class Meta :
        model = Size
        fields = "__all__"



class AdminCoupenSerializers(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta :
        model = Coupon
        fields = "__all__"



class AdminallCoupenSerializers(serializers.ModelSerializer):
    category  = serializers.CharField(source ='discount_category.name')
    class Meta :
        model = Coupon
        fields = ['id','code','coupon_type','discount','start_date','end_date','status','max_uses','used_count','discount_product','discount_category','category']



class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class AdminCustomerViewSerilizers(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields ="__all__"
