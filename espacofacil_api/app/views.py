from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, 
                                  UpdateView, DeleteView,
                                  DetailView, View)
from .forms import RoomEquipmentFormSet, RoomForm
from django.urls import reverse_lazy
from app.models import Room, User, Equipment, RoomEquipment


def home(request):
    return render(request, "app/home.html")
 

#Views da sala (room)

class RoomListView(ListView):
    model = Room


def room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        formset = RoomEquipmentFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            room = form.save()
            room_equipments = formset.save(commit=False)

            for equip in room_equipments:
                equip.room = room
                equip.save()
            
            return redirect("room_list")
    else:
        form = RoomForm()
        formset = RoomEquipmentFormSet()
    
    return render(request, "app/room_form.html", {"form": form, "formset":formset})

def room_update(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        formset = RoomEquipmentFormSet(request.POST, instance=room)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("room_list")
    
    else:
        form = RoomForm(instance=room)
        formset = RoomEquipmentFormSet(instance=room)
    
    return render(request, "app/room_form.html", {"form":form,"formset":formset})

class RoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy("room_list")

# views da sala com os equipamentos

class RoomDetailView(DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["equipment"] = RoomEquipment.objects.filter(room=self.object)
        return context
        
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
