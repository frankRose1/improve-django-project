from django import forms
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]
        widgets={
            'expiration_date': SelectDateWidget(
                empty_label=('Choose Year', 'Choose Month', 'Choose Day'),
            ),
            'items': CheckboxSelectMultiple()
        }