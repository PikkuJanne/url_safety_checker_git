from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from url_checker import views as app_views
from .openapi_config import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('url-checker/', include('url_checker.urls')),  
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', app_views.register, name='register'),
    path('api/register/', app_views.api_register, name='api-register'),
    path('api/login/', app_views.api_login, name='api-login'),
    path("api/", include("url_checker.urls")),
    path("swagger<str:format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
