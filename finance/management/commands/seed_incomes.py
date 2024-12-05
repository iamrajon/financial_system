import random
from faker import Faker
from django.core.management.base import BaseCommand
from finance.models import Income
from django.contrib.auth import get_user_model

User = get_user_model()  



"""
** Custom Command to seed random, fake incode data to databse for testing and debugging purpose

** How to seed data:
python manage.py seed_incomes --count 50
python manage.py seed_incomes 

"""

class Command(BaseCommand):
    help = "Generate random Income records for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=10, help="Number of Income records to create"
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        # Get all existing users; this assumes you have some users in your database
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found in the database. Please create some users first."))
            return

        incomes = []
        for _ in range(count):
            user = random.choice(users)  # Randomly assign a user
            income = Income(
                user=user,
                source_name=fake.job(),
                amount=round(random.uniform(1000, 50000), 2),  # Random amount between 1000 and 50000
                date_received=fake.date_this_year(),  # Random date in the current year
                status=random.choice([Income.IncomeStatus.PENDING, Income.IncomeStatus.RECEIVED]),
                notes=fake.text(max_nb_chars=200),
            )
            incomes.append(income)

        # Bulk create the income records
        Income.objects.bulk_create(incomes)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} Income records."))


