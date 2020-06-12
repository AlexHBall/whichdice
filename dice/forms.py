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
    ally = forms.ChoiceField(
        choices=enumerate(ally), label="Choose Ally", initial='',
        widget=forms.Select(), required=False)
    field_order = ['character', 'ally']
