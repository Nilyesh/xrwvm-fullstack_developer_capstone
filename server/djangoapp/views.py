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

        # 3. Call the external service to fetch data
        # Assuming get_request handles the full URL formation
        dealerships = get_request(endpoint)
        print(f"DEBUG: Data received from Node API for state {state}: {dealerships}")
        # 4. Handle a potential None return from get_request (optional but good practice)
        if dealerships is None:
            dealerships = []

        # 5. Return the successful response
        return JsonResponse({"status": 200, "dealers": dealerships})

    except Exception as e:
        # 6. Log the error (this is why you saw the 504/timeout initially)
        print(f"Error in get_dealerships: {e}")

        # 7. Return a failure status, but still return an empty list of dealers
        #    so the page doesn't crash on the frontend.
        return JsonResponse({"status": 500, "dealers": []})


# server/djangoapp/views.py

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint) # This calls restapis.py
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    # 1. Check if dealer_id is provided
    if dealer_id:
        # FIX: Use an f-string (the 'f' before the quotes) to insert the dealer_id
        endpoint = f"/fetchReviews/dealer/{dealer_id}"

        try:
            # 2. Call the Node.js microservice
            print(f"Calling Node.js at: {endpoint}") # DEBUG LINE
            reviews = get_request(endpoint)
            print(f"Reviews received: {reviews}")    # DEBUG LINE

            # 3. Check if reviews exist; if not, initialize as empty list
            if reviews is None:
                reviews = []

            # 4. Iterate and add sentiment analysis
            for review_detail in reviews:
                # Call your sentiment analyzer service
                response = analyze_review_sentiments(review_detail["review"])
                # Add sentiment key to the review dictionary
                review_detail["sentiment"] = response.get("sentiment", "neutral")

            return JsonResponse({"status": 200, "reviews": reviews})

        except Exception as e:
            # This captures errors from get_request or analyze_review_sentiments
            print(f"Error in get_dealer_reviews: {e}")
            return JsonResponse({"status": 500, "message": "Error fetching reviews"})

    # 5. Handle case where dealer_id is missing
    else:
        return JsonResponse({"status": 400, "message": "Bad Request: Missing dealer_id"})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


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
