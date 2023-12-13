from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogout.as_view(), name="user_logout"),
    path('tasks/', task_list, name='task-list'),
    path('tasks/create/', create_task, name='create-task'),
    path('tasks/<int:pk>/', get_task, name='get-task'),
    path('tasks/update/<int:pk>/', update_task, name='update-task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete-task'),
    path('tasks/search/<str:title_or_description>/', search_tasks, name='search-tasks'),
    path('tasks/created_by_user/get/', get_user_tasks, name='get_user_tasks'),
]
