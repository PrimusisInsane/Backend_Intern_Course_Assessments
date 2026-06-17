from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('register/', RegisterView.as_view()),        # POST /api/register/
    path('login/', TokenObtainPairView.as_view()),    # POST /api/login/
    path('token/refresh/', TokenRefreshView.as_view()), # POST /api/token/refresh/
    path('', include(router.urls)),
]