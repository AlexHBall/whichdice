from django.test import TestCase
from dice.models import CharacterDice


class ModelsTestCase(TestCase):
    def test_places_die(self):
        """ """
        dice = CharacterDice.objects.create(
            character_name="Test Character", dice_side_1="1", dice_side_2="-1", dice_side_3="+4",
            dice_side_4="2", dice_side_5="3", dice_side_6="2")
        places = dice.get_places_dice()
        self.assertEqual(places, [1,0,0,2,3,2])
