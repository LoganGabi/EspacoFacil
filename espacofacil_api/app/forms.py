from django import forms
from django.forms import inlineformset_factory
from .models import RoomEquipment, Room, User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["nameRoom","headCount","roomManager"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roomManager"].queryset = User.objects.all()
        self.fields["roomManager"].label_from_instance = lambda obj: obj.name

class RoomEquipmentForm(forms.ModelForm):
    class Meta:
        model = RoomEquipment
        fields = ["equipment", "amount"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].label_from_instance = lambda obj: obj.nameEquipment
      

RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                             extra=1, can_delete=True)