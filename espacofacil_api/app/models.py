from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100,unique=True)

    def __str__(self):
        return f'{self.name},{self.phone},{self.email}'

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
        return f'O espaço armazena {self.equipment} equipamentos'



class Occupancy(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    occupant = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    day = models.DateField(null=False,blank=True)
    time_start = models.TimeField(null=False, blank=False)
    time_end = models.TimeField(null=False, blank=False)
    status = models.BooleanField()

    def __str__(self):
        return f'Espaco reservado na data: {self.date}'