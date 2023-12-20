# views.py
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory, formset_factory
from django.core.exceptions import ValidationError
from .forms import ParticipantForm, VehicleForm
from .models import Participant, Vehicle
from django.shortcuts import render


def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participant_list.html', {'participants': participants})


def participant_detail(request, pk):
    participant = Participant.objects.get(pk=pk)
    return render(request, 'participant_detail.html', {'participant': participant})


def vehicle_create(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.participant = participant
            vehicle.save()
            return redirect('participant_detail', pk=participant_id)
    else:
        form = VehicleForm()

    return render(request, 'vehicle_create.html', {'form': form, 'participant': participant})


def participant_delete(request, pk):
    participant = Participant.objects.get(pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})


def participant_create(request):
    VehicleFormSet = formset_factory(VehicleForm, extra=1, can_delete=True)

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, prefix='participant')
        vehicle_formset = VehicleFormSet(request.POST, prefix='vehicle')

        if participant_form.is_valid() and vehicle_formset.is_valid():
            participant = participant_form.save()

            for vehicle_form in vehicle_formset:
                if vehicle_form.is_valid():
                    vehicle = vehicle_form.save(commit=False)
                    vehicle.participant = participant
                    vehicle.save()

            try:
                participant.full_clean()
            except ValidationError as e:
                participant_form.add_error(None, e.message_dict)
                return render(request, 'participant_form.html',
                              {'participant_form': participant_form, 'vehicle_formset': vehicle_formset,
                               'action': 'Create'})

            return redirect('participant_list')
    else:
        participant_form = ParticipantForm(prefix='participant')
        vehicle_formset = VehicleFormSet(prefix='vehicle')

    return render(request, 'participant_form.html',
                  {'participant_form': participant_form, 'vehicle_formset': vehicle_formset, 'action': 'Create'})


def participant_edit(request, pk):
    participant = Participant.objects.get(pk=pk)
    vehicle_set = participant.vehicle_set.all()

    # Use inlineformset_factory for handling related forms
    VehicleFormSet = inlineformset_factory(Participant, Vehicle, form=VehicleForm, extra=0, can_delete=True)

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, instance=participant, prefix='participant')
        vehicle_formset = VehicleFormSet(request.POST, instance=participant, prefix='vehicle')

        if participant_form.is_valid() and vehicle_formset.is_valid():
            participant = participant_form.save()

            # Delete vehicles marked for deletion
            for form in vehicle_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            for vehicle_form in vehicle_formset:
                if vehicle_form.is_valid():
                    # If the form is marked for deletion, do not save it
                    if vehicle_form.cleaned_data.get('DELETE'):
                        continue

                    vehicle = vehicle_form.save(commit=False)
                    vehicle.participant = participant
                    vehicle.save()

            try:
                participant.full_clean()
            except ValidationError as e:
                participant_form.add_error(None, e.message_dict)
                return render(request, 'participant_form.html',
                              {'participant_form': participant_form, 'vehicle_formset': vehicle_formset,
                               'action': 'Edit'})

            return redirect('participant_list')
    else:
        participant_form = ParticipantForm(instance=participant, prefix='participant')
        vehicle_formset = VehicleFormSet(instance=participant, prefix='vehicle', queryset=vehicle_set)

    return render(request, 'participant_form.html',
                  {'participant_form': participant_form, 'vehicle_formset': vehicle_formset, 'action': 'Edit'})
