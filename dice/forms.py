"""
Required by django
"""
from django import forms

from .models import CharacterDice


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