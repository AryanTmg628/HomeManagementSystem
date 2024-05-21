from .models import Journal,JournalImage
from utils.exception.exception import CustomException as ce 


from rest_framework import serializers
from django.db import transaction



# ! Serailizer For Journal Images 
class JournalImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model=JournalImage 
        fields=[
            'id',
            'image'
        ]




# ! Serailizer For Journal  
class JournalSerailizer(serializers.ModelSerializer):
    images=JournalImageSerailizer(many=True,read_only=True)
    user=serializers.StringRelatedField()
    upload_images=serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model=Journal
        fields=[
            'id',
            'title',
            'content',
            'date',
            'user',
            'images',
            'upload_images'
        ]


    def validate(self, attrs):
        date=attrs.get('date')
        user_id=self.context['user_id']

        journal=Journal.objects.filter(
            date=date,
            user_id=user_id
        )

        if journal.exists():
            return ce(
                message="You cannot create multiple journal for the same date"
            )

        return attrs


    def create(self, validated_data):
        """
        Over riding the create method to create Journal and 
        Journal Images at the same time 
        """
        try:
            with transaction.atomic():  
                uploaded_images=validated_data.pop('upload_images')

                user_id=self.context['user_id']
                
                journal=Journal.objects.create(
                    user_id=user_id,
                    **validated_data
                )

                list_of_journal_images=[
                    JournalImage(journal=journal, image=image)
                    for image in uploaded_images
                ]

                # ! Creating Journal Images Bulkly
                JournalImage.objects.bulk_create(list_of_journal_images)

            return journal
        except Exception as e :
            return ce(
                message=f"Some error occured while creating journal {e}"
            )
        

    def update(self, instance, validated_data):
        date=validated_data['date']
        user_id=self.context['user_id']

        journal=Journal.objects.filter(
            date=date,
            user_id=user_id
        )

        if journal.exists():
            return ce(
                message="Invalid Request You cannot have multiple journal for the same day"
            )
        
        return super().update(instance, validated_data)




