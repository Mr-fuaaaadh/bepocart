import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import *
from bepocartBackend.serializers import *
from django.db import IntegrityError, DatabaseError
from .models import *
from datetime import datetime, timedelta
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
                            'exp': datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
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
                    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



###################################################### Carousal ##################################################333####3

class CarousalAdd(APIView):
    def post(self, request):
        try:
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                carousal = Carousal.objects.get(pk=pk)
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
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
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
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
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
            # token = request.COOKIES.get('token')
            # if token is None:
            #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # user_id = payload.get('id')
            # if user_id is None:
            #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            banner = OfferBanner.objects.all()
            serializer = OfferBannerSerializers(banner, many=True)
            return Response({"status": "success", "message": "Fetched all offer banner", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class OfferBannerDelete(APIView):
    def get(self, request, pk):
        try:
            banner = OfferBanner.objects.filter(pk=pk).first()
            if banner is None:
                return Response({"status": "error", "message": "Offer Banner image not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OfferBannerSerializers(banner)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            # # token = request.COOKIES.get('token')
            # # if token is None:
            # #     return Response({"status": "error", "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # # try:
            # #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # # except ExpiredSignatureError:
            # #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # # except (DecodeError, InvalidTokenError):
            # #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            # # user_id = payload.get('id')
            # # if user_id is None:
            # #     return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.filter(pk=user_id).first()
            # if user is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
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
            token = request.COOKIES.get('token')
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
                banner = OfferBannerSerializers.objects.get(pk=pk)
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
            token = request.COOKIES.get('token')
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
            categories = Category.objects.all()
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

    def authenticate(self, request):
        token = request.COOKIES.get('token')
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
        
        return user, None

    def get(self, request):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        
        try:
            subcategories = Subcategory.objects.all().values()
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        
        try:
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
            subcategories = Subcategory.objects.all()
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubcategoryUpdate(APIView):
    # def authenticate(self, request):
    #     token = request.COOKIES.get('token')
    #     if not token:
    #         return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #     except ExpiredSignatureError:
    #         return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    #     except DecodeError:
    #         return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    #     except InvalidTokenError:
    #         return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    #     user_id = payload.get('id')
    #     if not user_id:
    #         return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    #     user = User.objects.filter(pk=user_id).first()
    #     if not user:
    #         return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     return user, None

    def get(self, request,pk):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        
        try:
            subcategories = Subcategory.objects.get(pk=pk)
            serializer = SubcategorySerializer(subcategories, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def put(self,request,pk):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response

        try :
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
    # def authenticate(self, request):
    #     token = request.COOKIES.get('token')
    #     if not token:
    #         return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #     except ExpiredSignatureError:
    #         return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    #     except DecodeError:
    #         return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    #     except InvalidTokenError:
    #         return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    #     user_id = payload.get('id')
    #     if not user_id:
    #         return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    #     user = User.objects.filter(pk=user_id).first()
    #     if not user:
    #         return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     return user, None

    def get(self, request,pk):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        
        try:
            subcategories = Subcategory.objects.get(pk=pk)
            serializer = SubcategorySerializer(subcategories, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, pk):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        try :
            subcategory = Subcategory.objects.get(pk=pk)
            subcategory.delete()
            return Response({"status":"success","messege":"Subcatecory delete successfuly completed"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#######################################  PRODUCT MANAGEMENT ########################################

class ProductAdd(APIView):
    # def authenticate(self, request):
    #         token = request.COOKIES.get('token')
    #         if not token:
    #             return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
    #         try:
    #             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #         except ExpiredSignatureError:
    #             return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    #         except DecodeError:
    #             return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    #         except InvalidTokenError:
    #             return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user_id = payload.get('id')
    #         if not user_id:
    #             return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user = User.objects.filter(pk=user_id).first()
    #         if not user:
    #             return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
    #         return user, None


    def post(self, request):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product successfully created"}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProductView(APIView):

    # def authenticate(self, request):
    #         token = request.COOKIES.get('token')
    #         if not token:
    #             return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
    #         try:
    #             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #         except ExpiredSignatureError:
    #             return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    #         except DecodeError:
    #             return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    #         except InvalidTokenError:
    #             return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user_id = payload.get('id')
    #         if not user_id:
    #             return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    #         user = User.objects.filter(pk=user_id).first()
    #         if not user:
    #             return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
    #         return user, None

    def get(self, request):

        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response
        try :
            products = Product.objects.filter(offer_type__isnull=True)
            serializer = ProductSerializerView(products,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
        
    

    
class ProductUpdate(APIView):
    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if not token:
            return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            return user, None
        except ExpiredSignatureError:
            return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (DecodeError, InvalidTokenError):
            return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response

        try:
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, many=False)
            return Response({"message": "Product details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response

        try:
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProductDelete(APIView):
    # # def authenticate(self, request):
    # #     token = request.COOKIES.get('token')
    # #     if not token:
    # #         return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    # #     try:
    # #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    # #         user_id = payload.get('id')
    # #         if not user_id:
    # #             return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    # #         user = User.objects.filter(pk=user_id).first()
    # #         if not user:
    # #             return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # #         return user, None
    # #     except ExpiredSignatureError:
    # #         return None, Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    # #     except (DecodeError, InvalidTokenError):
    # #         return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    # # def get(self, request, pk):
    # #     user, error_response = self.authenticate(request)
    # #     if error_response:
    # #         return error_response

    #     try:
    #         product = Product.objects.filter(pk=pk).first()
    #         if not product:
    #             return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    #         serializer = ProductSerializer(product, many=False)
    #         return Response({"message": "Product details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        # user, error_response = self.authenticate(request)
        # if error_response:
        #     return error_response

        try:
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
            token = request.COOKIES.get('token')
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
        token = request.COOKIES.get('token')
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

            products = Product.objects.filter(offer_type="DISCOUNT SALE")
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
            product = Product.objects.filter(pk=pk).first()
            if not product :
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = OfferProductSerializers(product, many=False)
            return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,pk):
        try :
            token = request.COOKIES.get('token')
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
            token = request.COOKIES.get('token')
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

                serializer = OfferProductSerializers(product, data=request.data, context={'user': user})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            except ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except (DecodeError, InvalidTokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AllOrders(APIView):
    def get(self, request):
        try:
            # token = request.COOKIES.get('token')
            # if not token:
            #     return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            #     user_id = payload.get('id')
            #     if not user_id:
            #         return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            #     user = User.objects.filter(pk=user_id).first()
            #     if not user:
            #         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                # Fetch orders belonging to the authenticated user
                order_products = Order.objects.all()
                serializer = AdminOrderSerializers(order_products, many=True)
                return Response({"message": "Orders fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AllOrderItems(APIView):
    def get(self, request,customer):
        try:
            # token = request.COOKIES.get('token')
            # if not token:
            #     return Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # try:
            #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            #     user_id = payload.get('id')
            #     if not user_id:
            #         return Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            #     user = User.objects.filter(pk=user_id).first()
            #     if not user:
            #         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            #     # Fetch orders belonging to the authenticated user
                order_products = OrderItem.objects.filter(order=customer)
                serializer = AdminOrderItemSerializers(order_products, many=True)
                return Response({"message": "Orders fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            # except ExpiredSignatureError:
            #     return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            # except (DecodeError, InvalidTokenError):
            #     return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
        
            

class ProductImageCreateView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'status': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError:
            return Response({'status': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = request.data.copy()  # Make a mutable copy of request data
        data['product'] = product.pk  # Set the product field in the data

        serializer = ProductImageSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'status': 'Integrity error occurred'}, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError:
                return Response({'status': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Log detailed serializer errors for debugging
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


