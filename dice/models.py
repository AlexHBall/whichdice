"""
Required by django
"""
from statistics import mean

from django.db import models
# Create your models here.


class CharacterDice(models.Model):
    """
    Models a character and their dice
    """
    character_name = models.CharField(max_length=20)
    dice_side_1 = models.CharField(max_length=3)
    dice_side_2 = models.CharField(max_length=3)
    dice_side_3 = models.CharField(max_length=3)
    dice_side_4 = models.CharField(max_length=3)
    dice_side_5 = models.CharField(max_length=3)
    dice_side_6 = models.CharField(max_length=3)

    def return_dice(self):
        """
        Returns a readable string for the dice
        """
        return '{},{},{},{},{},{}'.format(self.dice_side_1, self.dice_side_2, self.dice_side_3,
                                          self.dice_side_4, self.dice_side_5, self.dice_side_6)

    def __str__(self):
        """
        More easily readable string
        """
        return "{} - ({})".format(self.character_name, self.return_dice())

    def get_true_dice(self):
        """
        Returns a list of dice sides
        """
        return [self.dice_side_1, self.dice_side_2, self.dice_side_3,
                self.dice_side_4, self.dice_side_5, self.dice_side_6]

    def get_places_dice(self):
        """
        Returns a list of moveable places
        """
        sides = self.get_true_dice()
        places = []
        for side in sides:
            if side[0] == '-' or side[0] == '+':
                places.append(0)
            else:
                places.append(int(side))
        return places

    def get_coins_dice(self):
        """
        Returns a list of coin places
        """
        sides = self.get_true_dice()
        coins = []
        for side in sides:
            if side[0] == '-' or side[0] == '+':
                coins.append(int(side))
            else:
                coins.append(0)
        return coins

    def get_range(self):
        """
        Gets the range from a nice
        """
        place_dice = self.get_places_dice()
        return abs(max(place_dice) - min(place_dice))

    def get_statistics(self):
        """
        Return tuple of stastical information for one dice
        (min, max, mean, range)
        """
        place_dice = self.get_places_dice()
        return (min(place_dice), max(place_dice), mean(place_dice), self.get_range())
