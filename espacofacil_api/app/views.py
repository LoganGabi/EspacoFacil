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
from django.contrib import messages
import json
from datetime import time, datetime
from app.models import Occupancy, Occupant, Room, RoomTimeSlot, User, Equipment, RoomEquipment
from .forms import EquipmentForm, OccupancyForm, RoomEquipmentForm, RoomForm, RoomTimeSlotForm, RoomTimeslotFormSet, UserForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime


# signals.py


@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ou o nome da sua URL de destino
            else:
                form.add_error(None, 'Email ou senha inválidos.')

    return render(request, 'app/login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         print("DEBUG - Email:", email)
#         print("DEBUG - Senha:", password)

#         try:
#             user_obj = User.objects.get(email=email)
#             print("DEBUG - Usuário encontrado:", user_obj)
#             user = authenticate(request, username=user_obj.username, password=password)
#         except User.DoesNotExist:
#             print("DEBUG - Usuário com esse email não existe.")
#             user = None

#         if user is not None:
#             print("DEBUG - Autenticado com sucesso.")
#             login(request, user)
#             return redirect('/home/')  # Certifique-se que essa URL existe
#         else:
#             print("DEBUG - Falha na autenticação.")
#             return render(request, 'app/login.html', {'form': {'errors': True}})
    
#     print("DEBUG - GET recebido")
#     return render(request, 'app/login.html')

#Views da sala (room)

class RoomListView(LoginRequiredMixin, ListView):
    model = Room


@transaction.atomic
@login_required
def room_create(request):
    
    RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                            
                                             extra=1, can_delete=True
                                            )
    
    RoomTimeSlotFormSet = inlineformset_factory( Room,RoomTimeSlot,
                                            form=RoomTimeSlotForm,
                                            formset=RoomTimeslotFormSet,
                                            extra=1,can_delete=True)

    if request.method == "POST":
        form = RoomForm(request.POST)
        formset = RoomEquipmentFormSet(request.POST)
        timeSlotFormset = RoomTimeSlotFormSet(request.POST)

        if form.is_valid() and formset.is_valid() and timeSlotFormset.is_valid():
            room = form.save()
            room_equipments = formset.save(commit=False)
            room_time_slots = timeSlotFormset.save(commit=False)

            for deleted_equipment in formset.deleted_objects:
                deleted_equipment.delete()

            for deleted_time_slot in timeSlotFormset.deleted_forms:
                deleted_time_slot.delete()

            for equip in room_equipments:
                equip.room = room
                equip.save()
            
            for time_slot in room_time_slots:
                time_slot.room = room
                time_slot.save()
                  
            return redirect("room_list")
    else:
        form = RoomForm()
        formset = RoomEquipmentFormSet()
        timeSlotFormset = RoomTimeSlotFormSet()

    context = {
            'form':form,
            'formset':formset,
            'timeSlotFormset':timeSlotFormset
        }
    return render(request, "app/room_form.html",context)

