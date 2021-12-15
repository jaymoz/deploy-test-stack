from django import forms
from .models import Bookings,Parking_Space
from django.forms import ModelForm
from django.core.validators import RegexValidator

class Parking_SpaceForm(ModelForm):
	class Meta:
		model = Parking_Space
		fields = ['park_name','no_of_spaces']
		widgets = {
			'park_name':forms.TextInput(attrs={
				'class':'input-text input-text--primary-style',
				'type':'text',
				'id':'address-fname',
				'required':True,
				'placeholder':'parking space(name)'
			}),
			'no_of_spaces':forms.TextInput(attrs={
			'class':'input-text input-text--primary-style',
			'id':'address-lname',
			'type':'text',
			'required':True,
			'placeholder':'number of spaces'
			}),
		}


class BookingForm(ModelForm):
	class Meta:
		model = Bookings
		fields = ['manufacturer','car_model','color','plate_number','phone','start_period','end_period']
		widgets = {
			'manufacturer':forms.TextInput(attrs={
				'class':'input-text input-text--primary-style',
				'type':'text',
				'id':'address-fname',
				'required':True,
				'placeholder':'manufacturer'
			}),
			'car_model':forms.TextInput(attrs={
			'class':'input-text input-text--primary-style',
			'id':'address-lname',
			'type':'text',
			'required':True,
			'placeholder':'car model'
			}),
			'color':forms.TextInput(attrs={
			'class':'input-text input-text--primary-style',
			'id':'address-street',
			'type':'text',
			'required':True,
			'placeholder':'color'
			}),
			'phone':forms.TextInput(attrs={
			'class':'input-text input-text--primary-style',
			'id':'address-phone',
			'type':'tel',
			'required':True,
			'placeholder':'8 960 xxx-xx-xx'
			}),
			'plate_number':forms.TextInput(attrs={
			'class':'input-text input-text--primary-style',
			'id':'address-phone',
			'type':'tel',
			'required':True,
			'placeholder':'plate_number'
			}),
			'start_period':forms.DateTimeInput(attrs={
            'class':"input-text input-text--border-radius input-text--style-1",
            'type':'datetime-local',
			'id':'date1',
			'required':True,
			'placeholder':'start period'
			}),
			'end_period':forms.DateTimeInput(attrs={
			'class':"input-text input-text--border-radius input-text--style-1",
			'id':'date2',
            'type':'datetime-local',
			'required':True,
			'placeholder':'end period'
			}),
		}
