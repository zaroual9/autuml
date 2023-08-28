
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autouml_app.urls')),
    path('accounts/', include('allauth.urls')),  # Add this line
    path('uml/', include('autouml_app.urls')),   # Your existing app URL
]

# add at the last
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
