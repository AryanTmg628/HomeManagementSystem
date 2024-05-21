from rest_framework_nested import routers
from .views import (
    JournalViewSet,
    JournalImageViewSet
)


router=routers.DefaultRouter()
router.register('journal',JournalViewSet,basename="journal")
journal_router=routers.NestedDefaultRouter(router,'journal',lookup='journal')
journal_router.register('images',JournalImageViewSet, basename='journal_image')


urlpatterns = router.urls+journal_router.urls
