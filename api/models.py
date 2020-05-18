from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .helpers import validate_type

# Create your models here.


class User(models.Model):
    auth_id = models.CharField(
        max_length=100,
        unique=True
    )
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    xp = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    xp_to_lvlup = models.IntegerField(
        default=1515,
        validators=[MinValueValidator(1515)]
    )

# CLASS METHODS
    def __str__(self):
        return self.auth_id

    # leveling formula, using the current level it determines how much is needed to lvlup
    def calculate_xp_to_lvlup(self, level=None):
        if level == None:
            xp_needed = 5 * (self.level ^ 2) + 500 * self.level + 1000
        else:
            xp_needed = 5 * (level ^ 2) + 500 * level + 1000
        return xp_needed

    # calculates when xp can level up user more than once
    def multiple_lvlup(self, xp):
        running = True
        xp = xp
        level = self.level + 1

        while running:
            if xp >= self.calculate_xp_to_lvlup(level):
                level += 1
                xp -= self.calculate_xp_to_lvlup(level)
            else:
                running = False
        return xp, level

    # handles level logic when xp is sent in a request
    def leveling(self, xp):
      # build new object because serializer doesn't accept User objects
        user = {
          'id': self.id, 
          'auth_id': self.auth_id, 
          'level': self.level, 
          'xp': self.xp, 
          'xp_to_lvlup': self.xp_to_lvlup, 
          'entries': self.entries
        }
        xp_to_add = xp
        xp_needed = user['xp_to_lvlup']
        new_xp = user['xp'] + xp_to_add
        xp_diff = new_xp - xp_needed

        if xp_diff >= self.calculate_xp_to_lvlup((self.level + 1)):
            new_xp, new_level = self.multiple_lvlup(new_xp)
            user['level'] = new_level
            user['xp'] = new_xp
            user['xp_to_lvlup'] = self.calculate_xp_to_lvlup(new_level)

        elif new_xp >= xp_needed:
            user['level'] += 1
            user['xp'] = xp_diff
            user['xp_to_lvlup'] = self.calculate_xp_to_lvlup(user['level'])

        else:
            user['xp'] = new_xp

        return user


class Entry(models.Model):
    name = models.CharField(max_length=50, blank=True)
    completed = models.BooleanField(default=False)
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    # Creates a one-to-many relationship with itself
    parent_entry = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    # Creates a one-to-many relationship with itself
    user = models.ForeignKey(
        User,
        related_name='entries',
        on_delete=models.CASCADE
    )
    # Uses my custom validator to ensure proper values are saved
    type = models.CharField(
        max_length=6,
        blank=True,
        validators=[validate_type]
    )
    # Validates int to ensure it's not < 1 or > 10
    difficulty = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    xp = models.IntegerField(
        default=100,
        validators=[MinValueValidator(100), MaxValueValidator(10000)]
    )

    # Tells django what to print out when printing an instance
    def __str__(self):
        return self.name
