from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mptt_demo.apps.categories.views import CategoryViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("categories", CategoryViewSet)


app_name = "api"
urlpatterns = router.urls
