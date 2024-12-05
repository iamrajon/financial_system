from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from finance.serializers import ExpenseSerializer
from finance.models import Expense
from finance.filters import ExpenseFilter, CustomDynamicFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.core.cache import cache
from drf_spectacular.utils import extend_schema



# class based views for Expense Management: ie. List, Create, Retrieve, Update and Delete 
@extend_schema(tags=["Expense"])
class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpenseFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, CustomDynamicFilterBackend]
    search_fields = ['category', 'notes']
    ordering_fields = ['amount', 'due_date']

    def get_queryset(self):
        auth_user_expenses_list = Expense.objects.filter(user=self.request.user).order_by('id')
        return auth_user_expenses_list
    
    def perform_create(self, serializer):
        # set the user with the current user while creating new Expense since user is also mentioned in ExpenseSerializer
        serializer.save(user=self.request.user)


# Expense List with cache implemented
@extend_schema(tags=["Expense"])
class ExpenseListCachedView(GenericAPIView):
    """
    View to return a cached list of expense data for authenticated users.
    Only handles GET requests.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"expense_list_{user.id}" # Create unique cache key for expense
        cached_data = cache.get(cache_key)

        if cached_data is None:
            auth_user_expense_list = Expense.objects.filter(user=user)
            cache.set(cache_key, list(auth_user_expense_list), timeout=3600)
            cached_data = auth_user_expense_list

        return cached_data
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to return a cached list of expense
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# Income deatail view (retrieve, update, delete)
@extend_schema(tags=["Expense"])
class ExpenseRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auth_user_expense_instance = Expense.objects.filter(user=self.request.user)
        return auth_user_expense_instance


