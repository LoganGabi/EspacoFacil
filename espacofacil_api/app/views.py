from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, 
                                  UpdateView, DeleteView,
                                  DetailView)
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django import forms
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

import json
from datetime import time, datetime

from app.models import Occupancy, Room, User, Equipment, RoomEquipment

from .forms import RoomEquipmentForm, RoomForm
from .forms import UserForm

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return render(request, "app/login.html")

        user_auth = authenticate(request, email=email, password=senha)

        if user_auth is not None:
            login(request, user_auth)
            return redirect("/home")
        else:
            messages.error(request, "Senha incorreta.")
    
    return render(request, "app/login.html")

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
    form_class = UserForm
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        # hashing da senha
        form.instance.password = make_password(form.cleaned_data['password'])
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
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
    

# View da pesquisa das salas.

class RoomSearchView(View):
    def get(self, request):
        # Formulario de busca
        name_query = request.GET.get("name","").strip()
        head_count_query = request.GET.get("headCount")
        equipment_query = request.GET.get("equipments","").strip()
        date_query = request.GET.get("date")
        time_start_query = request.GET.get("time_start")
        time_end_query = request.GET.get("time_end")
    
        rooms = Room.objects.all()

        # Filtros

        if name_query:
            name_terms = [term.strip() for term in name_query.split(",") if term.strip()]
            q_obj = Q()
            for name in name_terms:
                q_obj |= Q(nameRoom__icontains=name)
            rooms = rooms.filter(q_obj)

        if head_count_query:
            try:
                rooms = rooms.filter(headCount__gte=int(head_count_query))
            except ValueError:
                pass
        
        if equipment_query:
            equipment_names = [e.strip() for e in equipment_query.split(",") if e.strip()]
            for name in equipment_names:
                rooms = rooms.filter(
                    roomequipment__equipment__nameEquipment__icontains=name
                ).distinct()
        
        if date_query and time_start_query and time_end_query:
            try:
                date_obj = datetime.strptime(date_query, "%Y-%m-%d").date()
                time_end_obj = datetime.strptime(time_end_query, "%H:%M").time()
                time_start_obj = datetime.strptime(time_start_query, '%H:%M').time()
                occupied_rooms = Occupancy.objects.filter(
                    day=date_obj,
                    status = True
                ).filter(
                    Q(time_start__lt=time_end_obj) & Q(time_end__gt=time_start_obj)
                ).values_list("room_id",flat=True)

                rooms = rooms.exclude(id__in=occupied_rooms)
            except ValueError:
                pass
        
        rooms = rooms.order_by("headCount")

        return render(request, "app/home.html", {"rooms":rooms})