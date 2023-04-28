from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
import json
from .query import airport_name, roomtype_dict, mealtype_dict

class DateInput(forms.DateInput):
    input_type = 'date'
    format = "%Y-%m-%d"

class BasicForm(forms.Form):
    airport = forms.ChoiceField(required=True, choices=list(enumerate(airport_name.values())))
    departure_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    adults = forms.IntegerField(min_value=1, max_value=30)
    children = forms.IntegerField(min_value=0, max_value=30)
    price_min = forms.IntegerField(min_value=0, max_value=10000)
    price_max = forms.IntegerField(min_value=0, max_value=10000)
    duration = forms.IntegerField(min_value=1, max_value=60)

class DetailForm(forms.Form):
    room_type = forms.ChoiceField(required=False, choices=list(enumerate([x.title() for x in (["No preference"]+list(roomtype_dict.values()))])))
    meal_type = forms.ChoiceField(required=False, choices=list(enumerate([x.title() for x in (["No preference"]+list(mealtype_dict.values()))])))
    ocean_view = forms.ChoiceField(required=False, choices=list(enumerate(["No", "Yes"])))
