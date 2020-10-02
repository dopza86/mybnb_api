from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReadRoomSerializer, WriteRoomSerializer
from .models import Room


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room)
            return Response(room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):

        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if request.user != room.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = WriteRoomSerializer(
                room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(ReadRoomSerializer(room).data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if request.user != room.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response()

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)