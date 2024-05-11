from rest_framework import serializers

from .models import DoorLock


class DoorLockSerializer(serializers.ModelSerializer):
    """
    Door lock serializer
    """

    class Meta:
        model = DoorLock
        fields = "__all__"

    def to_representation(self, instance):
        """
        run whenever we access serailizer.data and if the action is view it will remove the password
        """
        if "action" in self.context and self.context["action"] == "view":
            self.fields.pop("password", None)
        return super().to_representation(instance)
