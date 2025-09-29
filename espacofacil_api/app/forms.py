from django import forms
from django.forms import BaseInlineFormSet, ValidationError, inlineformset_factory
from .models import Equipment, Occupancy, RoomEquipment, Room, RoomTimeSlot, User

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'password', 'phone', 'email']
        labels = {
            'name': 'Nome',
            'password': 'Senha',
            'phone': 'Telefone',
            'email': 'Email',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control password-field'}),
            'phone': forms.TextInput(attrs={'class': 'form-control phone-mask'}),
            'email': forms.EmailInput(attrs={'class': 'form-control email-mask'}),
        }



class OccupancyForm(forms.ModelForm):
    class Meta:
        model = Occupancy
        exclude = ["room"]
        labels = {
            'day': 'Data',
            'time_start': 'Início',
            'time_end': 'Término',
            'occupant': 'Ocupante',
            'status': 'Ativo',
        }
        widgets = {
            'day': forms.TextInput(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'type': 'time'}),
            'occupant': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["nameRoom","headCount","roomManager"]

        labels = {
            'nameRoom': 'Nome do Espaço',
            'headCount': 'Capacidade Máxima',
            'roomManager': 'Responsável pelo Espaço',
        }

        widgets = {
            'nameRoom': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'   }),
            'headCount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, '');'}),
            'roomManager': forms.Select(attrs={'class': 'form-control form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roomManager"].queryset = User.objects.all()
        self.fields["roomManager"].label_from_instance = lambda obj: obj.name

class RoomEquipmentForm(forms.ModelForm):
    class Meta:
        model = RoomEquipment
        fields = ["equipment", "amount"]

        labels = {
            'equipment': 'Equipamento',
            'amount': 'Quantidade'
        }

        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, '');'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].label_from_instance = lambda obj: obj.nameEquipment

        if self.fields.get('DELETE'):
            self.fields['DELETE'].label = 'Equipamento Removido'
    
    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get("equipment")
        amount = cleaned_data.get("amount")

        if equipment and not amount:
            self.add_error('amount', 'Por favor, insira a quantidade para o equipamento selecionado.')
        if amount and not equipment:
            self.add_error('equipment', 'Por favor, selecione um equipamento para a quantidade inserida.')


        return cleaned_data
      

RoomEquipmentFormSet = inlineformset_factory( Room, RoomEquipment,
                                             form=RoomEquipmentForm,
                                             extra=1, can_delete=True)


class CustomTimeInput(forms.TimeInput):
    input_type = 'time'
class RoomTimeSlotForm(forms.ModelForm):
    class Meta:
        model = RoomTimeSlot
        fields = ["time_start","time_end","interval"]
        labels = {
            'time_start':'Tempo Inicial',
            'time_end':'Tempo Final',
            'interval':'Intervalo'
        }
        widgets = {
            'time_start':CustomTimeInput(
                attrs={
                    'class':'',
                    'required':'true'
                },
                format='%H:%M',
              
            ),
            'time_end':CustomTimeInput(
                attrs={
                    'class':'',
                    'required':'true'
                }, 
                format='%H:%M',
                
            ),
            'interval': forms.Select(
        choices=[
            (60, 'De 1h em 1h'),
            (120, 'De 2h em 2h'),
            (180, 'De 3h em 3h')
        ],
        attrs={'class': 'form-control'}
)
        }

    def clean(self):
        cleaned_data = super().clean()
        time_start = cleaned_data.get("time_start")
        time_end = cleaned_data.get("time_end")
        interval = cleaned_data.get("interval")

        if time_start and not time_end:
            self.add_error('time_end', "Por favor, insira o tempo final")
        
        if time_end and not time_start:
            self.add_error('time_start', "Por favor, insira o tempo inicial")

        if time_start and time_end and not interval:
            self.add_error('interval', "Por favor, insira o intervalo")

        if time_start and time_end and time_start > time_end:
            self.add_error("time_start", "O horário inicial não pode ser maior que o final")

        return cleaned_data

    
class RoomTimeslotFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        print('Estou sendo chamado????')
        intervals = []

        for form in self.forms:
            print(self.forms,'ooooooo')
            if form.cleaned_data.get("DELETE", False):
                continue

            time_start = form.cleaned_data.get("time_start")
            time_end = form.cleaned_data.get("time_end")

            if not time_start or not time_end:
                continue

            # Checa sobreposição com todos os intervalos já validados
            for start, end in intervals:
                if (time_start < end) and (time_end > start):
                    form.add_error(
                        None,  # None marca o erro no form inteiro
                        f"O intervalo {time_start.strftime('%H:%M')}–{time_end.strftime('%H:%M')} "
                        f"conflita com {start.strftime('%H:%M')}–{end.strftime('%H:%M')}"
                    )

            # Adiciona o intervalo atual à lista para checagem dos próximos
            intervals.append((time_start, time_end))

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["nameEquipment"]
        labels = {
            'nameEquipment': 'Nome do Equipamento'
        }
        widgets = {
            'nameEquipment': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }
