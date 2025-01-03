from datetime import datetime

from rest_framework import status, request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from WashZone.permissions import IsOwnerOrProvider
from authentication.decorators import validate_request
from orders.order_models.time_slot import TimeSlot
from orders.schemas import close_time_slot_schema, closed_time_slots_list_schema
from orders.serializers.time_slot_serializer import CloseTimeSlotSerializer, TimeSlotSerializer


class SlotView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser(), IsOwnerOrProvider()]
        return [IsAuthenticated()]

    @close_time_slot_schema
    @validate_request(CloseTimeSlotSerializer)
    def post(self, request):
        serializer = CloseTimeSlotSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'message': 'Slot closed successfully',
        }, status=status.HTTP_200_OK)


    @closed_time_slots_list_schema
    def get(self, request):
        string_date = request.query_params.get('date')
        provider = request.query_params.get('provider', None)

        if not string_date:
            return Response({'message': 'Missing date parameter'}, status=status.HTTP_400_BAD_REQUEST)

        if not provider:
            return Response({'message': 'Missing provider parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requested_date = datetime.strptime(string_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'message': 'Invalid date parameter'}, status=status.HTTP_400_BAD_REQUEST)

        closed_slots = TimeSlot.objects.filter(
            provider=provider,
            start_time__date=requested_date,
            is_available=False
        )

        response_data = TimeSlotSerializer(closed_slots, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)
