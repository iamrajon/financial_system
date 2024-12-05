from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Current User Model
User = get_user_model()


# Model for Income
class Income(models.Model):
    class IncomeStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        RECEIVED = "received", _("Received")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    source_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    status = models.CharField(max_length=10, choices=IncomeStatus.choices, default=IncomeStatus.PENDING)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ("-created_at",)
        verbose_name = _("Income")
        verbose_name_plural = _("Incomes")
        indexes = [
            models.Index(fields=['user', 'source_name', 'status'])
        ]

    def __str__(self):
        return f"{self.user} - {self.source_name} - {self.amount} - {self.status}"
    


# Model for Expense
class Expense(models.Model):
    class ExpenseStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=ExpenseStatus.choices, default=ExpenseStatus.PAID)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ['-created_at']
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
        indexes = [
            models.Index(fields=['user', 'category', 'status']),
        ]

    def __str__(self):
        return f"Expense({self.category}, {self.amount}, {self.user})"


# Model for Loan Management
class Loan(models.Model):
    class LoanStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        PAID = "paid", _("Paid")
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    loan_name = models.CharField(max_length=120)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text=_("The Principal Amount of Loan."))
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("The annual interest rate for the loan (percentage)."))
    tenure_months = models.PositiveIntegerField(help_text=_("The loan tenure in months."))
    monthly_installment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text=_("The calculated monthly installment for this loan."))
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=LoanStatus.choices, default=LoanStatus.ACTIVE)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")

    def calculate_monthly_installment(self):
        """
        Calculate the monthly installment for the loan using the formula for EMI
        """
        if self.principal_amount and self.interest_rate and self.tenure_months:
            r = self.interest_rate / 12 / 100  # Monthly interest rate
            n = self.tenure_months
            P = self.principal_amount

            if r == 0:  # Special case: No interest rate
                emi = P / n
            else:
                emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)

            return round(emi, 2)
        return None
    
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate the monthly installment
        before saving the model.
        """
        self.monthly_installment = self.calculate_monthly_installment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_name} - {self.user}"



