import random
from faker import Faker
from django.core.management.base import BaseCommand
from finance.models import Loan
from django.contrib.auth import get_user_model

User = get_user_model()  

"""
** Custom Command to seed random, fake loan data to databse for testing and debugging purpose

** How to seed data:
python manage.py seed_loans --count 50
python manage.py seed_loans

"""


class Command(BaseCommand):
    help = "Generate random Loan records for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help="Number of Loan records to create"
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        # Get all existing users; assume users already exist in the database
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found in the database. Please create some users first."))
            return

        loan_statuses = [Loan.LoanStatus.ACTIVE, Loan.LoanStatus.PAID]
        loans = []

        for _ in range(count):
            user = random.choice(users)  # Assign loan to a random existing user
            principal_amount = round(random.uniform(10000, 1000000), 2)  # Random principal amount between 10,000 and 1,000,000
            interest_rate = round(random.uniform(2.0, 15.0), 2)  # Random interest rate between 2% and 15%
            tenure_months = random.randint(12, 120)  # Random tenure between 1 year and 10 years
            remaining_balance = round(principal_amount * random.uniform(0.5, 1.0), 2)  # Remaining balance between 50%-100% of principal

            loan = Loan(
                user=user,
                loan_name=fake.bs(),  # Generate a random, descriptive name
                principal_amount=principal_amount,
                interest_rate=interest_rate,
                tenure_months=tenure_months,
                remaining_balance=remaining_balance,
                status=random.choice(loan_statuses),
                notes=fake.sentence(nb_words=10),  # Random sentence with 10 words
            )
            
            
            loans.append(loan)

        # Bulk create loan records
        Loan.objects.bulk_create(loans)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} Loan records."))
