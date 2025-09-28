# app/admin.py

from django.contrib import admin
from .models import User, Equipment, Room, RoomEquipment, Occupant, Occupancy

# Registra cada um dos seus modelos para que apareçam na página de administração
admin.site.register(User)
admin.site.register(Equipment)
admin.site.register(Room)
admin.site.register(RoomEquipment)
admin.site.register(Occupant)
admin.site.register(Occupancy)