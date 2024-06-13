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
    mainCategory = serializers.CharField(source ='category.category.pk')

    class Meta :
        model = Product
        fields = ['id','name','description','short_description','salePrice','stock','category','image','created_at','mainCategory']


class SubcatecoryBasedProductView(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='category.category.pk')
    class Meta :
        model = Product
        fields = ['id','name','short_description','description','price','salePrice','stock','category','image','discount','offer_banner','offer_type','mainCategory']


class WishlistSerializers(serializers.ModelSerializer):
    class Meta :
        model = Wishlist
        fields = "__all__"


class WishlistSerializersView(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='product.category.category.pk')
    class Meta :
        model = Wishlist
        fields = ['id','user','product','mainCategory']


class CartSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source ='product.name')
    salePrice = serializers.CharField(source ='product.salePrice')
    price = serializers.IntegerField(source ='product.price')
    image = serializers.ImageField(source ='product.image')
    mainCategory = serializers.CharField(source ='product.category.category.pk')


    class Meta :
        model = Cart
        fields = ['id','customer','product','name','salePrice','image','mainCategory','quantity','price']



class CartModelSerializers(serializers.ModelSerializer):
    class Meta :
        model = Cart
        fields = "__all__"


class ProductViewSerializers(serializers.ModelSerializer):
    mainCategory = serializers.CharField(source ='category.category.pk')
    class Meta :
        model = Product
        fields = ['id','name','image','salePrice','mainCategory','category','short_description','description','offer_type','price']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address', 'email', 'phone', 'pincode', 'city', 'state', 'note']

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data



class UserProfileSErilizers(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ['username', 'email', 'phone']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'updated_at', 'status', 'total_amount', 'address', 'items']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducyImage
        fields = "__all__"


class ProductSerializerWithMultipleImage(serializers.ModelSerializer):
    size_names = serializers.SerializerMethodField()

    class Meta:
        model = ProducyImage
        fields = ['id', 'product', 'color', 'image1', 'image2', 'image3', 'image4', 'image5','size', 'size_names']

    def get_size_names(self, obj):
        return [size.name for size in obj.size.all()]



class CustomerOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class CustomerOrderItems(serializers.ModelSerializer):
    productName = serializers.CharField(source ='product.name')
    productImage = serializers.ImageField(source ='product.image')
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price','productImage','productName','order']



class RecentlyViewedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyViewedProduct
        fields = ['user', 'product', 'viewed_at']

class RecomendedProductSerializer(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='category.category.pk')
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'salePrice', 'image','mainCategory'] 