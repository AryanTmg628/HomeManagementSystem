from .models import Task
from .serializers import (
    TaskSerailizer,
    UpdateTaskSerailizer
)


from utils.response.response import CustomResponse as cr 
from utils.exception.exception import CustomException as ce 


from django.http import Http404 


from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions  import IsAuthenticated
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)



# ! ViewSet For Task Model 
class TaskViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    

    def get_queryset(self):
        """
        Over riding the queryset
        """
        user_id=self.request.user.id
        return Task.objects.filter(
            user_id=user_id,
            status='COMPLETED'
        )
    

    def get_serializer_class(self):
        """
        Over riding the serailizer class the use different 
        serailizer for diferent method 
        """
        if self.request.method in ['PUT','PATCH']:
            return UpdateTaskSerailizer
        return TaskSerailizer
    

    def get_serializer_context(self):
        """
        Passing Context To Serailizer
        """
        user_id=self.request.user.id
        return {
            'user_id':user_id
        }
    

    def get_object(self):
        """
        Override get_object to handle non-existing objects
        """
        try:
            return super().get_object()
        except Http404:
            raise ce(
                message="Page Not found",
                status=HTTP_404_NOT_FOUND
            )


    def list(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        user=self.request.user 

        # ! For Listing Pending Tasks 
        pending_task=Task.objects.filter(
            user=user,
            status='PENDING',
        )
        pending_serializer=TaskSerailizer(
            pending_task,
            many=True
        )

        # ! For Listing Tasks InProgress 
        in_progress=Task.objects.filter(
            user=user,
            status='IN_PROGRESS'
        )
        in_progress_serializer=TaskSerailizer(
            in_progress,
            many=True
        )


        data={
            'COMPLETED':serializer.data,
            'PENDING':pending_serializer.data,
            'IN_PROGRESS':in_progress_serializer.data

        }
        return cr.success(
            data=data
        )
    

    def create(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return cr.success(
            status=HTTP_201_CREATED,
            message="New Task Has Been Added"
            )
    

    def retrieve(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return cr.success(
            data=serializer.data
        )


    def update(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return cr.success(
            data=serializer.data,
            message="Your Task Has Been Updated"
            )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your Task Has Been Deleted"
        )
