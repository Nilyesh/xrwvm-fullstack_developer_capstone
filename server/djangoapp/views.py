# Uncomment the required imports before adding the code
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .populate import initiate
import json
import logging

from .models import CarMake, CarModel, Dealer
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=401)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({"error": "Invalid request"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
    return JsonResponse({"error": "POST request required"}, status=405)


@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email
        )
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


from django.http import JsonResponse
from .models import Dealer
from .restapis import get_request


def get_dealerships(request, state="All"):
    dealerships = []
    try:
        if state == "All":
            endpoint = "/fetchDealers"
        else:
            endpoint = f"/fetchDealers/state/{state}"

        dealerships = get_request(endpoint)

        if dealerships is None:
            dealerships = []

        # FIX: Change 'dealership' to 'dealerships'
        return JsonResponse({"status": 200, "dealers": dealerships})

    except Exception as e:
        print(f"Error in get_dealership: {e}")
        return JsonResponse({"status": 500, "dealers": []})

        # 7. Return a failure status, but still return an empty list of dealers
        #    so the page doesn't crash on the frontend.
        return JsonResponse({"status": 500, "dealers": []})


# server/djangoapp/views.py


def get_dealer_details(request, dealer_id):
    if dealer_id:
        # Correctly assign the fetched data to the 'dealer' variable
        endpoint = f"/fetchDealer/{dealer_id}"
        dealer = get_request(endpoint)
        
        # Now 'dealer' exists and can be used here
        return JsonResponse({"status": 200, "dealer": dealer})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        try:
            reviews = get_request(endpoint)

            # If reviews is None or empty, return early with an empty list
            if not reviews:
                return JsonResponse({"status": 200, "reviews": []})

            for review_detail in reviews:
                try:
                    response = analyze_review_sentiments(review_detail["review"])
                    review_detail["sentiment"] = response.get("sentiment", "neutral")
                except Exception as e:
                    print(f"Sentiment error: {e}")
                    review_detail["sentiment"] = "neutral"

            return JsonResponse({"status": 200, "reviews": reviews})
        except Exception as e:
            return JsonResponse({"status": 500, "message": "Internal Server Error"})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        if not request.user.is_anonymous:
            try:
                data = json.loads(request.body)
                response = post_review(data)
                
                # Change the check: if post_review returns any data, 
                # it means the microservice was reached and responded.
                if response: 
                    return JsonResponse({"status": 200})
                else:
                    return JsonResponse({"status": 400, "message": "Microservice failed to save review"})
            except Exception as e:
                print(f"Error in add_review: {e}")
                return JsonResponse({"status": 500, "message": str(e)})
        else:
            return JsonResponse({"status": 403, "message": "Unauthorized"})
    return JsonResponse({"status": 405, "message": "Method not allowed"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


def index(request):
    # This function renders the main index.html file from the React build folder.
    return render(request, "index.html")


def contact(request):
    # This assumes your contact page HTML is saved as 'contact.html'
    return render(request, "contact.html")
