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


# INCOMPLETO
class OccupancyCreateView(CreateView):
    model = Occupancy
    fields = '__all__'

    # def get_form(self,form_class=None):
    #     form = super().get_form(form_class)
        
    #     form.fields['date_start'].widget = forms.DateTimeField(attrs={'type':'datetime-local'})
    def form_valid(self,form):
        room  = form.cleaned_data["room"]
        date_start = form.cleaned_data["date_start"]
        date_end = form.cleaned_data["date_end"]
        room = get_object_or_404(Room,id="room_id")
        if Occupancy.objects.filter(
            room = room
        ).filter(
            Q(date_start_in__lt=date_start)
            &
            Q(date_end_in__gt = date_end)
        ).exists():
            form.add_error(None,"Já existe uma ocupação nesse intervalo de datas!")
            return self.form_invalid(form)
        return super().form_valid(form)

# OBJETIVO : MOSTRAR OS HORARIOS OCUPADOS REFERENTES AQUELA SALA ESPECIFICA
def occupancy_view(request,idRoom):
    allOcuppancys = Occupancy.objects.filter(room = idRoom)
    context = {
        'Occupancys':allOcuppancys
    }
    return render(request,"app/occupancy_list.html",context)