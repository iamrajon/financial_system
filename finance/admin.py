from django.contrib import admin
from finance.models import Income, Expense, Loan

# Register your models here.
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'source_name', 'amount', 'date_received', 'status', 'created_at']
    search_fields = ['source_name', 'status']
    list_filter = ['status', 'user', 'date_received'] 
    


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'amount', 'due_date', 'status', 'created_at']
    search_fields = ['category', 'status']
    list_filter = ['status', 'user', 'due_date']



# Register Loan Model to admin_panel
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'loan_name', 'principal_amount', 'interest_rate', 'tenure_months', 'monthly_installment', 'status','created_at']
    search_fields = ['loan_name', 'status']
    list_filter = ['status', 'remaining_balance', 'user']


admin.site.register(Loan, LoanAdmin)