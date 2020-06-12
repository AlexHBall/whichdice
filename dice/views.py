"""
Required by django
"""
from django.shortcuts import render

from .models import CharacterDice

def home_view(request):
    """
    Home Screen, default location
    """
    return render(request, 'dice/home_screen.html', {})

def all_character_view(request):
    """
    Views all different characters and their dice
    """
    queryset = CharacterDice.objects.all()

    for query in queryset:
        print(query)
    context = {
        "object_list": queryset
    }
    return render(request, 'dice/character_list.html', context)
