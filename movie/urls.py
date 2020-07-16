from django.urls import path


from .views import MovieListView

urlpatterns = [
    path('', MovieListView.as_view(), name='get_movies')
]