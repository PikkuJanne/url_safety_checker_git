from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_url, name='submit_url'),  # URL for submitting URLs
    path('result/<int:url_id>/', views.display_result, name='display_result'),
    path('api/submit-url/', views.submit_url, name='api-submit-url'),
    path('history/', views.history, name='history'),
]

