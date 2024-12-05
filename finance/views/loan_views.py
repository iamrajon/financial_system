from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from finance.serializers import LoanSerializer
from finance.models import Loan
from finance.filters import LoanFilter, CustomDynamicFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.core.cache import cache
from drf_spectacular.utils import extend_schema



#class based views for Loan Management: ie. List, Create, Retrieve, Update and Delete 
@extend_schema(tags=["Loan"])
class LoanListCreateView(ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, CustomDynamicFilterBackend]
    filterset_class = LoanFilter
    search_fields = ['loan_name', 'notes']
    ordering_fields = ['loan_name', 'principal_amount', 'remaining_balance']

    def get_queryset(self):
        auth_user_loans_list = Loan.objects.filter(user=self.request.user)
        return auth_user_loans_list
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Loans List with cache inmplemented
@extend_schema(tags=["Loan"])
class LoanListCachedView(GenericAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"loan_list_{user.id}"  # Create unique cache key for loan
        cached_data = cache.get(cache_key)

        if cached_data is None:
            auth_user_loan_list = Loan.objects.filter(user=user)
            cache.set(cache_key, list(auth_user_loan_list), timeout=3600)
            cached_data = auth_user_loan_list

        return cached_data
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to return a cached list of loan
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# Loan Details Veiw for (retrieve, update and delete)
@extend_schema(tags=["Loan"])
class LoanRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)
    
    
