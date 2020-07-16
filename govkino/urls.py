from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('movies/', include('movie.urls')),
    path('events/', include('event.urls'))
]
