import random
from faker import Faker
from django.core.management.base import BaseCommand
from finance.models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()  

"""
** Custom Command to seed random, fake expense data to databse for testing and debugging purpose

** How to seed data:
python manage.py seed_expenses --count 50
python manage.py seed_expenses 

"""

class Command(BaseCommand):
    help = "Generate random Expense records for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help="Number of Expense records to create"
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        # Get all existing users; assume users already exist in the database
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found in the database. Please create some users first."))
            return

        categories = ["Food", "Rent", "Travel", "Utilities", "Entertainment", "Miscellaneous"]
        statuses = ["pending", "paid"]

        expenses = []
        for _ in range(count):
            user = random.choice(users)  # Randomly assign an existing user
            expense = Expense(
                user=user,
                category=random.choice(categories),  # Randomly pick a category
                amount=round(random.uniform(10, 5000), 2),  # Random amount between 10 and 5000
                due_date=fake.date_between(start_date="-1y", end_date="today"),  # Random date within the last year
                status=random.choice(statuses),  # Randomly select "pending" or "paid"
                notes=fake.sentence(nb_words=10),  # Random sentence with 10 words
            )
            expenses.append(expense)

        # Bulk create expenses
        Expense.objects.bulk_create(expenses)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} Expense records."))
