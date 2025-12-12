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
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data["name"], description=data["description"]))

    car_model_data = [
        {
            "name": "Pathfinder",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
        },
        {
            "name": "Qashqai",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
        },
        {
            "name": "XTRAIL",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[0],
        },
        {
            "name": "A-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
        },
        {
            "name": "C-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
        },
        {
            "name": "E-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[1],
        },
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {
            "name": "Sorrento",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[3],
        },
        {
            "name": "Carnival",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[3],
        },
        {
            "name": "Cerato",
            "type": "Sedan",
            "year": 2023,
            "car_make": car_make_instances[3],
        },
        {
            "name": "Corolla",
            "type": "Sedan",
            "year": 2023,
            "car_make": car_make_instances[4],
        },
        {
            "name": "Camry",
            "type": "Sedan",
            "year": 2023,
            "car_make": car_make_instances[4],
        },
        {
            "name": "Kluger",
            "type": "SUV",
            "year": 2023,
            "car_make": car_make_instances[4],
        },
        # Add more CarModel instances as needed
    ]
    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            car_make=data["car_make"],
            type=data["type"],
            year=data["year"],
        )

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
    CarModel.objects.create(name="Corolla", type="SEDAN", year=2020, car_make=make1)
    CarModel.objects.create(name="Camry", type="SEDAN", year=2021, car_make=make1)
    CarModel.objects.create(name="RAV4", type="SUV", year=2022, car_make=make1)

    CarModel.objects.create(name="F-150", type="WAGON", year=2020, car_make=make2)
    CarModel.objects.create(name="Mustang", type="SEDAN", year=2021, car_make=make2)
    CarModel.objects.create(name="Explorer", type="SUV", year=2022, car_make=make2)

    CarModel.objects.create(name="X5", type="SUV", year=2020, car_make=make3)
    CarModel.objects.create(name="3 Series", type="SEDAN", year=2021, car_make=make3)
    CarModel.objects.create(name="i8", type="WAGON", year=2022, car_make=make3)

    CarModel.objects.create(name="Nexon", type="SUV", year=2020, car_make=make4)
    CarModel.objects.create(name="Altroz", type="SEDAN", year=2021, car_make=make4)
    CarModel.objects.create(name="Harrier", type="WAGON", year=2022, car_make=make4)

    CarModel.objects.create(name="Civic", type="SEDAN", year=2020, car_make=make5)
    CarModel.objects.create(name="Accord", type="SEDAN", year=2021, car_make=make5)
    CarModel.objects.create(name="CR-V", type="SUV", year=2022, car_make=make5)

    print("Database cleared and repopulated with 5 CarMakes and 15 CarModels.")


if __name__ == "__main__":
    initiate()
