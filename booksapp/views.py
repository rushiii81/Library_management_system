from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status, permissions
from .models import AdminUser, Book
from .serializers import AdminUserSerializer, BookSerializer
from django.http import HttpResponse

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password, make_password
import requests



### Home page with login and view books option #######
def home_redirect(request):
    return render(request, 'home.html')


### view to allow only admin to edit , add and delete books ########
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow only admins to modify books.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin




## view to fetch data from api ########
def student_view(request):
    api_url = request.build_absolute_uri('/books/')  # Fetch data from API
    response = requests.get(api_url)

    if response.status_code == 200:
        books = response.json()
    else:
        books = []  # Empty list if API fails

    return render(request, 'books_list.html', {'books': books})



## view for admin to signup if data is valid ########

@api_view(['POST'])
def admin_signup(request):
    serializer = AdminUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Admin registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




## view for admin to login if data is valid ########

@api_view(['POST'])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    admin = get_object_or_404(AdminUser, email=email)

    if admin.check_password(password) and admin.is_admin:  # Only admins can log in
        refresh = RefreshToken.for_user(admin)
        return Response({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials or unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)




def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = get_object_or_404(AdminUser, email=email)

        if check_password(password, admin.password):
            refresh = RefreshToken.for_user(admin)
            request.session['access_token'] = str(refresh.access_token)  # Store token in session
            return redirect('list_books')  # Redirect to book list page

    return render(request, 'admin_login.html')



#view to add book ######

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book added successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#view to show all books #####

def list_books(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})


#view to update the book #####

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##view to delete the book #####

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




