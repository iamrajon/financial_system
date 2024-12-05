from rest_framework import serializers
from .models import Income, Expense, Loan
from datetime import date



# ModelSerializer for Income Model
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'source_name', 'amount', 'date_received', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    


# ModelSerializer for Expense Model
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'amount', 'due_date', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_due_date(self, value):
        #Ensure the due date is not in the past
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    

# ModelSerializer for Loan Model
class LoanSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.DecimalField(
        max_digits = 12, 
        decimal_places = 2,
        read_only = True,
        help_text = "The Dynamically calculated monthly installment for Loan"
    )

    class Meta:
        model = Loan
        fields = ['id', 'user', 'loan_name', 'principal_amount', 'interest_rate', 'tenure_months', 'monthly_installment', 'remaining_balance', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'monthly_installment', 'created_at', 'updated_at']

    def validate_principal_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The principal_amount must be greater than 0.")
        return value
    
    def validate_interest_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("The interest_rate cannot be negative.")
        return value
    
    def validate_tenure_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("The tenure_month must be greater than 0.")
        return value
    
    def validate_remaining_balance(self, value):
        principal_amount = self.initial_data.get('principal_amount') if not self.instance else self.instance.principal_amount
        if value < 0:
            raise serializers.ValidationError("The remaining_balance cannot be negative.")
        elif principal_amount and value > float(principal_amount):
            raise serializers.ValidationError("Remaining balance cannot exceed the principal amount.")
        return value


# Serializer fo Report
class ReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)