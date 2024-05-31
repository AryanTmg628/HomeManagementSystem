from rest_framework_nested import routers
from .views import (
    PortfolioViewSet,
    EducationViewSet,
    SkillViewSet,
    ProjectViewSet
)

router=routers.DefaultRouter()
router.register('portfolio',PortfolioViewSet,basename='portfolio')


portfolio_router=routers.NestedDefaultRouter(router,'portfolio',lookup='portfolio')
portfolio_router.register('educations',EducationViewSet,basename='portfolio_education')
portfolio_router.register('skills',SkillViewSet,basename='portfolio_skill')
portfolio_router.register('projects',ProjectViewSet,basename='portfolio_project')


urlpatterns = router.urls+ portfolio_router.urls 
