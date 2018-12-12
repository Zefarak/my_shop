from rest_framework import permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (BillCategoryListSerializer, BillCategoryDetailSerializer,
                          BillListSerializer, BillDetailSerializer)
from ..models import Bill, BillCategory


@api_view(['GET'])
def transaction_homepage(request, format=None):
    return Response({
        'bill-categories': reverse('api_bill_category_list', request=request, format=None),
        'bills': reverse('api_bill_list', request=request, format=None)
    })


class BillCategoryListApiView(generics.ListCreateAPIView):
    serializer_class = BillCategoryListSerializer
    queryset = BillCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


class BillCategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillCategoryDetailSerializer
    queryset = BillCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


class BillListApiView(generics.ListCreateAPIView):
    serializer_class = BillListSerializer
    queryset = Bill.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('is_paid', 'category')


class BillDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillDetailSerializer
    queryset = Bill.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]