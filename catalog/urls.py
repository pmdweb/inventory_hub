from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet) # Register the viewset with the router

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
]
# This will automatically create the necessary URLs for the CategoryViewSet
# such as:
# - /categories/ (GET, POST)
# - /categories/{id}/ (GET, PUT, PATCH, DELETE)

# This allows us to easily manage the API endpoints for the Category model.
