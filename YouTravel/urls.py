from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('YouTravel.common.urls')),
                  path('trips/', include('YouTravel.trips.urls')),
                  path('account/', include('YouTravel.accounts.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
