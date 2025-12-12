# Uncomment the imports before you add the code
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

app_name = "djangoapp"
urlpatterns = [
    path("admin/", admin.site.urls),
    # Dealer related paths
    path(route="get_dealers/", view=views.get_dealerships, name="get_dealers"),
    path(
        route="get_dealers/<str:state>/",
        view=views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path("dealer/<int:dealer_id>/", view=views.get_dealer_details, name="dealer_details"),
    path(
        "reviews/dealer/<int:dealer_id>/",
        view=views.get_dealer_reviews,
        name="dealer_reviews",
    ),
    path("logout/", views.logout, name="logout"),
    # User authentication paths
    path(route="login/", view=views.login_user, name="login"),
    path("register/", view=views.registration, name="register"),
    # Review submission path
    path("add_review/", view=views.add_review, name="add_review"),
    # Frontend React routes (serve index.html for these paths)
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("dealers/", TemplateView.as_view(template_name="index.html"), name="dealers"),
    path(
        "dealer/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html"),
        name="dealer_page",
    ),
    path(
        "postreview/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html"),
        name="post_review",
    ),
    path(route="get_cars", view=views.get_cars, name="getcars"),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
