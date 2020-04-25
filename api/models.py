from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_type

# Create your models here.
class Entry(models.Model):
  name = models.CharField(max_length=50)
  completed = models.BooleanField(default=False)
  description = models.CharField(
    max_length=500,
    blank=True,
    default=''
    )
  # Creates a one-to-many relationship with itself
  parentId = models.ForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.SET_NULL
    )
  # Uses my custom validator to ensure proper values are saved
  type = models.CharField(
    max_length=6,
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
