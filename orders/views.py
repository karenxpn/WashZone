from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from WashZone.permissions import IsOwnerOrProvider, IsOwner
from authentication.decorators import validate_request
from orders.order_models.order import Order
from orders.schemas import orders_schema
from orders.serializers.create.create_order_serializer import CreateOrderSerializer
from orders.serializers.order_serializer import OrderSerializer
from orders.serializers.update_order_serializer import UpdateOrderSerializer


# Create your views here.

@orders_schema
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__service', 'items__provider', 'items__features')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateOrderSerializer
        if self.action in ['create']:
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(owner=self.request.user).order_by('-id')
        queryset = (queryset
                    .select_related('owner', 'service', 'provider')
                    .prefetch_related('order_features__feature'))

        return queryset


    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwner()]

        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            return [IsAuthenticated(), IsOwnerOrProvider()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @validate_request(CreateOrderSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @validate_request(UpdateOrderSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @validate_request(UpdateOrderSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


