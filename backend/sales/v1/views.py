from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from lenta_backend.constants import ONLY_LIST_MSG
from sales.v1.models import Sales
from sales.v1.serializers import SalesFactSerializer, SalesGroupSerializer
from sales.v1.filters import SalesFilter


class SalesViewSet(viewsets.ModelViewSet):
    """Представление модели продаж.
    """
    queryset = Sales.objects.all()
    serializer_class = SalesGroupSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    pagination_class = LimitPageNumberPagination
    filterset_class = SalesFilter

    def retrieve(self, request, pk=None):
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)

    def get_serializer(self, *args, **kwargs):
        """Задает значение many=true, если передан список.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SalesViewSet, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == 'create':
            return SalesFactSerializer
        return self.serializer_class

    def get_serializer_context(self):
        """Передает дополнительный контекст для поиска по дате.
        """
        context = {'request': self.request}
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start and date_end:
            context['date_start'] = date_start
            context['date_end'] = date_end
        return context

    def list(self, request, *args, **kwargs):
        store_ids = self.request.query_params.getlist('store')
        sku_ids = self.request.query_params.getlist('sku')
        if not store_ids or not sku_ids:

            return Response(
                {'error': 'Не найдены данные с указанными параметрами'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = self.filter_queryset(self.get_queryset())
        data_list = []
        for obj in queryset:
            serializer = self.get_serializer(obj)
            if serializer.data not in data_list:
                data_list.append(serializer.data)
        return Response({"data": data_list})

    def create(self, request):
        serializer = self.get_serializer(data=request.data['data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=['get'])
    def ml_all(self, request, *args, **kwargs):
        queryset = Sales.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
