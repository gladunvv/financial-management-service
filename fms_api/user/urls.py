from django.urls import path
from user.views import (
    UserCreateView,
    UserLogInView,
    UserLogOutView,
    UserDeleteView,
)

app_name = 'user'
urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
]
