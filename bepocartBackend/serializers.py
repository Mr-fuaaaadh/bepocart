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
        fields = ['id','slug','name','description','short_description','price','salePrice','category','image','created_at','mainCategory','discount','type']


class SubcatecoryBasedProductView(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='category.category.pk')
    class Meta :
        model = Product
        fields = ['id','name','short_description','description','price','salePrice','category','image','discount','mainCategory','slug']


class WishlistSerializers(serializers.ModelSerializer):
    class Meta :
        model = Wishlist
        fields = "__all__"


class WishlistSerializersView(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='product.category.category.pk')
    category = serializers.CharField(source = "product.category.name")
    productName = serializers.CharField(source='product.name')
    productImage = serializers.ImageField(source='product.image')
    productPrice = serializers.IntegerField(source ="product.salePrice")
    slug = serializers.CharField(source ="product.slug")



    class Meta :
        model = Wishlist
        fields = ['id','user','product','mainCategory','productName','productImage','productPrice','category','slug']


from django.db.models import Q

class CartSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    category = serializers.IntegerField(source='product.category.pk')
    slug = serializers.CharField(source='product.slug')
    salePrice = serializers.CharField(source='product.salePrice')
    price = serializers.IntegerField(source='product.price')
    subcategory_slug = serializers.CharField(source='product.category.slug')
    image = serializers.ImageField(source='product.image')
    mainCategory = serializers.CharField(source='product.category.category.pk')
    stock = serializers.SerializerMethodField()
    has_offer = serializers.SerializerMethodField()
    discount_product = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'customer', 'product', 'name', 'salePrice', 'image', 'category', 
            'mainCategory', 'quantity', 'slug', 'price', 'color', 'size', 'stock', 
            'has_offer', 'discount_product', 'subcategory_slug'
        ]

    def get_stock(self, obj):
        product_type = obj.product.type
        try:
            if product_type == "single":
                try:
                    variant = ProductColorStock.objects.get(product=obj.product, color=obj.color)
                    return variant.stock
                except ProductColorStock.DoesNotExist as e:
                    return 0
            else:
                try:
                    check_color = ProductVariant.objects.filter(product=obj.product, color=obj.color).first()
                    if check_color:
                        try:
                            variant = ProductVarientSizeStock.objects.get(product_variant=check_color, size=obj.size)
                            return variant.stock
                        except ProductVarientSizeStock.DoesNotExist as e:
                            return 0
                    else:
                        return 0
                except ProductVariant.DoesNotExist as e:
                    return 0
        except Exception as e:
            return 0


    def get_has_offer(self, obj):
        product = obj.product
        category = product.category

        has_offer = OfferSchedule.objects.filter(
            Q(offer_active=True) & (Q(offer_products=product) | Q(offer_category=category))
        ).exists()

        if has_offer:
            return "Offer Applied"
        
        excluded_offer = OfferSchedule.objects.filter(
            Q(offer_active=True) & (Q(exclude_products=product) | Q(excluded_offer_category=category))
        ).exists()
        
        if excluded_offer:
            return "normal"
        
        return "normal"
    
    def get_discount_product(self, obj):
        product = obj.product
        category = product.category

        discount_not_allowed = OfferSchedule.objects.filter(
            Q(offer_active=True) & (Q(discount_not_allowed_products=product) | Q(discount_not_allowed_category=category))
        ).exists()
        
        if discount_not_allowed:
            return "Discount Not Allowed"
        
        discount_allowed = OfferSchedule.objects.filter(
            Q(offer_active=True) & (Q(discount_approved_products=product) | Q(discount_approved_category=category))
        ).exists()

        if discount_allowed:
            return "Discount Allowed"
        
        return "normal"
    
    



class CartModelSerializers(serializers.ModelSerializer):
    class Meta :
        model = Cart
        fields = "__all__"


class ProductViewSerializers(serializers.ModelSerializer):
    mainCategory = serializers.CharField(source ='category.category.pk')
    class Meta :
        model = Product
        fields = ['id','name','image','salePrice','mainCategory','category','short_description','description','price','slug']


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
        fields = ['first_name','last_name','email','password','zip_code','place','image','phone']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price','']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'updated_at', 'status', 'total_amount', 'address', 'items','payment_method','coupon',"payment_id"]



class SingleProductSerilizers(serializers.ModelSerializer):
    class Meta :
        model = ProductColorStock
        fields = "__all__"


class SingleProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='product.type')
    class Meta:
        model = ProductColorStock
        fields = ['id', 'product', 'color', 'image1', 'image2', 'image3','image4','image5','type','stock']




class VariantProductColorStock(serializers.ModelSerializer):
    class Meta :
        model = ProductVariant
        fields = "__all__"



class VariantProductSerializer(serializers.ModelSerializer):
    stock_info = serializers.SerializerMethodField()
    type = serializers.CharField(source='product.type')

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'color', 'image1', 'image2', 'image3', 'image4', 'image5', 'stock_info', 'type']

    def get_stock_info(self, obj):
        size_stocks = ProductVarientSizeStock.objects.filter(product_variant_id=obj.id)
        return [
            {'size': size_stock.size, 'stock': size_stock.stock}
            for size_stock in size_stocks
        ]
    
class ProductVarientSizeStockSerializers(serializers.ModelSerializer):
    class Meta :
        model = ProductVarientSizeStock
        fields = "__all__"




class CustomerOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class CustomerAllOrderSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(source ='product.image')
    name = serializers.CharField(source ='product.name')
    price_ = serializers.CharField(source ='product.price')
    sale_price = serializers.IntegerField(source ='product.salePrice')
    status = serializers.CharField(source ='order.status')


    class Meta:
        model = OrderItem
        fields = ['customer','order','product','quantity','created_at','color','size','price','image','name','price_','sale_price','status']


class CustomerOrderItems(serializers.ModelSerializer):
    productName = serializers.CharField(source ='product.name')
    productImage = serializers.ImageField(source ='product.image')
    salePrice = serializers.CharField(source ='product.salePrice')
    status = serializers.CharField(source ='order.status')
    price = serializers.CharField(source ='product.price')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price','productImage','productName','order','salePrice','created_at','color','size','status','free_quantity']



class RecentlyViewedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyViewedProduct
        fields = ['user', 'product', 'viewed_at']

class RecomendedProductSerializer(serializers.ModelSerializer):
    mainCategory = serializers.IntegerField(source ='category.category.pk')
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'salePrice', 'image','mainCategory','slug'] 



class UserProfileSerializers(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ['image']




class CouponSerilizers(serializers.ModelSerializer):
    class Meta :
        model = Coupon
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta :
        model = Blog
        fields = "__all__"


class CustomerCoinSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = "__all__"



class CoinValueModelSerilizers(serializers.ModelSerializer):
    class Meta :
        model = CoinValue
        fields = ['value']



class ReviewModelSerilizers(serializers.ModelSerializer):
    first_name = serializers.CharField(source ='user.first_name')
    last_name = serializers.CharField(source ='user.last_name')
    image = serializers.ImageField(source ='user.image')

    class Meta:
        model = Review
        fields = ['id','user','product','rating','review_text','status','created_at','first_name','last_name','image']




class ReviewAddingModelSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"



class OfferModelSerilizers(serializers.ModelSerializer):

    class Meta:
        model = OfferSchedule
        fields = "__all__"