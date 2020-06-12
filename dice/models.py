"""
Required by django
"""
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
