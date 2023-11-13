from django.urls import path
from . import views
from .views import *
from .models import *


app_name = 'cad'


urlpatterns = [
    path('cad/tfidf/', CadTfidf.as_view()),
    path('cadsimilarity/<str:id>/', CadSimilarityView.as_view(), name='cadsimilarity'),
    path('cad/updateCNN/', UpdateCNNClassification.as_view(), name='download_files'),
]