import jwt
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from bepocartBackend.serializers import *
from bepocartAdmin.serializers import *
from bepocartBackend.models import *
from bepocartAdmin.models import *
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Q
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.db import transaction


class CustomerRegistration(APIView):
    def post(self, request):
        try:
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Registration successfully completed",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "error",
                    "message": "Registration failed",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CustomerLogin(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            customer = Customer.objects.filter(email=email).first()

            if customer and customer.check_password(password):
                # Generate JWT token
                expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
                userToken = {
                    'id': customer.pk,
                    'email': customer.email,
                    'exp': expiration_time,
                    'iat': datetime.utcnow()
                }
                token = jwt.encode(userToken, settings.SECRET_KEY, algorithm='HS256')


                # Set JWT token in cookies
                response = Response({
                    "status": "success",
                    "message": "Login successful",
                    "token": token
                }, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='token',
                    value=token,
                    httponly=True,
                    samesite='Lax',
                    # secure=settings.SECURE_COOKIE
                )
                return response
            else:
                return Response({
                    "status": "error",
                    "message": "Invalid email or password"
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



################################################  HOME    #############################################

class CategoryView(APIView):
    def get(self, request):
        try :
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            },status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubcategoryView(APIView):
    def get(self, request,pk):
        try :
            subcategories = Subcategory.objects.filter(category=pk)
            serializer = SubcatecorySerializer(subcategories, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            },status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerProductView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductViewSerializer(products, many=True)
            return Response({"products": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerCarousalView(APIView):
    def get(self, request):
        try:
            banner = Carousal.objects.all()
            serializer = CarousalSerializers(banner, many=True)
            return Response({"banner": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CustomerOfferBannerView(APIView):
    def get(self, request):
        try:
            banner = OfferBanner.objects.all()
            serializer = OfferBannerSerializers(banner, many=True)
            return Response({"banner": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

class SubcategoryBasedProducts(APIView):
    def get(self, request, pk):
        try:
            subcategory = Subcategory.objects.filter(pk=pk).first()
            print(subcategory)
        except Subcategory.DoesNotExist:
            return Response({"message": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=subcategory)
        serializer = SubcatecoryBasedProductView(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)




from django.db import IntegrityError

class CustomerAddProductInWishlist(APIView):
    def post(self, request, pk):
        try:
            # Retrieve the token from the request headers
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            # Decode the JWT token
            try:
                user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                return Response({"message": f"Invalid token: {e}"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = user_token.get('id')
            if not user_id:
                return Response({"message": "Invalid token userToken"}, status=status.HTTP_401_UNAUTHORIZED)

            # Check if the user exists
            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the product exists
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

           
            # Check if the product is already in the user's wishlist
            if Wishlist.objects.filter(user=user, product=product).exists():
                return Response({"message": "Product already exists in the wishlist"}, status=status.HTTP_400_BAD_REQUEST)
            
             # Update or create the recently viewed product entry
            recently_viewed, created = RecentlyViewedProduct.objects.get_or_create(user=user, product=product)
            if not created:
                recently_viewed.viewed_at = timezone.now()
                recently_viewed.save()

            # Add the product to the wishlist
            wishlist_data = {'user': user.pk, 'product': product.pk}
            wishlist_serializer = WishlistSerializers(data=wishlist_data)
            if wishlist_serializer.is_valid():
                wishlist_serializer.save()
                return Response({"message": "Product added to wishlist successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Unable to add product to wishlist", "errors": wishlist_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({"message": "Product already exists in the wishlist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CustomerWishlist(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            print("Token:", token)  

            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                userToken = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                return Response({"message": "Invalid token: " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = userToken.get('id')

            if not user_id:
                return Response({"message": "Invalid token userToken"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
            wishlist = Wishlist.objects.filter(user=user.pk)
            serializer = WishlistSerializersView(wishlist, many=True)
            return Response({"status":"User wishlist products","data":serializer.data},status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class CustomerProductDeleteInWishlist(APIView):
    def delete(self, request, pk):
        try:
            product = Wishlist.objects.filter(pk=pk).first()
            if product is None:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomerProductInCart(APIView):
    def post(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product = Product.objects.get(pk=product.pk)
            recently_viewed, created = RecentlyViewedProduct.objects.get_or_create(user=user, product=product)
            if not created:
                recently_viewed.viewed_at = timezone.now()
                recently_viewed.save()
                


            # Check if the product is already in the user's Cart
            if Cart.objects.filter(customer=user, product=product).exists():
                return Response({"message": "Product already exists in the cart"}, status=status.HTTP_400_BAD_REQUEST)

            cart_data = {'customer': user.pk, 'product': product.pk}
            serializer = CartModelSerializers(data=cart_data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product added to cart successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Unable to add product to cart", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        except IntegrityError:
            return Response({"message": "Product already exists in the cart"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.DecodeError, jwt.InvalidTokenError) as e:
            return Response({"message": f"Invalid token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)




class CustomerCartProducts(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            print("Token:", token)

            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                userToken = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                return Response({"message": "Invalid token: " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = userToken.get('id')

            if not user_id:
                return Response({"message": "Invalid token userToken"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
            cart = Cart.objects.filter(customer=user)
            if not cart:
                return Response({"message": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CartSerializers(cart, many=True)

            # Calculate total price, discounted price, and total quantity
            total_price = 0
            total_discounted_price = 0
            for item in cart:
                product = item.product
                original_price = product.price if product.price is not None else 0
                sale_price = product.salePrice if product.salePrice is not None else original_price
                quantity = item.quantity
                
                total_price += original_price * quantity
                total_discounted_price += sale_price * quantity
            
            if total_discounted_price <= 500 :
                shipping_fee = 60
                Subtottal = total_discounted_price + shipping_fee
            else :
                shipping_fee = 0
                Subtottal = total_discounted_price + shipping_fee


            response_data = {
                "status": "User cart products",
                "data": serializer.data,
                "Discount": total_price,
                "Shipping Charge ": shipping_fee,
                "Total Price": total_discounted_price,
                "Subtottal": Subtottal

            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CartProductDelete(APIView):
    def get(self,request,pk):
        try :
            product = Cart.objects.filter(pk=pk).first()
            if product is None :
                return Response({"message": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CartModelSerializers(product, many=False)
            return Response({"message": "Product Fetch from cart",'data':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self,request,pk):
        try :
            product = Cart.objects.filter(pk=pk).first()
            if product is None :
                return Response({"message": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response({"message": "Product Delete from cart"}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

            

class IncrementProductQuantity(APIView):

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            cart_item = Cart.objects.filter(customer=user,pk=pk).first()
            if not cart_item:
                return Response({"message": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

            cart_item.quantity += 1
            cart_item.save()

            return Response({"message": "Product quantity increased successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None

class DecrementProductQuantity(APIView):
    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            cart_item = Cart.objects.filter(customer=user, pk=pk).first()
            if not cart_item:
                return Response({"message": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return Response({"message": "Product quantity decreased successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Quantity cannot be less than 1"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None



class OfferBanerBasedProducts(APIView):
    def post(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            offer = OfferBanner.objects.filter(pk=pk).first()
            if not offer:
                return Response({"message": "Offer banner not found"}, status=status.HTTP_404_NOT_FOUND)

            products = Product.objects.filter(offer_banner=offer.pk)
            serializer = ProductViewSerializers(products, many=True)
            if serializer:
                return Response({'products':serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': "Products not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None
        


class ProductBigView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.filter(pk=pk).first()
            if product:
                serializer = OfferProductSerializers(product)
                return Response({'product':serializer.data}, status=status.HTTP_200_OK)
            return Response({'message':"product not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MianCategoryBasedProducts(APIView):
    def get(self, request, pk):
        try:
            main_category = Category.objects.filter(pk=pk).first()
            if main_category:
                products = Product.objects.filter(category__category=main_category)
                serializer = ProductViewSerializers(products, many=True)
                return Response({'products':serializer.data}, status=status.HTTP_200_OK)
            return Response({'message':"Category not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserPasswordReset(APIView):
    def put(self, request):
        try:
            token = request.headers.get('Authorization')
            print(token)
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                old_password = serializer.validated_data.get('old_password')
                new_password = serializer.validated_data.get('new_password')
                confirm_password = serializer.validated_data.get('confirm_password')

                # Check if the old password matches the user's current password
                if old_password and not check_password(old_password, user.password):
                    return Response({"message": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

                # Check if the new password and confirm password match
                if new_password != confirm_password:
                    return Response({"message": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

                # Update the user's password
                user.password = make_password(new_password)
                user.save()

                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None


class UserAddressAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            address_data = request.data.copy()
            address_data['user'] = user.id
            serializer = AddressSerializer(data=address_data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Address added successfully"}, status=status.HTTP_201_CREATED)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({"message": "Address already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.DecodeError, jwt.InvalidTokenError) as e:
            return Response({"message": f"Invalid token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
        


class UserAddressView(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            userAddress = Address.objects.filter(user=user.pk)
            serializer = AddressSerializer(userAddress, many=True)
            return Response({'address': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None




class UserAddressUpdate(APIView):
    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            userAddress = Address.objects.filter(pk=pk).first()
            if not userAddress:
                return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = AddressUpdateSerializer(userAddress, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None



class UserAddressDelete(APIView):
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            userAddress = Address.objects.filter(pk=pk).first()
            if not userAddress:
                return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

            userAddress.delete()
            return Response({"message": "Address deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None



class UserSearchProductView(APIView):
    def post(self, request):
        try:
            query = request.query_params.get('q', '')
            print
            if not query:
                return Response({"message": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Search products by name, description, short description, and category name
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(short_description__icontains=query) 
                # Q(category__name_icontains=query)
            )

            if products.exists():
                serializer = ProductSerializerView(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No products found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            

class HighToLowProducts(APIView):
    def post(self, request, pk):
        try:
            sort_order = request.query_params.get('sort', 'high_to_low')
            category = Subcategory.objects.filter(pk=pk).first()
            
            if not category:
                return Response({"message": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

            if sort_order == 'high_to_low':
                products = Product.objects.filter(category=category.pk).order_by('-salePrice')
            elif sort_order == 'low_to_high':
                products = Product.objects.filter(category=category.pk).order_by('salePrice')
            else:
                return Response({"message": "Invalid sort order"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LowToHighProducts(APIView):
    def post(self, request,pk):
        try:
            sort_order = request.query_params.get('sort', 'low_to_high')
            category = Subcategory.objects.filter(pk=pk).first()

            if not category:
                return Response({"message": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

            if sort_order == 'low_to_high':
                products = Product.objects.filter(category=category.pk).order_by('salePrice')
            elif sort_order == 'high_to_low' : 
                products = Product.objects.filter(category=category.pk).order_by('-salePrice')
            else:
                return Response({"message": "Invalid sort order"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = Customer.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            otp_instance = OTP.objects.filter(user=user).first()
            if otp_instance:
                otp = random.randint(100000, 999999)
                otp_instance.otp = otp
                otp_instance.save()
            else:
                otp = random.randint(100000, 999999)
                OTP.objects.create(user=user, otp=otp)
            
            # Render email template with OTP value
            email_body = render_to_string('otp.html', {'otp': otp})

            # Send email
            send_mail(
                'Your OTP Code',
                '',
                settings.EMAIL_HOST_USER,  
                [email],  
                fail_silently=False,
                html_message=email_body
            )
            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            print(email)
            print(otp)
            if not otp :
                return Response({"message": "OTP not found"}, status=status.HTTP_404_NOT_FOUND)


            user = Customer.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            valid_otp = OTP.objects.filter(user=user, otp=otp).first()
            if not valid_otp:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            # OTP verified, proceed to change password
            return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']


            user = Customer.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            if new_password != confirm_password :
                return Response({"message": "Password is not match !"}, status=status.HTTP_404_NOT_FOUND)
            
            user.password = make_password(new_password)
            user.save()

            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileUpdate(APIView):
    def get(self,request):
        try:
            token = request.COOKIES.get('token')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
            serializer = UserProfileSErilizers(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None

    def put(self,request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
            serializer = UserProfileSErilizers(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None




class CreateOrder(APIView):
    def post(self, request, pk):
        # Check if token exists in cookies
        token = request.COOKIES.get('token')
        if not token:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode and verify the user token
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve user ID from the token
        user_id = user_token.get('id')
        if not user_id:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve user from the database
        user = Customer.objects.filter(pk=user_id).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if cart is empty
        cart_items = Cart.objects.filter(customer=user)
        if not cart_items.exists():
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve and validate address
        address = Address.objects.filter(pk=pk, user=user).first()
        if not address:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Create order within a transaction
            with transaction.atomic():
                order = Order.objects.create(customer=user, address=address, status='pending')

                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.salePrice * item.quantity
                    )

                    # Deduct stock from product
                    item.product.stock -= item.quantity
                    item.product.save()

                # Calculate the total price of the order
                order.calculate_total()

                # Clear the cart after ordering
                cart_items.delete()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class DiscountSaleProducts(APIView):
    def get(self, request):
        try:
            discount_sale = Product.objects.filter(offer_type="DISCOUNT SALE").order_by('-pk')
            serializer = SubcatecoryBasedProductView(discount_sale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'No products found for discount sale'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FlashSaleProducts(APIView):
    def get(self, request):
        try:
            discount_sale = Product.objects.filter(offer_type="FLASH SALE").order_by('-pk')
            serializer = SubcatecoryBasedProductView(discount_sale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'No products found for flash sale'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FIftypercontageProducts(APIView):
    def get(self, request):
        try:
            discount_sale = Product.objects.filter(offer_type="50 %").order_by('-pk')
            serializer = SubcatecoryBasedProductView(discount_sale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'No products found for 50 percantage sale'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BuyOneGetOneOffer(APIView):
    def get(self, request):
        try:
            discount_sale = Product.objects.filter(offer_type="BUY 1 GET 1").order_by('-pk')
            serializer = SubcatecoryBasedProductView(discount_sale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'No products found for BUY 1 GET 1 sale'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BuyToGetOne(APIView):
    def get(self, request):
        try:
            discount_sale = Product.objects.filter(offer_type="BUY 2 GET 1").order_by('-pk')
            serializer = SubcatecoryBasedProductView(discount_sale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'No products found for BUY 2 GET 1 sale'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ProducViewWithMultipleImage(APIView):
    def get(self, request, pk):
        try:
            product = ProducyImage.objects.filter(product_id=pk)
            serializer = ProductSerializerWithMultipleImage(product,many=True)
            return Response({"product":serializer.data},status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserProfileView(APIView):
    def post(self,request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
            serializer = UserProfileSErilizers(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None



class CustomerOrders(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('token')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            user_orders = Order.objects.filter(customer=user)
            if not user_orders.exists():
                return Response({"message": "No orders found for this user"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerOrderSerializers(user_orders, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None
        


class CustomerOrderProducts(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.filter(pk=pk).first()
            if not order:
                return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            
            order_items = OrderItem.objects.filter(order=order)
            if not order_items.exists():
                return Response({"message": "No items found for this order"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerOrderItems(order_items, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class RecentlyViewedProductsView(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            recently_viewed = RecentlyViewedProduct.objects.filter(user=user).select_related('product').order_by('-pk')[:10]
            products = [item.product for item in recently_viewed]
            serializer = RecomendedProductSerializer(products, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, product_id):
    #     try:
    #         token = request.COOKIES.get('token')
    #         if not token:
    #             return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user_id = self._validate_token(token)
    #         if not user_id:
    #             return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user = Customer.objects.filter(pk=user_id).first()
    #         if not user:
    #             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    #         product = Product.objects.get(pk=product_id)
    #         recently_viewed, created = RecentlyViewedProduct.objects.get_or_create(user=user, product=product)
    #         if not created:
    #             recently_viewed.viewed_at = timezone.now()
    #             recently_viewed.save()

    #         return Response({"message": "Product added to recently viewed"}, status=status.HTTP_200_OK)
    #     except Product.DoesNotExist:
    #         return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None
        


class RecommendedProductsView(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch recently viewed products by the user
            recently_viewed_products = RecentlyViewedProduct.objects.filter(user=user).values_list('product', flat=True).order_by('-pk')

            # Fetch products from user's orders
            ordered_products = OrderItem.objects.filter(order__customer=user).values_list('product', flat=True)

            # Combine recently viewed and ordered products to find similar ones
            product_ids = list(set(recently_viewed_products) | set(ordered_products))

            if not product_ids:
                return Response({"message": "No recommendations available"}, status=status.HTTP_200_OK)

            # Fetch products that are similar to the ones the user interacted with
            similar_products = Product.objects.filter(category__products__id__in=product_ids).exclude(id__in=product_ids).distinct()[:10]

            # Serialize the recommended products
            serializer = RecomendedProductSerializer(similar_products, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def _validate_token(self, token):
        try:
            user_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return user_token.get('id')
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return None
class FilteredProductsView(APIView):
    def post(self, request,pk):
        try:
            min_price = request.data.get('min_price', 0)
            max_price = request.data.get('max_price', 1000000)
            category = Subcategory.objects.filter(pk=pk).first()
            

            filtered_products = Product.objects.filter(category=category,salePrice__gte=min_price, salePrice__lte=max_price)
            serializer = ProductSerializer(filtered_products, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)