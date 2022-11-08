"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import include, path

from apps.users.tasks import check

from .views import ProtectedDefaultRoute

urlpatterns = [
    path("admin/", admin.site.urls),
    path("protected/", ProtectedDefaultRoute.as_view()),
    path("healthz/", lambda request: HttpResponse()),
    path("worker-check/", lambda request: check.delay(0, 0)),
    path("v2/tours/", include("apps.natours.api.v2.urls.tours")),
    path("v2/reports/", include("apps.natours.api.v2.urls.reports")),
    path("v1/", include("apps.reviews.api.v1.urls.tour_review")),
    path("v1/", include("apps.users.api.v1.urls.auth")),
    path("v1/", include("apps.users.api.v1.urls.users")),
    path("v1/", include("apps.users.api.v1.urls.profile")),
    path("v1/", include("apps.bookings.api.v1.urls.booking_tours")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
