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

    def __str__(self):
        return self.auth_id

    pass

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
    default = 1,
    validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

  xp = models.IntegerField(
    default=100,
    validators=[MinValueValidator(100), MaxValueValidator(10000)]
  )

  # Tells django what to print out when printing an instance
  def __str__(self):
    return self.name