@transaction.atomic
@login_required
def room_update(request, pk):
    RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                             extra=0, can_delete=True)
    
    RoomTimeSlotFormSet = inlineformset_factory( Room,RoomTimeSlot,
                                            form=RoomTimeSlotForm,
                                            extra=0,can_delete=True)

    room = Room.objects.get(pk=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        formset = RoomEquipmentFormSet(request.POST, instance=room)
        timeSlotFormset = RoomTimeSlotFormSet(request.POST,instance=room)

        if form.is_valid() and formset.is_valid() and timeSlotFormset.is_valid():
            form.save()
            room_equipments = formset.save(commit=False)
            room_time_slots = timeSlotFormset.save(commit=False)

            for deleted_time_slot in timeSlotFormset.deleted_forms:
                deleted_time_slot.delete()
            
            for deleted_equipment in formset.deleted_objects:
                deleted_equipment.delete()
            
            for equip in room_equipments:
                equip.save()

            for time_slot in room_time_slots:
                time_slot.room = room
                time_slot.save()

            return redirect("room_list")
    
    else:
        form = RoomForm(instance=room)
        formset = RoomEquipmentFormSet(instance=room)
        timeSlotFormset = RoomTimeSlotFormSet(instance=room)
    
    context = {
        'form':form,
        'formset':formset,
        'timeSlotFormset':timeSlotFormset
    }
    
    return render(request, "app/room_form.html",context)


def auto_create_schedules(request):
    """
    Cria ocupações automaticamente para os próximos 14 dias,
    usando os RoomTimeSlot definidos.
    """
    today = date.today()
    rooms = Room.objects.all()

    for room in rooms:
        intervals = RoomTimeSlot.objects.filter(room=room)

        for i in range(14):
            current_date = today + timedelta(days=i)

            for interval in intervals:
                start_time = datetime.combine(current_date, interval.time_start)
                end_time = datetime.combine(current_date, interval.time_end)
                delta = timedelta(minutes=interval.interval)

                current_start = start_time
                while current_start < end_time:
                    current_end = min(current_start + delta, end_time)

                    # Evita duplicação
                    if not Occupancy.objects.filter(
                        room=room,
                        day=current_date,
                        time_start=current_start.time(),
                        time_end=current_end.time()
                    ).exists():
                        Occupancy.objects.create(
                            room=room,
                            day=current_date,
                            time_start=current_start.time(),
                            time_end=current_end.time(),
                            status=True
                        )

                    current_start += delta

            print(f"Horários criados para {room} no dia {current_date}")
class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy("room_list")

# views da sala com os equipamentos

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["equipment"] = RoomEquipment.objects.filter(room=self.object)
        return context
        
#views do usuario (user)

class UserListView(LoginRequiredMixin, ListView):
    model = User

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        # hashing da senha
        form.instance.password = make_password(form.cleaned_data['password'])
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user_list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("user_list")

#views do equipamento

class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_list")

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ["nameEquipment"]
    success_url = reverse_lazy("equipment_list")

class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    success_url = reverse_lazy("equipment_list")

@login_required
def occupancy_view(request,idRoom):
    users = User.objects.filter(room=idRoom)
    occupants = Occupant.objects.all()
    nameRoom = Room.objects.get(pk=idRoom).nameRoom
    
    auto_create_schedules(request)
    return render(request,"app/occupancy_list.html",{
        'idRoom':idRoom,
        'nameRoom':nameRoom,
        'users':users,
        'occupants':occupants
        }
    )
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Occupancy, Occupant
import json

@login_required
def occupancy_create(request, idRoom):
    if request.method != "POST":
        return JsonResponse({"erro": "Método inválido"}, status=405)

    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)

    day_str = dados.get("day")
    time_start_str = dados.get("time_start")
    time_end_str = dados.get("time_end")
    occupant_id = dados.get("occupant")

    if not day_str:
        return JsonResponse({"erro": "O campo 'day' é obrigatório"}, status=400)

    # Converte day para date
    try:
        day = datetime.strptime(day_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"erro": "Formato de 'day' inválido, use YYYY-MM-DD"}, status=400)

    # Se time_start e time_end estiverem presentes, cria novo Occupancy
    if time_start_str and time_end_str:
        try:
            time_start = datetime.strptime(time_start_str, "%H:%M").time()
            time_end = datetime.strptime(time_end_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({"erro": "Formato de horário inválido, use HH:MM"}, status=400)

        # Busca occupant se informado
        occupant_obj = None
        if occupant_id:
            try:
                occupant_obj = Occupant.objects.get(pk=occupant_id)
            except Occupant.DoesNotExist:
                return JsonResponse({"erro": "O occupant informado não existe"}, status=400)

        # Verifica conflito de horário
        conflict_exists = Occupancy.objects.filter(
            room=idRoom,
            day=day
        ).filter(
            Q(time_start__lt=time_end) & Q(time_end__gt=time_start)
        ).exists()

        if conflict_exists:
            return JsonResponse({"erro": "Já existe um horário nesse dia"}, status=400)

        # Cria o Occupancy
        occupancy = Occupancy.objects.create(
            room_id=idRoom,
            occupant=occupant_obj,
            day=day,
            time_start=time_start,
            time_end=time_end,
            status=True
        )
        print(f"Occupancy criado: {occupancy.id}")

    # Retorna todos os Occupancy do dia
    occupancys_qs = Occupancy.objects.filter(room=idRoom, day=day).order_by("time_start")
    occupancys = [
        {
            "id": o.id,
            "occupant": o.occupant.firstName if o.occupant else None,
            "time_start": o.time_start.strftime("%H:%M") if o.time_start else None,
            "time_end": o.time_end.strftime("%H:%M") if o.time_end else None,
        }
        for o in occupancys_qs
    ]

    print(f"Occupancies retornados para room {idRoom} no dia {day}: {len(occupancys)}")
    return JsonResponse(occupancys, safe=False)

def occupancy_update(request,idOccupancy):
    occupancy = get_object_or_404(Occupancy, pk=idOccupancy)

    if request.method == "POST":
        form = OccupancyForm(request.POST, instance=occupancy)
        if form.is_valid():
            form.save()
            return redirect("occupancy_list", idRoom=occupancy.room.id)
    else:
        form = OccupancyForm(instance=occupancy)

    return render(request, "app/occupancy_form.html", {"occupancyForm": form})



def occupancy_delete(request,idOccupancy):
    if request.method == "POST":
        occupancy = get_object_or_404(Occupancy,pk = idOccupancy)
        id_occupancy = occupancy.room.id
        occupancy.delete()
        return occupancy_create(request,id_occupancy)
# View da pesquisa das salas.

class RoomSearchView(LoginRequiredMixin, View):
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