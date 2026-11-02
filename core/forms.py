from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Appointment, CustomerProfile, Service

User = get_user_model()


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        full_name = self.cleaned_data['full_name'].strip()
        name_parts = full_name.split(maxsplit=1)
        user.first_name = name_parts[0] if name_parts else ''
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        if commit:
            user.save()

        profile, _ = CustomerProfile.objects.get_or_create(
            user=user,
            defaults={'phone': self.cleaned_data['phone_number']},
        )
        profile.phone = self.cleaned_data['phone_number']
        profile.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'appointment_date', 'appointment_time', 'phone_number', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional notes for your stylist or therapist.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(available=True).order_by('category', 'name')

    def clean_appointment_date(self):
        selected_date = self.cleaned_data['appointment_date']
        if selected_date < timezone.localdate():
            raise forms.ValidationError('Please select a date in the future.')
        return selected_date

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number'].strip()
        if len(phone) < 7:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone
