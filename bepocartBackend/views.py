import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from bepocartBackend.serializers import *
from bepocartAdmin.serializers import *
from bepocartBackend.models import *
from bepocartAdmin.models import *
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError



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
                
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the product is already in the user's wishlist
            if Wishlist.objects.filter(user=user, product=product).exists():
                return Response({"message": "Product already exists in the wishlist"}, status=status.HTTP_400_BAD_REQUEST)

            wishlist_data = {'user': user.pk, 'product': product.pk}
            wishlist_serializer = WishlistSerializers(data=wishlist_data)
            if wishlist_serializer.is_valid():
                wishlist_serializer.save()
                return Response({"message": "Product added to wishlist successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Unable to add product to wishlist", "errors": wishlist_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        except IntegrityError as e:
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
            serializer = WishlistSerializers(wishlist, many=True)
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
                
            cart = Cart.objects.filter(customer=user.pk)
            serializer = CartSerializers(cart, many=True)
            return Response({"status":"User wishlist products","data":serializer.data},status=status.HTTP_200_OK)
                
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
            if not token:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = self._validate_token(token)
            if not user_id:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Customer.objects.filter(pk=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({"message": "New password not provided"}, status=status.HTTP_400_BAD_REQUEST)

            
            user.password = make_password(new_password)
            user.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

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

        









