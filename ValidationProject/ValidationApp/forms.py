from django import forms
from .models import Participant, Vehicle

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'car_manufacture_date': forms.DateInput(attrs={'type': 'date'}),
        }
