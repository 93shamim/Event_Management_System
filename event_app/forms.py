from django import forms
from .models import EventApp
from category.models import Category
from organizer.models import Organizer


class EventAppForm(forms.ModelForm):
    class Meta:
        model = EventApp
        fields = ['name', 'category', 'description', 'start_date_time', 'end_date_time', 'capacity', 'location', 'organizer']
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Select Category")
        organizer = forms.ModelChoiceField(queryset=Organizer.objects.all(), label="Select Organizer")


    def __init__(self, *args, **kwargs):
        super(EventAppForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['capacity'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['organizer'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        start_date_time = cleaned_data.get('start_date_time')
        end_date_time = cleaned_data.get('end_date_time')
        if start_date_time and end_date_time and start_date_time > end_date_time:
            self.add_error('start_date', 'Start date must be before end date')
            self.add_error('end_date', 'End date must be after start date') 

        return cleaned_data
    


