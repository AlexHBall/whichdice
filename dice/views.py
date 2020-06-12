from django.shortcuts import render

from .models import CharacterDice


def home_view(request):
    return render(request, 'dice/home_screen.html', {})


def all_character_view(request):
    queryset = CharacterDice.objects.all()

    for query in queryset:
        print(query.return_dice())
    context = {
        "object_list": queryset
    }
    return render(request, 'dice/character_list.html', context)
