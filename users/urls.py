from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.UsersViewSet)
app_name = "users"

urlpatterns = router.urls
