from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import NetworkNode, Product
from .permissions import IsActiveEmployee
from .serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели NetworkNode с фильтрацией по стране
    """

    queryset = NetworkNode.objects.all().select_related("supplier").prefetch_related("products")
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели Product
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
