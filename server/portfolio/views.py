from utils.response.response import CustomResponse as cr
from utils.exception.exception import CustomException as ce
from .tasks import send_email_to_contacted_person
from .serializers import (
    PortfolioSerializer,
    EducationSerializer,
    SkillSerializer,
    ProjectSerializer,
    ContactSerializer
)
from .models import (
    Portfolio,
    Education,
    Skill,
    Project,
)

from django.db import transaction
from django.contrib.auth import get_user_model



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT
)



# ! Initializing User Model
User = get_user_model()



# ! ViewSet For Portfolio Model 
class PortfolioViewSet(ModelViewSet):
    queryset=Portfolio.objects.all()


    def get_serializer_class(self):
        """
        Adding Different Serailizer For Different actiona and 
        methods 
        """
        if self.action=="contact":
            return ContactSerializer
        return PortfolioSerializer



    # ! Custom Action 
    @action(
        detail=True,
        methods=['post'],
    )
    def contact(self, request, pk):
        """
        Custome Action To Contact A User
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ! Using transaction 
        with transaction.atomic():
            info=serializer.save()
            user=User.objects.get(id=pk)

            data={
                'fullname':info.fullname,
                'email':info.subject,
                'contact_no':info.contact_no,
                'subject':info.subject,
                'message':info.message,
                'date':info.date,
                'to_email':user.email
            }


            # ! Calling Celery Task Send Email  
            send_email_to_contacted_person.delay(data)

            return cr.success(
                message="You message has been recorded.You'll be contacted soon"
            )
     



# ! ViewSet For Users Education 
class EducationViewSet(ModelViewSet):
    serializer_class=EducationSerializer


    def get_queryset(self):
        """
        Overriding the base quesryset to filter the 
        users education by portfolio pk 
        """
        portfolio_pk=self.kwargs['portfolio_pk']

        return  Education.objects.filter(
            user_id=portfolio_pk
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        return {
            'portfolio_id':portfolio_pk
        }
    

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
        return cr.success(
            status=HTTP_201_CREATED,
            message="New Education Has Been Added"
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
            data=serializer.data,
            message="Your Education Has Been Updated"
            )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your Education Has Been Deleted"
            # message=f"{self.get_object()} Education Has Been Deleted"
        )


    


# ! ViewSet For Users Skill 
class SkillViewSet(ModelViewSet):
    serializer_class=SkillSerializer


    def get_queryset(self):
        """
        Overriding the base quesryset to filter the 
        users skills by portfolio pk 
        """
        portfolio_id=self.kwargs['portfolio_pk']
        
        return Skill.objects.filter(
            user_id=portfolio_id
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        return {
            'portfolio_id':portfolio_pk
        }
    

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
        return cr.success(
            status=HTTP_201_CREATED,
            message="New SKill Has Been Added"
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
            data=serializer.data,
            message="Your Skill Has Been Updated"
            )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your SKill Has Been Deleted"
        )




# ! ViewSet For Users Project 
class ProjectViewSet(ModelViewSet):
    serializer_class=ProjectSerializer

    def get_queryset(self):
        """
        Overriding the base quesryset to filter the 
        users project by portfolio pk 
        """
        portfolio_id=self.kwargs['portfolio_pk']
        
        return Project.objects.filter(
            user_id=portfolio_id
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        
        return {
            'portfolio_id':portfolio_pk
        }
    

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
        return cr.success(
            status=HTTP_201_CREATED,
            message="New  Project Has Been Added"
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
            data=serializer.data,
            message="Your Project Has Been Updated"
            )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Over riding method for custom response  
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your Project Has Been Deleted"
        )


















