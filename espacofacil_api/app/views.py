from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django import forms

from django.urls import reverse_lazy
from app.models import Room, User, Equipment


def home(request):
    return render(request, "app/home.html")
 

#Views da sala (room)

class RoomListView(ListView):
    model = Room


class RoomCreateView(CreateView):
    model = Room
    fields = ["nameRoom", "headCount", "roomManager"]
    success_url = reverse_lazy("room_list")

class RoomUpdateView(UpdateView):
    model = Room
    fields = ["nameRoom","headCount","roomManager"]
    success_url = reverse_lazy("room_list")

class RoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy("room_list")

#views do usuario (user)

class UserListView(ListView):
    model = User

class UserCreateView(CreateView):
    model = User
    fields = ["name", "phone","email" ]
    success_url = reverse_lazy("user_list")

class UserUpdateView(UpdateView):
    model = User
    fields = ["name", "phone","email"]
    success_url = reverse_lazy("user_list")

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("user_list")

#views do equipamento

class EquipmentListView(ListView):
    model = Equipment

class EquipmentCreateView(CreateView):
    model = Equipment
    fields = ["nameEquipment"]
    success_url = reverse_lazy("equipment_list")

class EquipmentUpdateView(UpdateView):
    model = Equipment
    fields = ["nameEquipment"]
    success_url = reverse_lazy("equipment_list")

class EquipmentDeleteView(DeleteView):
    model = Equipment
    success_url = reverse_lazy("equipment_list")
