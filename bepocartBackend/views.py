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
                token = jwt.encode(userToken, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


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













