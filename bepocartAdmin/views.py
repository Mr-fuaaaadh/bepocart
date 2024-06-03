import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import *
from .models import *
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError

class AdminRegister(APIView):
    def post(self, request):
        try:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Admin registration is successfully completed", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid request", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AdminLogin(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = Admin.objects.filter(email=email, password=password).first()
            if user is not None:
                # Generate JWT token
                payload = {
                    'id': user.pk,
                    'exp': datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                token_str = token.decode('utf-8') 
                response = Response({"token": token_str}, status=status.HTTP_200_OK)
                response.set_cookie('token', token_str, httponly=True, secure=True)

                return response
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            
            user = Admin.objects.filter(pk=id).first()
            if user is None:
                return Response({"error":"user not found"},status=status.HTTP_404_UNAUTHORIZED)
                return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)

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

        user = Admin.objects.filter(pk=user_id).first()
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
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        
        try:
            serializer = SubcategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Subcategory successfully created"}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class SubcategoryView(APIView):
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

        user = Admin.objects.filter(pk=user_id).first()
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



class SubcategoryUpdate(APIView):
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

        user = Admin.objects.filter(pk=user_id).first()
        if not user:
            return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return user, None

    def get(self, request):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        
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

        user = Admin.objects.filter(pk=user_id).first()
        if not user:
            return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return user, None

    def get(self, request):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        
        try:
            subcategories = Subcategory.objects.get(pk=pk)
            serializer = SubcategorySerializer(subcategories, many=False)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, pk):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        try :
            subcategory = Subcategory.objects.get(pk=pk)
            Subcategory.delete()
            return Response({"status":"success","messege":"Subcatecory delete successfuly completed"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#######################################  PRODUCT MANAGEMENT ########################################

class ProductAdd(APIView):
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

            user = Admin.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return user, None


    def post(self, request):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product successfully created"}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ProductView(APIView):

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

            user = Admin.objects.filter(pk=user_id).first()
            if not user:
                return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return user, None

    def get(self, request):

        user, error_response = self.authenticate(request)
        if error_response:
            return error_response
        try :
            products = Product.objects.all()
            serializer = ProductSerializer(products,many=True)
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

            user = Admin.objects.filter(pk=user_id).first()
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
    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if not token:
            return None, Response({"status": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('id')
            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            user = Admin.objects.filter(pk=user_id).first()
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

    def delete(self, request, pk):
        user, error_response = self.authenticate(request)
        if error_response:
            return error_response

        try:
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



