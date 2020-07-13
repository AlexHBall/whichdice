from django.test import TestCase
from dice.models import CharacterDice, get_best_dice,get_best_dice_new


class ModelsTestCase(TestCase):
    def test_places_die(self):
        """ """
        dice = CharacterDice.objects.create(
            character_name="Test Character", dice_side_1="1", dice_side_2="-1", dice_side_3="+4",
            dice_side_4="2", dice_side_5="3", dice_side_6="2")
        places = dice.get_places_dice()
        self.assertEqual(places, [1, 0, 0, 2, 3, 2])

    # def test_golden_mushroom(self):
    #     default = CharacterDice.objects.create(
    #         character_name="Default", dice_side_1="1", dice_side_2="2", dice_side_3="3",
    #         dice_side_4="4", dice_side_5="5", dice_side_6="6")
    #     bowser_jr = CharacterDice.objects.create(
    #         character_name="Bowser Jr", dice_side_1="1", dice_side_2="1", dice_side_3="1",
    #         dice_side_4="4", dice_side_5="4", dice_side_6="9")
    #     koopa = CharacterDice.objects.create(
    #         character_name="Koopa", dice_side_1="1", dice_side_2="1", dice_side_3="2",
    #         dice_side_4="3", dice_side_5="3", dice_side_6="10")
    #     monty_mole = CharacterDice.objects.create(
    #         character_name="Monty Mole", dice_side_1="+1", dice_side_2="2", dice_side_3="3",
    #         dice_side_4="4", dice_side_5="5", dice_side_6="6")

    #     dices = [default,bowser_jr,koopa,monty_mole]
    #     effect = 5
    #     result = get_best_dice(dices,-2,effect)
    #     print(result)

    def test_best_dice_one_character_no_item(self):
        default = CharacterDice.objects.create(
            character_name="Default", dice_side_1="1", dice_side_2="2", dice_side_3="3",
            dice_side_4="4", dice_side_5="5", dice_side_6="6")
        bowser_jr = CharacterDice.objects.create(
            character_name="Bowser Jr", dice_side_1="1", dice_side_2="1", dice_side_3="1",
            dice_side_4="4", dice_side_5="4", dice_side_6="9")

        dices = [default,bowser_jr]
        effect = 0
        target = 9
        best_dice = get_best_dice(dices,target,effect)
        self.assertEqual(best_dice,{1: 1.0})

    def test_best_dice_one_character_negative_spaces(self):
        default = CharacterDice.objects.create(
            character_name="Default", dice_side_1="1", dice_side_2="2", dice_side_3="3",
            dice_side_4="4", dice_side_5="5", dice_side_6="6")
        bowser_jr = CharacterDice.objects.create(
            character_name="Bowser Jr", dice_side_1="1", dice_side_2="1", dice_side_3="1",
            dice_side_4="4", dice_side_5="4", dice_side_6="9")

        dices = [default,bowser_jr]
        effect = 0
        target = -3
        best_dice = get_best_dice(dices,target,effect)
        self.assertEqual(best_dice,{-1: 1.0})

    def test_best_dice_one_character_too_many_spaces(self):
        default = CharacterDice.objects.create(
            character_name="Default", dice_side_1="1", dice_side_2="2", dice_side_3="3",
            dice_side_4="4", dice_side_5="5", dice_side_6="6")
        bowser_jr = CharacterDice.objects.create(
            character_name="Bowser Jr", dice_side_1="1", dice_side_2="1", dice_side_3="1",
            dice_side_4="4", dice_side_5="4", dice_side_6="9")

        dices = [default,bowser_jr]
        effect = 0
        target = 50
        best_dice = get_best_dice(dices,target,effect)
        self.assertEqual(best_dice,{-1: 1.0})