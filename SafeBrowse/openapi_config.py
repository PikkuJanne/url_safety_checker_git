from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="URL Safety Checker",
        default_version="v1",
        description="Safe Browsing is a Google service that lets client applications check URLs against Google's constantly updated lists of unsafe web resources.",
        terms_of_service="https://developers.google.com/safe-browsing/v4",
        contact=openapi.Contact(email="example@example.com"),
        license=openapi.License(name="MIT license"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), 
)
