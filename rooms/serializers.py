from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Room, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("room",)


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    is_favs = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError(
                "Not enough time between changes")
        else:
            return data

    def get_is_favs(self, obj):
        request = self.context.get("request")
        if request is not None:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def create(self, validate_data):
        request = self.context.get("request")
        user = request.user
        room = Room.objects.create(**validate_data, user=user)
        return room
