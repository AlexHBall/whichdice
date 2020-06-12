"""
Required by django
"""
from django.shortcuts import render, get_object_or_404

from .models import CharacterDice
from .forms import SelectPlayerCharacter


def home_view(request):
    """
    Home Screen, default location
    """

    def get_ally_context(form, context):
        result = []
        allies = ('ally_one',
                  'ally_two',
                  'ally_three',
                  'ally_four')
        for key in allies:
            identifier = int(form.cleaned_data.get(key))
            if identifier > 0:
                result.append(CharacterDice.objects.get(pk=identifier))
        context['allies'] = result

    character_form = SelectPlayerCharacter(request.POST or None)
    context = {'character_form': character_form}
    if character_form.is_valid():
        character_id = int(character_form.cleaned_data.get("character")) + 1
        character = CharacterDice.objects.get(pk=character_id)
        context['character'] = character
        get_ally_context(character_form, context)
        print(context)
    return render(request, 'dice/home_screen.html', context)


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


def character_view(request, idenitifer):
    """
    Views a specific character
    """
    obj = get_object_or_404(CharacterDice, id=idenitifer)
    context = {
        'object': obj
    }
    print(obj)
    return render(request, 'dice/character_detail.html', context)
