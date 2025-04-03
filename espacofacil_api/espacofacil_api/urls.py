from django.contrib import admin
from django.urls import path
from app.views import home

from app.views import (
    RoomListView, room_create, room_update,RoomDeleteView,RoomDetailView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    EquipmentListView,EquipmentCreateView,EquipmentUpdateView,EquipmentDeleteView)      

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path("roomList", RoomListView.as_view(),name="room_list"),
    path("roomCreate", room_create,name="room_create"),
    path("updateRoom/<int:pk>", room_update, name="room_update"),
    path("deleteRoom/<int:pk>", RoomDeleteView.as_view(), name="room_delete"),
    path('userList', UserListView.as_view(), name="user_list"),
    path("userCreate", UserCreateView.as_view(), name="user_create"),
    path("updateUser/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    path("deleteUser/<int:pk>", UserDeleteView.as_view(), name="user_delete"),
    path("equipmentList", EquipmentListView.as_view(), name="equipment_list"),
    path("equipmentCreate", EquipmentCreateView.as_view(),name="equipment_create"),
    path("updateEquipmnet/<int:pk>",EquipmentUpdateView.as_view(),name="equipment_update"),
    path("deleteEquipmnet/<int:pk>",EquipmentDeleteView.as_view(),name="equipment_delete"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
] 