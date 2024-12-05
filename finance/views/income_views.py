from finance.serializers import IncomeSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from finance.models import Income
from rest_framework.permissions import AllowAny, IsAuthenticated
from finance.filters import IncomeFilter, CustomDynamicFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from drf_spectacular.utils import extend_schema



# class based views for Income List, Create, Retrieve, Update and Delete 
@extend_schema(tags=["Income"])
class IncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IncomeFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, CustomDynamicFilterBackend]
    search_fields = ['source_name', 'notes']
    ordering_fields = ['amount', 'date_received', 'source_name']

    def get_queryset(self):
        auth_user_income_list = Income.objects.filter(user=self.request.user)
        return auth_user_income_list

    def perform_create(self, serializer):
        """set the user field to current user"""
        serializer.save(user=self.request.user)


# Income List with Cache implemented
@extend_schema(tags=["Income"])
class IncomeListCachedView(GenericAPIView):
    """
    View to return a cached list of income data for authenticated users.
    Only handles GET requests.
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"income_list_{user.id}"  # Create a unique cache key for the user
        cached_data = cache.get(cache_key)  

        if cached_data is None:  # If no cache, fetch data from the DB and cache it
            auth_user_income_list = Income.objects.filter(user=user)
            cache.set(cache_key, list(auth_user_income_list), timeout=3600)  # Cache the queryset as a list
            cached_data = auth_user_income_list

        return cached_data

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to return a cached list of incomes.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# Income deatail view (retrieve, update, delete)
@extend_schema(tags=["Income"])
class IncomeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auth_user_income_instance = Income.objects.filter(user=self.request.user)
        return auth_user_income_instance
    

