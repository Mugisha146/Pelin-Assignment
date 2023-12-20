from django.contrib import admin
from .models import Participant, Vehicle

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'reference_number', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'reference_number')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('participant', 'plate_type', 'plate_number', 'car_color', 'car_model', 'car_manufacture_name', 'car_manufacture_date')
    search_fields = ('participant__first_name', 'participant__last_name', 'plate_number', 'car_model')
