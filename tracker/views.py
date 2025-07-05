from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import ExpenseIncome
from .serializers import UserSerializer, ExpenseIncomeSerializer, ExpenseIncomeListSerializer
from .permissions import IsOwnerOrIsAdmin

# Authentication Views
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# Expense/Income ViewSet
class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows expenses/incomes to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrIsAdmin]

    def get_queryset(self):
        """
        This view should return a list of all the expenses/incomes
        for the currently authenticated user. Superusers can see all.
        """
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-created_at')
        return ExpenseIncome.objects.filter(user=user).order_by('-created_at')

    def get_serializer_class(self):
        """
        Return different serializers for list and detail views.
        """
        if self.action == 'list':
            return ExpenseIncomeListSerializer
        return ExpenseIncomeSerializer

    def perform_create(self, serializer):
        """
        Associate the logged-in user with the new expense/income record.
        """
        serializer.save(user=self.request.user)