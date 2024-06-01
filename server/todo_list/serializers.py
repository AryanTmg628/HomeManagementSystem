from .models import Task
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer



# ! Serializer For Task Model
class TaskSerailizer(ModelSerializer):
    class Meta:
        model=Task
        fields=[
            'id',
            'title',
            'description',
            'status',
            'created_at',
            'updated_at'
        ]


    def create(self, validated_data):
        """
        Overriding the create method 
        """
        user_id=self.context['user_id']
        return Task.objects.create(
            user_id=user_id,
            **validated_data
        )
    



# ! Serailizer For Updating Task 
class UpdateTaskSerailizer(ModelSerializer):
    class Meta:
        model=Task
        fields=[
            'title',
            'description',
            'status',
        ]