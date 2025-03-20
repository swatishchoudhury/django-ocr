from django.urls import path
from . import views

urlpatterns = [
    path('api/extract-dob/', views.extract_dates_api, name='extract_dates_api'),
]