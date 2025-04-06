from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, 
                                  UpdateView, DeleteView,
                                  DetailView, View)
from .forms import RoomEquipmentForm, RoomEquipmentFormSet, RoomForm
from django.urls import reverse_lazy
from app.models import Occupancy, Room, User, Equipment, RoomEquipment
from django.db import transaction
from django.db.models import Q
from django.forms import inlineformset_factory
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from datetime import time

def home(request):
    return render(request, "app/home.html")
 

#Views da sala (room)

class RoomListView(ListView):
    model = Room


@transaction.atomic
def room_create(request):
    
    RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                             extra=1, can_delete=True)
    if request.method == "POST":
        form = RoomForm(request.POST)
        formset = RoomEquipmentFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            room = form.save()
            room_equipments = formset.save(commit=False)
       
            for deleted_equipment in formset.deleted_objects:
                deleted_equipment.delete()

            for equip in room_equipments:
                equip.room = room
                equip.save()
        
            
            return redirect("room_list")
    else:
        form = RoomForm()
        formset = RoomEquipmentFormSet()
    
    return render(request, "app/room_form.html", {"form": form, "formset":formset})

@transaction.atomic
def room_update(request, pk):
    RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                             extra=0, can_delete=True)
    room = Room.objects.get(pk=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        formset = RoomEquipmentFormSet(request.POST, instance=room)

        if form.is_valid() and formset.is_valid():
            form.save()
            room_equipments = formset.save(commit=False)
            for deleted_equipment in formset.deleted_objects:
                deleted_equipment.delete()
            
            for equip in room_equipments:
                equip.save()
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


def occupancy_view(request,idRoom):
    users = User.objects.all()
    return render(request,"app/occupancy_list.html",{'idRoom':idRoom,'users':users})


def occupancy_create(request,idRoom):
            
        if request.method == "POST":
            dados = json.loads(request.body)

            day = dados.get("day")
            time_start = dados.get("time_start")
            time_end = dados.get("time_end")

            occupant = dados.get("occupant")
            try:
               
                print(occupant)
                print(time_start)
                print('------')
                # PRECISA AJEITAR A LOGICA
                # DATAS QUE OCORREM EM HORARIOS JA MARCADOS TA RETORNANDO ERRO NO FRONTEND
                if day and time_start and time_end:
                    conflict_exists = Occupancy.objects.filter(
                    room=idRoom,
                    day=day
                    ).filter(
                        Q(time_start__lte=time_end) & Q(time_end__gte=time_start)
                    ).exists()

                    if conflict_exists:
                        return JsonResponse({"erro": "Já existe dia e horário nesse banco"}, status=400)
                    else:

                        occupancy = Occupancy.objects.create(
                            room_id = idRoom,
                            day = day,
                            time_start = time_start,
                            time_end = time_end,
                            status = False
                        )

                        if occupancy.pk:
                            print("Criado com sucesso!")
                        else:
                            print("Erro ao criar")

            except json.JSONDecodeError:
                print("entrei")
                return JsonResponse({"erro": "JSON inválido"}, status=400)
            
            if day:
                occupancys= Occupancy.objects.filter(room=idRoom,day=day)
                occupancys = [
                    {
                        'id':occupancy.id,
                        'time_start':occupancy.time_start,
                        'time_end':occupancy.time_end
                    } for occupancy in occupancys
                ]
                return JsonResponse(occupancys,safe=False)
    