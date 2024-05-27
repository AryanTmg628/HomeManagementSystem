from utils.response.response import CustomResponse as cr
from utils.exception.exception import CustomException as ce
from .serializers import (
    PortfolioSerializer,
    EducationSerializer,
    SkillSerializer,
    ProjectSerializer
)
from .models import (
    Portfolio,
    Education,
    Skill,
    Project,
)

from rest_framework.viewsets import ModelViewSet




# ! ViewSet For Portfolio Model 
class PortfolioViewSet(ModelViewSet):
    queryset=Portfolio.objects.all()
    http_method_names=['retrieve','patch']
    serializer_class=PortfolioSerializer  




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
            portfolio_id=portfolio_pk
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        return {
            'portfolio_id':portfolio_pk
        }
    



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
            portfolio_id=portfolio_id
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        return {
            'portfolio_id':portfolio_pk
        }




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
            portfolio_id=portfolio_id
        )
    

    def get_serializer_context(self):
        """
        Passing context to serailizer
        """
        portfolio_pk=self.kwargs['portfolio_pk']
        
        return {
            'portfolio_id':portfolio_pk
        }

















