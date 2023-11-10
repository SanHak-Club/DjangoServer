from django.urls import path
from . import views
from .views import *
from .models import *


app_name = 'cad'


urlpatterns = [
    path('tfidf/', get_similar_cad),
    path('similar/', get_similar_cad),
]