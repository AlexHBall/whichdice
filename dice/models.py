from django.db import models

# Create your models here.


class CharacterDice(models.Model):
    character_name = models.CharField(max_length=20)
    dice_side_1 = models.CharField(max_length=3)
    dice_side_2 = models.CharField(max_length=3)
    dice_side_3 = models.CharField(max_length=3)
    dice_side_4 = models.CharField(max_length=3)
    dice_side_5 = models.CharField(max_length=3)
    dice_side_6 = models.CharField(max_length=3)

    def return_dice(self):
        return '{},{},{},{},{},{}'.format(self.dice_side_1, self.dice_side_2, self.dice_side_3,
                                          self.dice_side_4, self.dice_side_5, self.dice_side_6)
