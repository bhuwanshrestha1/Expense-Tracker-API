from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ExpenseIncome

# User Serializer for registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Expense/Income Serializer (for list view)
class ExpenseIncomeListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = ['id', 'title', 'amount', 'transaction_type', 'total', 'created_at']

    def get_total(self, obj):
        if obj.tax_type == 'percentage':
            return obj.amount + (obj.amount * obj.tax / 100)
        return obj.amount + obj.tax

# Expense/Income Serializer (for detail/create/update views)
class ExpenseIncomeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'user', 'title', 'description', 'amount', 'transaction_type', 
            'tax', 'tax_type', 'total', 'created_at', 'updated_at'
        ]

    def get_total(self, obj):
        """Calculates total based on tax type."""
        if obj.tax_type == 'percentage':
            return obj.amount + (obj.amount * obj.tax / 100)
        # Default to flat tax
        return obj.amount + obj.tax