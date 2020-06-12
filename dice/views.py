"""
Required by django
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers

from .models import CharacterDice
from .forms import SelectPlayerCharacter

ALLIES_KEY = 'allies'
CHARACTER_KEY = 'character'


def home_view(request):
    """
    Home Screen, default location
    """
    request.session.flush()

    def get_ally_context(form):
        result = []
        allies = ('ally_one',
                  'ally_two',
                  'ally_three',
                  'ally_four')
        for key in allies:
            identifier = int(form.cleaned_data.get(key))
            if identifier > 0:
                ally = CharacterDice.objects.get(pk=identifier)
                result.append(ally)
        request.session[ALLIES_KEY] = serializers.serialize(
                    'json', result)

    def get_character(form):
        character_id = int(form.cleaned_data.get("character")) + 1
        chara = CharacterDice.objects.get(pk=character_id)
        character = serializers.serialize(
            'json', [chara])
        request.session[CHARACTER_KEY] = character

    character_form = SelectPlayerCharacter(request.POST or None)
    context = {'character_form': character_form}
    if character_form.is_valid():
        get_character(character_form)
        get_ally_context(character_form)
        return redirect('/dice')
    return render(request, 'dice/home_screen.html', context)


def all_character_view(request):
    """
    Views all different characters and their dice
    """
    queryset = CharacterDice.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, 'dice/character_list.html', context)


def dice_view(request):
    """
    Views to help the player decide which dice to use
    """
    character_from_session = serializers.deserialize(
        "json", request.session.get(CHARACTER_KEY))

    for chara in character_from_session:
        character = chara.object

    allies_from_session = serializers.deserialize(
        "json", request.session.get(ALLIES_KEY))

    allies = []
    for ally in allies_from_session:
        allies.append(ally.object)
    print("Called with {} {}".format(character, allies))
    context = {'character': character,
               'allies': allies}
    return render(request, 'dice/dice.html', context)


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
