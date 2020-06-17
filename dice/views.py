"""
Required by django
"""
from django.shortcuts import render, redirect
from django.core import serializers

from .models import CharacterDice
from .forms import SelectPlayerCharacter, GetPlayerSpaces

ALLIES_KEY = 'allies'
CHARACTER_KEY = 'character'
BEST_DICE_KEY = 'best_dice'


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
    display = CharacterDice.objects.all().exclude(id=22).exclude(id=21)
    context['object_list'] = display
    if character_form.is_valid():
        get_character(character_form)
        get_ally_context(character_form)
        return redirect('/dice')
    return render(request, 'dice/home_screen.html', context)


def dice_view(request):
    """
    Views to help the player decide which dice to use
    """

    def get_characters():
        character_from_session = serializers.deserialize(
            "json", request.session.get(CHARACTER_KEY))

        allies_from_session = serializers.deserialize(
            "json", request.session.get(ALLIES_KEY))

        characters = [CharacterDice.objects.last()]
        for chara in character_from_session:
            characters.append(chara.object)

        for ally in allies_from_session:
            characters.append(ally.object)
        return characters

    def get_context_from_session():
        characters = get_characters()
        available_dice = []
        place_dice = []
        # statistics = []
        for character in characters:
            available_dice.append(character.get_true_dice())
            place_dice.append(character.get_places_dice())
            # statistics.append(character.get_statistics())
        return {'character': characters[1],
                'allies': characters[2:],
                'dice': available_dice,
                'place_dice': place_dice, }
        # 'statistics': statistics, }

    def handle_spaces_form():
        characters = get_characters()
        target = int(spaces_form.cleaned_data.get("spaces"))
        effect = spaces_form.cleaned_data.get("item")
        dice = []
        for chara in characters:
            dice.append(chara.get_places_dice())
        best_dice = CharacterDice.get_best_dice(dice, target, effect)
        if best_dice >= 0:
            dice_to_use = characters[best_dice]
            character = serializers.serialize(
                'json', [dice_to_use])
        else:
            character = 'Not Possible'
        request.session[BEST_DICE_KEY] = character

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
    try:
        character_from_session = serializers.deserialize(
            "json", request.session.get(BEST_DICE_KEY))
        for chara in character_from_session:
            character = chara.object

        return render(request, 'dice/best_dice.html', {'object': character})
    except:
        return render(request, 'dice/best_dice.html', {})


# def character_view(request, idenitifer):
#     """
#     Views a specific character
#     """
#     obj = get_object_or_404(CharacterDice, id=idenitifer)
#     context = {
#         'object': obj
#     }
#     print(obj)
#     return render(request, 'dice/character_detail.html', context)

# def all_character_view(request):
#     """
#     Views all different characters and their dice
#     """
#     queryset = CharacterDice.objects.all()
#     context = {
#         "object_list": queryset
#     }
#     return render(request, 'dice/character_list.html', context)
