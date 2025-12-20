# Uncomment the imports before you add the code
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

app_name = "djangoapp"
urlpatterns = [
    # Admin and static management
    path("admin/", admin.site.urls),
    # --- 1. DATA API ROUTES (Backend) ---
    # These return JSON data. React calls these to fill the table/details.
    path(route="get_cars/", view=views.get_cars, name="getcars"),
    path(route="get_dealers/", view=views.get_dealerships, name="get_dealers"),
    path(route="get_dealers/<str:state>/", view=views.get_dealerships, name="get_dealers_by_state"),
    path(route="dealer/<int:dealer_id>/", view=views.get_dealer_details, name="getdealer_details"),
    path(route="reviews/dealer/<int:dealer_id>/", view=views.get_dealer_reviews, name="dealer_reviews"),
    path(route='get_dealer/<int:dealer_id>/', view=views.get_dealer_details, name='get_dealer_details'),
    # --- 2. USER AUTHENTICATION ROUTES ---
    path(route="login/", view=views.login_user, name="login"),
    path(route="register/", view=views.registration, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path(route="add_review/", view=views.add_review, name="add_review"),
    # --- 3. FRONTEND REACT ROUTES (UI) ---
    # These serve the index.html file so React can take over the UI.
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("dealers/", TemplateView.as_view(template_name="index.html"), name="dealers"),
    path("contact/", TemplateView.as_view(template_name="index.html"), name="contact"),
    # NOTE: Path changed to 'dealer_details' to avoid conflict with 'dealer/' API
    path("dealer_details/<int:dealer_id>/", TemplateView.as_view(template_name="index.html"), name="dealer_page"),
    path("postreview/<int:dealer_id>/", TemplateView.as_view(template_name="index.html"), name="post_review"),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
