from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.decorators import validate_request
from orders.serializers.time_slot_serializer import CloseTimeSlotSerializer


class SlotView(APIView):
    permission_classes = [IsAuthenticated]

    @validate_request(CloseTimeSlotSerializer)
    def post(self, request):
        serializer = CloseTimeSlotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'message': 'Slot closed successfully',
        }, status=status.HTTP_200_OK)