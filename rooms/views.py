from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer
from .models import Room


class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        paginator.page_size = 20
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)

        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room)
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
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if request.user != room.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(
                room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
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


@api_view(["GET"])
def room_search(request):
    paginator = OwnPagination()
    rooms = Room.objects.filter()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
