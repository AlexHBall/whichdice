from django.shortcuts import render

from .models import CharacterDice

def home_view(request):
    return render(request, 'dice/home_screen.html', {})

# Create your views here.
