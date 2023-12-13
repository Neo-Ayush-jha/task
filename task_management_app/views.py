from .models import *
from .serializers import *
from datetime import timedelta
from django.db.models import Q
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.pagination import PageNumberPagination


# ------------------------------------ User Registration View---------------------------------------------------------->
class UserRegistration(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------ UserLogout---------------------------------------------------------------------->
class UserLogout(APIView):
    def post(self, request):
        try:
            # Logic to update the token in the User model
            user = (
                request.user
            )  # Assuming you're using request.user for the current user
            user.remember_token = (
                None  # Set the token to None or some other value to invalidate it
            )
            user.save()
            return Response(
                {"message": "You have been logged out successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred while logging out."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ------------------------------------ User Login and JWT Token View  UserLoginView------------------------------------>
class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            access_token = AccessToken.for_user(user)
            access = str(access_token)  # Generate a random string
            token_expiration = timezone.now() + timedelta(
                minutes=2
            )  # Set the expiration time to 2 minutes
            user.remember_token = access
            user.token_expiration = token_expiration
            user.save()  # Save the user object with the new values

            return Response(
                {
                    "access": access,
                    "remember_token": user.remember_token,
                    "token_expiration": token_expiration,
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# ------------------------------------------------Task--------------------------------------------------------------------->


# ------------------------------------------------Task Listing--------------------------------------------------------------------->
@api_view(["GET"])
@permission_classes([AllowAny])
def task_list(request):
    pagination_class = PageNumberPagination()
    tasks = Task.objects.all()
    paginated_tasks = pagination_class.paginate_queryset(tasks, request)

    serializer = TaskSerializer(paginated_tasks, many=True)
    return pagination_class.get_paginated_response(serializer.data)


# ------------------------------------------------Task Post/Create--------------------------------------------------------------------->
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == "POST":
        request.data["owner"] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------Task Single List--------------------------------------------------------------------->
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if request.user != task.owner:
            return Response(
                {"message": "You do not have permission to view this task."},
                status=status.HTTP_403_FORBIDDEN,
            )
        pagination_class = PageNumberPagination()
        paginated_task = pagination_class.paginate_queryset([task], request)

        serializer = TaskSerializer(paginated_task, many=True)
        return pagination_class.get_paginated_response(serializer.data)
    except Task.DoesNotExist:
        return Response(
            {"message": "No data found with this ID."}, status=status.HTTP_404_NOT_FOUND
        )

# ------------------------------------------------Task Created By User List--------------------------------------------------------------------->
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_tasks(request):
    try:
        user_tasks = Task.objects.filter(owner=request.user)
        pagination_class = PageNumberPagination()
        paginated_user_tasks = pagination_class.paginate_queryset(user_tasks, request)
        serializer = TaskSerializer(paginated_user_tasks, many=True)
        return pagination_class.get_paginated_response(serializer.data)
    
    except Exception as e:
        return Response(
            {"message": f"Error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
# ------------------------------------------------Task Update--------------------------------------------------------------------->
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if request.user != task.owner:
            return Response(
                {"message": "You do not have permission to update this task."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["owner"] = request.user.id
        serializer = TaskSerializer(task, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response(
            {"message": "No data found with this ID."}, status=status.HTTP_404_NOT_FOUND
        )


# ------------------------------------------------Task Delete--------------------------------------------------------------------->
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(
            {"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
    except Task.DoesNotExist:
        return Response(
            {"message": "No data found with this ID."}, status=status.HTTP_404_NOT_FOUND
        )


# ------------------------------------------------Task Search--------------------------------------------------------------------->
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_tasks(request, title_or_description):
    try:
        tasks = Task.objects.filter(
            Q(title__icontains=title_or_description)
            | Q(description__icontains=title_or_description),
            owner=request.user,
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
