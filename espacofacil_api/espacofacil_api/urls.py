from django.contrib import admin
from django.urls import path
from app.views import home

from app.views import RoomListView, RoomCreateView,RoomUpdateView,RoomDeleteView, UserListView, UserCreateView, UserUpdateView, UserDeleteView          

urlpatterns = [
    path('admin/', admin.site.urls),
    path("roomList", RoomListView.as_view(),name="room_list"),
    path("roomCreate", RoomCreateView.as_view(),name="room_create"),
    path("updateRoom/<int:pk>", RoomUpdateView.as_view(), name="room_update"),
    path("deleteRoom/<int:pk>", RoomDeleteView.as_view(),name="room_delete"),
    path('userList', UserListView.as_view(), name="user_list"),
    path("userCreate", UserCreateView.as_view(), name="user_create"),
    path("updateUser/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    path("deleteUser/<int:pk>", UserDeleteView.as_view(), name="user_delete"),
    path("", home, name="home")
]
