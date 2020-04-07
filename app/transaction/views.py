from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.db.models import Sum, Count

from base.models import Transaction

from transaction import serializers


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    pagination_class = PageNumberPagination

    def retrieve(self, request, pk=None):
        t = Transaction.objects.get(id=pk)
        serializer = self.serializer_class(t)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        t = Transaction.objects.get(id=pk)
        t.is_deleted = True
        t.save()
        serializer = self.serializer_class(t)
        return Response(serializer.data)


class TransactionCreateViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin):
    serializer_class = serializers.TransactionCreateSerializer
    queryset = Transaction.objects.all()
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()


class TransactionBreakdownViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin):
    pagination_class = PageNumberPagination

    def retrieve(self, request, pk=None):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        filters = {'account_id': pk}

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            filters['date__gte'] = start_date
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            filters['date__lte'] = end_date

        queryset = (Transaction.objects
                    .filter(**filters)
                    .values('expense_type')
                    .annotate(num_transactions=Count('id'))
                    .annotate(amount_sum=Sum('amount'))
                    .values('expense_type', 'num_transactions', 'amount_sum'))

        return Response(queryset)
