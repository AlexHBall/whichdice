"""
Required by django
"""
from collections import Counter

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
    # TODO: Use filepath field ?
    character_image_path = models.CharField(max_length=50, default="null")
    character_dice_path = models.CharField(max_length=50, default="null")

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

    # def get_coins_dice(self):
    #     """
    #     Returns a list of coin places
    #     """
    #     sides = self.get_true_dice()
    #     coins = []
    #     for side in sides:
    #         if side[0] == '-' or side[0] == '+':
    #             coins.append(int(side))
    #         else:
    #             coins.append(0)
    #     return coins

    @staticmethod
    def get_best_dice(dices, target, effect):
        """
        Given a list of dices, return the one with the highest probability of getting target

        Effect can be +3,+5,-2
        """

        # TODO: Work out with effect
        # TODO: Work out with how many characters (-1,0 or 1,2)

        counters = []
        probabilites = []
        for dice in dices:
            counters.append(Counter(dice))

        for cntr in counters:
            probability = {}
            for num in cntr:
                probability[num] = cntr[num]/6
            probabilites.append(probability)
        dice_number = -1
        current_dice = 0
        current_highest_p = 0
        for dice in probabilites:
            try:
                if dice[target] > current_highest_p:
                    current_highest_p = dice[target]
                    dice_number = current_dice
            except KeyError:
                pass
            current_dice += 1

        return dice_number
