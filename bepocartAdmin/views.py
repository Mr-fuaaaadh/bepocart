import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import *
from bepocartBackend.serializers import *
from django.db import IntegrityError, DatabaseError
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from django.contrib.auth import get_user_model
User = get_user_model() 

class AdminRegister(APIView):
    def post(self, request):

        try:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registration is successfully completed", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid request", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminLogin(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            print(f"Email: {email}, Password: {password}")

            user = User.objects.filter(email=email).first()
            if user:
                if check_password(password, user.password):
                    try:
                        payload = {
                            'id': user.pk,
                            'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
                        }
                        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                        if isinstance(token, bytes):
                            token = token.decode('utf-8')

                        response = Response({"token": token}, status=status.HTTP_200_OK)
                        response.set_cookie('token', token, httponly=True, secure=True)
                        return response
                    except Exception as e:
                        print(f"Token generation error: {e}")
                        return Response({"error": "Token generation failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": "Invalid or Incorrect Email Or Password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



###################################################### Carousal ##################################################333####3

class CarousalAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CarousalSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Carousal added successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class CarousalView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            print("Authorization header:", token)
            if token is None:
                print("Unauthenticated")
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                print("Token has expired")
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                print("Invalid token")
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                print("Invalid token payload")
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            carousal = Carousal.objects.all()
            serializer = CarousalSerializers(carousal, many=True)
            return Response({"status": "success", "message": "Fetched all Carousals", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class CarousalUpdate(APIView):
    def get(self, request, pk):
        try:
            carousal = Carousal.objects.filter(pk=pk).first()
            if carousal is None:
                return Response({"status": "error", "message": "Banner image not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CarousalSerializers(carousal)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                carousal = Carousal.objects.get(pk=pk)
                print(carousal.pk)
            except Carousal.DoesNotExist:
                return Response({"message": "Carousal not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CarousalSerializers(carousal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Carousal updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CarousalDelete(APIView):
    def get(self, request, pk):
        try:
            carousal = Carousal.objects.filter(pk=pk).first()
            if carousal is None:
                return Response({"status": "error", "message": "Banner image not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CarousalSerializers(carousal)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            print("Authorization header:", token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                carousal = Carousal.objects.get(pk=pk)
                carousal.delete()
                return Response({"status": "success", "message": "Banner image deleted successfully"}, status=status.HTTP_200_OK)
            except Carousal.DoesNotExist:
                return Response({"status": "error", "message": "Banner image not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




################################################################# OFFER BANNER ##########################################################################



class OfferBannerAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            try:
                serializer = OfferBannerSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "message": "Offer banner added successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"status": "error", "message": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class OfferBannerView(APIView):
     def get(self, request):
        try:
            token = request.headers.get('Authorization')
            print("data",token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            banner = OfferBanner.objects.all()
            serializer = OfferBannerSerializers(banner, many=True)
            return Response({"status": "success", "message": "Fetched all offer banner", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class OfferBannerDelete(APIView):
    def get(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            banner = OfferBanner.objects.filter(pk=pk).first()
            if banner is None:
                return Response({"status": "error", "message": "Offer Banner image not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OfferBannerSerializers(banner)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                banner = OfferBanner.objects.get(pk=pk)
                banner.delete()
                return Response({"status": "success", "message": "Pffer Banner image deleted successfully"}, status=status.HTTP_200_OK)
            except OfferBanner.DoesNotExist:
                return Response({"status": "error", "message": "Offer Banner image not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class OfferBannerUpdate(APIView):
    def get(self, request, pk):
        try:
            banner = OfferBanner.objects.filter(pk=pk).first()
            if banner is None:
                return Response({"status": "error", "message": " Offer Banner image not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OfferBannerSerializers(banner)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                banner = OfferBanner.objects.get(pk=pk)
            except OfferBanner.DoesNotExist:
                return Response({"message": "Offer banner  not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OfferBannerSerializers(banner, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Offer Banner updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    


            








##################################################################3  Category #############################################################################

class CategoryAdd(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            print("headers token   :",token)
            if token is None:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError as e:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError as e:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            id = payload.get('id')
            if id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = User.objects.filter(pk=id).first()
            if user is None:
                return Response({"error":"user not found"},status=status.HTTP_404_UNAUTHORIZED)
                # return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"message": "User authenticated", "id": id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Categories(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            print("headers token:", token)
            if token is None:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            categories = Category.objects.all().order_by('id')
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDelete(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, many=False)
            return Response({"message": "Category fetch successfully completed", "data": serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            print("headers token:", token)
            if token is None:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CategoryUpdate(APIView):

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response({"message": "Category fetch successful", "data": serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




###############################################   SUBACTEGORY     ###################################################




class SubcategoryAdd(APIView):
    def post(self, request):        
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SubcategoryModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Subcategory successfully created"}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class SubcategoryView(APIView):
    def get(self, request):
       
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            subcategories = Subcategory.objects.all()
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubcategoryUpdate(APIView):
    def get(self, request,pk):
        try:
            subcategories = Subcategory.objects.get(pk=pk)
            serializer = SubCategoryUpdateSerializers(subcategories, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def put(self,request,pk):
        try :
            token = request.headers.get('Authorization')
            if not token:
                return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            subcategory = Subcategory.objects.get(pk=pk)
            serializer = CategorySerializer(subcategory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Sub Category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubcategoryDelete(APIView):
    def get(self, request,pk):
        try:
            token = request.headers.get('Authorization')
            print(token)
            if not token:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            subcategories = Subcategory.objects.get(pk=pk)
            serializer = SubcategorySerializer(subcategories, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try :
            token = request.headers.get('Authorization')
            print(token)
            if not token:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except DecodeError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError:
                return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            subcategory = Subcategory.objects.get(pk=pk)
            subcategory.delete()
            return Response({"status":"success","messege":"Subcatecory delete successfuly completed"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#######################################  PRODUCT MANAGEMENT ########################################

class ProductAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product successfully created"}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProductView(APIView):
    def get(self, request):
        try :
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            products = Product.objects.filter(offer_type__isnull=True).order_by('id')
            serializer = ProductSerializerView(products,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
        
    

    
class ProductUpdate(APIView):

    def get(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
        
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, many=False)
            return Response({"message": "Product details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Exception: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            print("token   :",token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
        
            product = Product.objects.filter(pk=pk).first()
            if not product:
                print("product not found")
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"Exception: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProductDelete(APIView):
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




###################################################### OFFER PRODUCTS #####################################################################

class OfferProductAdd(APIView):
    def post(self, request):
        try :
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = OfferProductSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Offer product added successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e :
            return Response({"anid"})



class OfferProductView(APIView):
    def get(self, request):
        try:

            token = request.headers.get('Authorization')
            print(token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
           
            products = Product.objects.filter(offer_type__isnull=False).order_by('id')
            serializer = OfferProductSerializers(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (DecodeError, InvalidTokenError):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class OfferProductDelete(APIView):
    def get(self,request,pk):
        try :
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product = Product.objects.filter(pk=pk).first()
            if not product :
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = OfferProductSerializers(product, many=False)
            return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,pk):
        try :
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                product =Product.objects.filter(pk=pk).first()
                if not product :
                    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                product.delete()
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class OfferProductUpdate(APIView):

    def get(self,request,pk):
        try :
            product = Product.objects.filter(pk=pk).first()
            if not product :
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = OfferProductSerializers(product, many=False)
            return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def put(self,request,pk):
        try :
            token = request.headers.get('Authorization')
            if not token :
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                product = Product.objects.filter(pk=pk).first()
                if not product:
                    return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = OfferProductSerializers(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
                print("error    :",serializer.errors)
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





################################################### ORDER MANAGEMENT #######################################################


class AllOrders(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                order_products = Order.objects.all()
                serializer = AdminOrderViewsSerializers(order_products, many=True)
                return Response({"message": "Orders fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print("Exception:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OrderStatusUpdation(APIView):
    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                order = Order.objects.filter(pk=pk).first()
                if not order:
                    return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

                new_status = request.data.get('status')
                if not new_status:
                    return Response({"error": "No status provided"}, status=status.HTTP_400_BAD_REQUEST)

                order.status = new_status
                order.save()

                return Response({"status": "Order status updated successfully"}, status=status.HTTP_200_OK)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print("Exception:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class AllOrderItems(APIView):
    def get(self, request,customer):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if not user_id:
                    return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

                user = User.objects.filter(pk=user_id).first()
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                # Fetch orders belonging to the authenticated user
                order_products = OrderItem.objects.filter(order=customer)
                serializer = CustomerOrderItems(order_products, many=True)
                return Response({"message": "Orders fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
        
            

class ProductImageCreateView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            print("Product ID:", product.pk)
        except Product.DoesNotExist:
            return Response({'status': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as db_error:
            print("Database error:", db_error)
            return Response({'status': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = request.data
        data['product'] = product.pk

        serializer = ProductImageSerializer(data=data)
        if serializer.is_valid():
            try:
                product_image = serializer.save()
                size_ids = data.getlist('size', [])
                size_ids = [int(size_id) for size_id in size_ids]
                sizes = Size.objects.filter(id__in=size_ids)
                if sizes.count() != len(size_ids):
                    return Response({'status': 'One or more size IDs are invalid'}, status=status.HTTP_400_BAD_REQUEST)
                
                product_image.size.set(sizes)  # Ensure 'sizes' is the correct field name

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as integrity_error:
                print("Integrity Error:", integrity_error)
                return Response({'status': 'Integrity error occurred'}, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError as db_error:
                print("Database Error:", db_error)
                return Response({'status': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductBasdMultipleImageView(APIView):
    def get(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            print(token)
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            

            product = Product.objects.filter(pk=pk).first()
            print("Product ID :",product)
            if product is None:
                return Response({"message": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
            product_images = ProducyImage.objects.filter(product=product)
            serializer = ProductSerializerWithMultipleImage(product_images, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductMultipleImageDelete(APIView):
    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product_image = ProducyImage.objects.filter(pk=pk).first()
            if product_image is None:
                return Response({"message": "Product Image not found"}, status=status.HTTP_404_NOT_FOUND)
            product_image.delete()
            return Response({"message": "Product Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductSizeAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSizeSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class ProductSizeView(APIView):
    def get(self, request):
        try:
            sizes = Size.objects.all()
            serializer = ProductSizeSerializers(sizes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class AdminCouponCreation(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data.copy()  # Make a copy of request data
            data['discount_product'] = list(map(int,data.get('discount_product', [])))
            data['discount_category'] = list(map(int, data.get('discount_category', [])))

            serializer = AdminCoupenSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response({"message": "Coupon created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return Response({"error": "Validation Error", "details": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as ie:
            return Response({"error": "Integrity Error", "details": str(ie)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as de:
            return Response({"error": "Database Error", "details": str(de)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminCoupensView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            coupons = Coupon.objects.all()
            data = Coupon.objects.all()
            for i in data :
                print(i.start_date)
                print(i.end_date)

            serializer = AdminallCoupenSerializers(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdminCouponDelete(APIView):
    def delete(self,request,pk):
        try :
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            coupons = Coupon.objects.filter(pk=pk).first()
            if coupons is None:
                return Response({"error": "Coupon not found"}, status=status.HTTP_404_NOT_FOUND)
            coupons.delete()
            return Response({"status": "success", "message": "Coupon deleted successfully"}, status=status.HTTP_200_OK)  


        except Exception as e:
            return Response({"error": "Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AdminCouponUpdate(APIView):
    
    def get(self, request, pk):
        try:
            coupon = Coupon.objects.filter(pk=pk).first()
            if not coupon:
                return Response({"error": f"Coupon with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = AdminCoupenSerializers(coupon)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                coupon = Coupon.objects.get(pk=pk)
            except Coupon.DoesNotExist:
                return Response({"error": f"Coupon with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = AdminCoupenSerializers(coupon, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class AdminBlogCreate(APIView):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BlogSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminBlogView(APIView):
    def get(self, request,):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            blog = Blog.objects.all()
            serializer = BlogSerializers(blog, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AdminBlogDelete(APIView):
    def get(self, request, pk):
        try:
            blog = Blog.objects.filter(pk=pk).first()
            if blog is None:
                return Response({'error': "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BlogSerializers(blog)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            blog = Blog.objects.filter(pk=pk).first()
            if blog is None:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
            
            blog.delete()
            return Response({"success": "Blog deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AdminBlogUpdate(APIView):
    def get(self, request, pk):
        try:
            blog = Blog.objects.filter(pk=pk).first()
            if blog is None:
                return Response({'error': "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BlogSerializers(blog)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, pk):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            blog = Blog.objects.filter(pk=pk).first()
            if blog is None:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BlogSerializers(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Blog update successfully completed", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AdminCustomerView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get('id')
            if user_id is None:
                return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            customers = Customer.objects.all()
            serializer = AdminCustomerViewSerilizers(customers, many=True)  
            return Response({"message": "Customers data fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Exception status: {str(e)}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




        



            
            

            

        





        