from django.urls import path
from .views import (
    signup_view, login_view, logout_view, profile_view,
    task_list_view, task_detail_view, create_task_view, apply_task_view
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('', task_list_view, name='task_list'),
    path('task/create/', create_task_view, name='create_task'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail'),
    path('task/<int:task_id>/apply/', apply_task_view, name='apply_task'),
]
