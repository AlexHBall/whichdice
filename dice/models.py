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

    def get_places_dice_string(self):
        places = self.get_places_dice()
        return ', '.join(places)

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

        def calculate_dice_space_probabilties():
            probabilites = []
            for cntr in dice_counts:
                probability = {}
                for num in cntr:
                    probability[num] = cntr[num]/6
                probabilites.append(probability)
            return probabilites

        number_to_roll = target
        number_of_allies = len(dices) - 2
        if effect:
            number_to_roll -= int(effect)

        ally_rolls = calculate_ally_spaces(number_of_allies)
        numbers_to_roll = [number_to_roll-v for v in ally_rolls.keys()]
        dice_counts = [Counter(d) for d in dices]
        dice_probabilites = calculate_dice_space_probabilties()

        best_dice_for_spaces = {}
        for n in numbers_to_roll:
            dice_number = -1
            current_dice = 0
            current_highest_p = 0

            for dice in dice_probabilites:
                try:
                    if dice[n] > current_highest_p:
                        current_highest_p = dice[n]
                        dice_number = current_dice
                except KeyError:
                    pass
                current_dice += 1
            best_dice_for_spaces[n] = dice_number
        most_probable_ally_roll = max(
            ally_rolls.items(), key=operator.itemgetter(1))[0]

        #TODO Go through each probability sorted not -1 and find most common or return different probabilities
        probs = {k: v for k, v in sorted(
            ally_rolls.items(), key=lambda item: item[1], reverse=True)}

        try:
            return best_dice_for_spaces[most_probable_ally_roll]
        except KeyError:
            return -1
