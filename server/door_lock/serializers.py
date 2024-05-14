from rest_framework import serializers

from .models import DoorLock


class DoorLockSerializer(serializers.ModelSerializer):
    """
    Door lock serializer
    """

    class Meta:
        model = DoorLock
        fields = "__all__"
