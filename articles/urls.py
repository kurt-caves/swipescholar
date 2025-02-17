from django.urls import path
from . import views
from .views import wikipedia_intro, new_title

urlpatterns = [
    path('api/wikipedia', wikipedia_intro, name='wikipedia_intro'),
    path('api/wiki', new_title, name='new_title'),
]