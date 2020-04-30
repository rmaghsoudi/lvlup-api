from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_type

# Create your models here.
class Entry(models.Model):
  name = models.CharField(max_length=50, blank=True)
  completed = models.BooleanField(default=False)
  description = models.CharField(
    max_length=500,
    blank=True,
    null=True
    )
  # Creates a one-to-many relationship with itself
  parentId = models.ForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.SET_NULL
    )
  # Creates a one-to-many relationship with itself
  user = models.ForeignKey(
    'User',
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
    default = 1,
    validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

  # Tells django what to print out when printing an instance
  def __str__(self):
    return self.name

class User(models.Model):
    authId = models.CharField(max_length=100)
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    xp = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.authId
    pass
