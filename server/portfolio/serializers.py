from .models import (
    Portfolio,
    Education,
    Skill,
    Project,
    Contact
)


from rest_framework import serializers



# ! Serializer For Users Education 
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Education
        fields=[
            'id',
            'institution_name',
            'degree',
            'date_from',
            'date_to',
        ]

    
    def create(self, validated_data):
        """
        Overriding the create method
        """
        user_id=self.context['user_id']

        return Education.objects.create(
            user_id=user_id,
            **validated_data
        )





# ! Serializer For Users Skills 
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=Skill
        fields=[
            'id',
            'icon',
            'name',
            'level'
        ]

    
    def create(self, validated_data):
        """
        Overriding the create method
        """
        user_id=self.context['user_id']

        return Skill.objects.create(
            user_id=user_id,
            **validated_data
        )




# ! Serializer For Project Serializer 
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=[
            'id',
            'title',
            'description',
            'live_link',
            'github_link',
        ]


    def create(self, validated_data):
        """
        Overriding the create method
        """
        user_id=self.context['user_id']

        return Project.objects.create(
            user_id=user_id,
            **validated_data
        )        




# ! Serializer For Contacting User 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=[
            'id',
            'fullname',
            'email',
            'subject',
            'message',
            'contact_no',
            'date'
        ] 




# ! Serializer For Users Portfolio 
class PortfolioSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    
    class Meta:
        model = Portfolio
        fields = [
            'pk',
            'user',
            'image',
            'description',
            'location',
            'instagram_link',
            'github_link',
            'contact_no'
        ]