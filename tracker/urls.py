from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView, ExpenseIncomeViewSet

# Creating a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expense')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Authentication Endpoints
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Expense/Income Endpoints (managed by the router)
    path('', include(router.urls)),
]