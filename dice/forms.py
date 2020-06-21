"""
Required by django
"""
from django import forms

from .models import CharacterDice

ITEM_CHOICES = [
    'No Item', 'Mushroom (+3)', 'Golden Mushroom (+5)', 'Poison Mushroom (-2)']


class CustomPlayerFormSelect(forms.CheckboxSelectMultiple):
    option_template_name = 'myapp/radio_option_custom.html'

class CustomPlayerForm(forms.Form):
    characters = CharacterDice.objects.all().exclude(id=22).exclude(id=21)
    name = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=enumerate(characters), label="Choose character")


class GetPlayerSpaces(forms.Form):
    """
    Gets the amount of spaces to travel
    """
    spaces = forms.IntegerField(label='Select Number of Spaces', min_value=0)
    item = forms.ChoiceField(
        choices=enumerate(ITEM_CHOICES), label="Choose Item", initial='',
        widget=forms.Select(), required=True)


class SelectPlayerCharacter(forms.Form):
    """
    Allows user to select their character
    """
    characters = list(CharacterDice.objects.values_list(
        'character_name', flat=True))
    ally = characters.copy()
    ally.insert(0, 'None')

    character = forms.ChoiceField(
        choices=enumerate(characters), label="Choose Character", initial='',
        widget=forms.Select(), required=True)
    ally_one = forms.ChoiceField(
        choices=enumerate(ally), label="Choose Ally 1", initial='',
        widget=forms.Select(), required=False)
    ally_two = forms.ChoiceField(
        choices=enumerate(ally), label="Choose Ally 2", initial='',
        widget=forms.Select(), required=False)
    ally_three = forms.ChoiceField(
        choices=enumerate(ally), label="Choose Ally 3", initial='',
        widget=forms.Select(), required=False)
    ally_four = forms.ChoiceField(
        choices=enumerate(ally), label="Choose Ally 4", initial='',
        widget=forms.Select(), required=False)
    field_order = ['character', 'ally_one',
                   'ally_two', 'ally_three', 'ally_four']
