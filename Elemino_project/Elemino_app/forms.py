from django import forms

from .models import Performance


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = [
            'pet_id',
            'pet_name',
            'pet_type',
            'breed',
            'age',
            'gender',
            'owner_name',
            'contact_number',
            'date_registered',
        ]
        widgets = {
            'date_registered': forms.DateInput(attrs={'type': 'date'}),
        }
