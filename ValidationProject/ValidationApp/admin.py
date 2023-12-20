from .models import Participant, Vehicle
from django.contrib import admin
from .models import YourModel
import logging



@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'reference_number', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'reference_number')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('participant', 'plate_type', 'plate_number', 'car_color', 'car_model', 'car_manufacture_name',
                    'car_manufacture_date')
    search_fields = ('participant__first_name', 'participant__last_name', 'plate_number', 'car_model')



logger = logging.getLogger('django')

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    # Your model admin configuration

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Log the action
        logger.info(f"Object {obj} {'changed' if change else 'added'} by {request.user}")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)

        # Log the action
        logger.info(f"Object {obj} deleted by {request.user}")
