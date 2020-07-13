"""
Required by django
"""
from collections import Counter
from itertools import product as comb_product
import operator

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

    def get_probabilites(self):
        probability = {}
        sides_counter = Counter(self.get_places_dice())
        for k in sides_counter.keys():
            probability[k] = sides_counter[k]/6
        return probability


def get_best_dice(dices, target, effect):
    """
    Given a list of dices, return the one with the highest probability of getting target

    Effect can be +3,+5,-2
    """

    def calculate_ally_spaces(number_of_allies):
        # TODO Calculate Bomb-O-Bomb
        dices = [[1, 2] for i in range(number_of_allies)]
        spaces = list(comb_product(*dices))
        totals = []
        for space in spaces:
            totals.append(sum(space))
        b = Counter(totals)
        probabilites = {}
        for k in b:
            probabilites[k] = b[k] / sum(b.values())
        return probabilites

    def get_best_dice_dict(dices, ally_roll, no_to_roll):
        best_dice_dict = {}
        numbers_to_roll = [no_to_roll-v for v in ally_roll.keys()]

        dice_prob_dicts = [d.get_probabilites() for d in dices]
        for n in numbers_to_roll:
            dice_number = -1
            current_dice = 0
            current_highest_p = 0
            for dice in dice_prob_dicts:
                try:
                    if dice[n] > current_highest_p:
                        current_highest_p = dice[n]
                        dice_number = current_dice
                except KeyError:
                    pass
                current_dice += 1
            best_dice_dict[n] = dice_number
        return best_dice_dict

    def get_roll_prob_dict(best_d_dict, ally_dict):
        # TODO Improve this it's incredibly hacky
        bad_list = list(best_d_dict.keys())
        very_bad_list = list(ally_dict.keys())
        bad_dict = {}
        for i in range(len(bad_list)):
            bad_dict[best_d_dict[bad_list[i]]
                     ] = ally_dict[very_bad_list[i]]
        return bad_dict

    number_to_roll = target
    number_of_allies = len(dices) - 2
    if effect:
        number_to_roll -= int(effect)

    ally_rolls = calculate_ally_spaces(number_of_allies)
    best_dice_dict = get_best_dice_dict(dices, ally_rolls, number_to_roll)
    return get_roll_prob_dict(best_dice_dict, ally_rolls)
