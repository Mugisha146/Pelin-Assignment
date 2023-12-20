from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
import re


def validate_birth_date(birth_date):
    # Validation rule: Date of birth should be 18+
    if (datetime.date.today() - birth_date) < datetime.timedelta(days=365 * 18):
        raise ValidationError(_('Participants must be 18 or older.'))


def validate_reference_number(reference_number):
    # Validation rule: Reference number should be between 99-999
    if not 99 <= int(reference_number) <= 999:
        raise ValidationError(_('Reference number should be between 99 and 999.'))


def validate_manufacture_date(manufacture_date):
    # Validation rule: Manufacture car before 2000 is not allowed
    if manufacture_date.year < 2000:
        raise ValidationError(_('Cars manufactured before 2000 are not allowed.'))


def validate_email(email):
    # Validation rule: Email must be from the '@stud.ur.ac.rw' domain
    if not email.endswith('@stud.ur.ac.rw'):
        raise ValidationError(_('Email must be from the "@stud.ur.ac.rw" domain.'))


def validate_plate_type(plate_type):
    # Validation rule: plate should start with GR, IT, RNP, RDF, CD, RAA up to RAH
    allowed_plate_types = ['GR', 'IT', 'RNP', 'RDF', 'CD', 'RAA', 'RAB', 'RAC', 'RAD', 'RAE', 'RAF', 'RAG', 'RAH']
    if plate_type not in allowed_plate_types:
        raise ValidationError(_('Invalid plate type. Choose one of: GR, IT, RNP, RDF, CD, RAA up to RAH.'))


def validate_phone(value):
    # Validation rule: Phone number should start with '+'
    if not value.startswith('+'):
        raise ValidationError(_('Phone number should start with "+".'))


def validate_rwandan_plate_number(value):
    # Validation rule: Plate number should match Rwandan plate patterns
    allowed_patterns = ['GR', 'IT', 'RNP', 'RDF', 'CD', 'RAA', 'RAB', 'RAC', 'RAD', 'RAE', 'RAF', 'RAG', 'RAH']

    # Extract the plate_type (first two or three characters) and plate_number
    plate_type = ''
    plate_number = ''

    if len(value) >= 2:
        # Extract the plate_type (2 or 3 characters) and plate_number
        plate_type = value[:3] if len(value) >= 3 else value[:2]
        plate_number = value[3:] if len(value) >= 3 else value[2:]

    if plate_type not in allowed_patterns:
        raise ValidationError(
            _('Plate number should start with one of the following: GR, IT, RNP, RDF, CD, RAA up to RAH.'))


class Participant(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(validators=[validate_email])
    phone = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(limit_value=6),
            validate_phone,
            RegexValidator(regex=r'^\+\d{1,15}$', message=_('Invalid phone number format.'))
        ]
    )
    birth_date = models.DateField(validators=[validate_birth_date])
    reference_number = models.CharField(max_length=3,
                                        validators=[MinLengthValidator(limit_value=3), validate_reference_number])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reference_number})"


class Vehicle(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True)
    PLATE_TYPE_CHOICES = [
        ('GR', 'Government (GR)'),
        ('IT', 'Import Temporary (IT)'),
        ('RNP', 'Rwanda National Police (RNP)'),
        ('RDF', 'Rwanda Defence Force (RDF)'),
        ('CD', 'Ambassador (CD)'),
        ('RAA', 'RAA'),
        ('RAB', 'RAB'),
        ('RAC', 'RAC'),
        ('RAD', 'RAD'),
        ('RAE', 'RAE'),
        ('RAF', 'RAF'),
        ('RAG', 'RAG'),
        ('RAH', 'RAH'),
    ]

    plate_type = models.CharField(max_length=3, choices=PLATE_TYPE_CHOICES, verbose_name='Plate Type',
                                  validators=[validate_plate_type])
    plate_number = models.CharField(max_length=10, )
    car_color = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_manufacture_name = models.CharField(max_length=50)
    car_manufacture_date = models.DateField(validators=[validate_manufacture_date])

    def __str__(self):
        return f"{self.plate_type} {self.plate_number} ({self.car_model})"
