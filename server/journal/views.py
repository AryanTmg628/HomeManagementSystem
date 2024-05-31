from .models import Journal,JournalImage
from .serailizers import JournalSerailizer,JournalImageSerailizer

from utils.response.response import CustomResponse as cr 
from utils.exception.exception import CustomException as ce

from django.http import Http404 


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)



# ! ViewSet For Journal
class JournalViewSet(ModelViewSet):
    serializer_class=JournalSerailizer
    permission_classes=[IsAuthenticated]

    
    def get_queryset(self): 
        journal=(
            Journal.objects.filter(
                user=self.request.user
                )
                .select_related('user')
                .prefetch_related('images')
                .order_by('date')
            )
        
        return journal


    def get_serializer_context(self):
        return {
            'user_id':self.request.user.id
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
        return cr.success(
            data=serializer.data
            )


    def create(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return cr.success(
            message="Journal Successfully Created",
            data=serializer.data,
            status=HTTP_201_CREATED
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
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return cr.success(
            message="Journal Updated",
            data=serializer.data
        )


    def destroy(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            message="Journal Successfully Deleted ",
            status=HTTP_204_NO_CONTENT
            )
    



# ! ViewSet For Journal Images
class JournalImageViewSet(ModelViewSet):
    serializer_class=JournalImageSerailizer
    permission_classes=[IsAuthenticated]
    http_method_names=['get','head','options']


    def get_queryset(self):
        journal_pk=self.kwargs['journal_pk']

        if not Journal.objects.filter(id=journal_pk).exists():
            raise ce(
                message="Page Not found",
                status=HTTP_404_NOT_FOUND
            )

        journal_images=JournalImage.objects.filter(
            journal_id=journal_pk
        )
        return journal_images
    

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
        return cr.success(
            data=serializer.data
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








    


    


