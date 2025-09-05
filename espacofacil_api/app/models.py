from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 🔒 Usa hash seguro
        user.save(using=self._db)
        return user
    
    # user_type = models.ForeignKey('UserType', on_delete=models.CASCADE, null=True, blank=True)


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class UserType(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Equipment(models.Model):
    nameEquipment = models.CharField(max_length=200)
    
    def __str__(self):
        return {self.nameEquipment}

class Room(models.Model):
    roomManager = models.ForeignKey(User,on_delete=models.CASCADE)
    # RoomMetting = models.ForeignKey(RoomMetting,null=True)
    nameRoom = models.CharField(max_length=100, null=False, blank=False)
    headCount = models.IntegerField(null=False, blank=False)
    

    def __str__(self):
        return f'{self.nameRoom} pode conter {self.headCount} indivíduos'

class RoomEquipment(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.equipment.nameEquipment



class Occupancy(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    nameOccupant = models.CharField(max_length=60,null=True)
    occupant = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    day = models.DateField(null=False,blank=True)
    time_start = models.TimeField(null=False, blank=False)
    time_end = models.TimeField(null=False, blank=False)
    status = models.BooleanField()

    def __str__(self):
        return f'Espaco reservado na data: {self.day}'
