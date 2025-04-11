from django import forms
from django.forms import inlineformset_factory
from .models import RoomEquipment, Room, User

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'password', 'phone', 'email', 'user_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

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
