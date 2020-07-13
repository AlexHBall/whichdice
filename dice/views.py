"""
Required by django
"""
from django.shortcuts import render, redirect
from django.core import serializers

from .models import CharacterDice,get_best_dice
from .forms import SelectPlayerCharacter, GetPlayerSpaces, CustomPlayerForm

import json

ALLIES_KEY = 'allies'
CHARACTER_KEY = 'characters'
BEST_DICE_KEY = 'best_dice'
TARGET_SPACES_KEY = 'target'


def home_view(request):
    """
    Home Screen, default location
    """
    request.session.flush()

    def get_characters(form):
        result = []
        ids = form.cleaned_data['name']
        for i in ids:
            to_query = int(i) + 1
            result.append(CharacterDice.objects.get(pk=to_query))
        request.session[CHARACTER_KEY] = serializers.serialize(
            'json', result)

    character_form = CustomPlayerForm(request.POST or None)
    context = {'form': character_form}
    display = CharacterDice.objects.all().exclude(id=22).exclude(id=21)
    context['object_list'] = display

    if character_form.is_valid():
        get_characters(character_form)
        return redirect("/dice")
    return render(request, 'dice/home_screen.html', context)


def dice_view(request):
    """
    Views to help the player decide which dice to use
    """

    def get_characters():
        character_from_session = serializers.deserialize(
            "json", request.session.get(CHARACTER_KEY))

        characters = [CharacterDice.objects.last()]
        for chara in character_from_session:
            characters.append(chara.object)

        return characters

    def get_context_from_session():
        characters = get_characters()
        available_dice = []
        place_dice = []
        for character in characters:
            available_dice.append(character.return_dice())
            place_dice.append(character.get_places_dice())
        return {'characters': characters[1:],
                'dice': available_dice,
                'place_dice': place_dice, }

    def handle_spaces_form():
        effects = {"0": 0, "1": 3, "2": 5, "3": -2}
        characters = get_characters()
        target = int(spaces_form.cleaned_data.get("spaces"))
        effect = effects[spaces_form.cleaned_data.get("item")]
        dice = [chara for chara in characters]
        best_dice = get_best_dice(dice, target, effect)
        print(best_dice)
        character_dice_dict = {}
        for key in best_dice:
            if key > 0:
                # TODO: When key is -1 this isn't possible needs to change
                character_dice_dict[characters[key].character_name] = str(
                    best_dice[key]*100) + "%"
        print(character_dice_dict)
        if character_dice_dict.keys():
            character = json.dumps(character_dice_dict)
        else:
            character = 'Not Possible'
        request.session[BEST_DICE_KEY] = character
        request.session[TARGET_SPACES_KEY] = target

    context = get_context_from_session()
    spaces_form = GetPlayerSpaces(request.POST or None)
    context['form'] = spaces_form
    if spaces_form.is_valid():
        handle_spaces_form()
        return redirect('/best_dice')
    return render(request, 'dice/dice.html', context)


def best_dice_view(request):
    """
    Displays the best dice to use
    """
    target = request.session.get(TARGET_SPACES_KEY)

    try:
        character = json.loads(request.session.get(BEST_DICE_KEY))

        return render(request, 'dice/best_dice.html', {'object': character, 'target': target})
    except:
        return render(request, 'dice/best_dice.html', {'target' : target})
