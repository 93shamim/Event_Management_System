from django import forms
from .models import Organizer

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['name','description'] 
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }