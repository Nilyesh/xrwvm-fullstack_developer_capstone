import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproj.settings")
django.setup()

from djangoapp.models import CarMake, CarModel

def initiate():
    # Clear existing data
    CarMake.objects.all().delete()
    CarModel.objects.all().delete()

    # Create 5 CarMakes
    make1 = CarMake.objects.create(name="Toyota", description="Reliable Japanese cars")
    make2 = CarMake.objects.create(name="Ford", description="American classic cars")
    make3 = CarMake.objects.create(name="BMW", description="Luxury German cars")
    make4 = CarMake.objects.create(name="Tata", description="Indian innovation")
    make5 = CarMake.objects.create(name="Honda", description="Efficient Japanese cars")

    # Create 15 CarModels (3 per make)
    CarModel.objects.create(name="Corolla", type="SEDAN", year=2020, dealer_id=1, car_make=make1)
    CarModel.objects.create(name="Camry", type="SEDAN", year=2021, dealer_id=2, car_make=make1)
    CarModel.objects.create(name="RAV4", type="SUV", year=2022, dealer_id=3, car_make=make1)

    CarModel.objects.create(name="F-150", type="WAGON", year=2020, dealer_id=4, car_make=make2)
    CarModel.objects.create(name="Mustang", type="SEDAN", year=2021, dealer_id=5, car_make=make2)
    CarModel.objects.create(name="Explorer", type="SUV", year=2022, dealer_id=6, car_make=make2)

    CarModel.objects.create(name="X5", type="SUV", year=2020, dealer_id=7, car_make=make3)
    CarModel.objects.create(name="3 Series", type="SEDAN", year=2021, dealer_id=8, car_make=make3)
    CarModel.objects.create(name="i8", type="WAGON", year=2022, dealer_id=9, car_make=make3)

    CarModel.objects.create(name="Nexon", type="SUV", year=2020, dealer_id=10, car_make=make4)
    CarModel.objects.create(name="Altroz", type="SEDAN", year=2021, dealer_id=11, car_make=make4)
    CarModel.objects.create(name="Harrier", type="WAGON", year=2022, dealer_id=12, car_make=make4)

    CarModel.objects.create(name="Civic", type="SEDAN", year=2020, dealer_id=13, car_make=make5)
    CarModel.objects.create(name="Accord", type="SEDAN", year=2021, dealer_id=14, car_make=make5)
    CarModel.objects.create(name="CR-V", type="SUV", year=2022, dealer_id=15, car_make=make5)

    print("Database cleared and repopulated with 5 CarMakes and 15 CarModels.")

if __name__ == "__main__":
    initiate()
