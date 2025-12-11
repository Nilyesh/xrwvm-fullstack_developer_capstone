# Uncomment the following imports before adding the Model code

from django.db import models

# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# CarModel model
class CarModel(models.Model):
    name = models.CharField(max_length=50)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # link to CarMake
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        # Add more choices as required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default="SUV")
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])

    def __str__(self):
        return f"{self.name} ({self.year})"

        # Add more choices as required
class Dealer(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
        
    # Other fields as needed

 # method to print a car make object