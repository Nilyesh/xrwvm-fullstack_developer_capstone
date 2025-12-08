# Uncomment the required imports before adding the code
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            return JsonResponse({"message": "Registration successful"}, status=201)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"error": "Invalid request"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)

def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    endpoint = f"/getDealerDetails/{dealer_id}"
    dealer = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealer})

def get_dealer_reviews(request, dealer_id):
    endpoint = f"/getDealerReviews/{dealer_id}"
    reviews = get_request(endpoint)
    # Optionally analyze sentiment here
    for review in reviews:
        review["sentiment"] = analyze_review_sentiments(review.get("review", ""))
    return JsonResponse({"status": 200, "reviews": reviews})

@csrf_exempt
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": "success", "response": response})
        except Exception as e:
            logger.error(f"Add review error: {e}")
            return JsonResponse({"error": "Invalid request"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)
