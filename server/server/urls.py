
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/auth/',include('authentication.urls')),
    path('api/',include('journal.urls')),
    path('api/',include('portfolio.urls')),
    path('api/',include('todo_list.urls')),
]


# ! FOR MEADIA AND STATIC FILES IN DEVELOPMENT PHASE
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
