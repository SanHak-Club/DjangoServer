from django.urls import path
from . import views
from .views import *
from .models import *


app_name = 'cad'


# urlpatterns = [
#     path('cad/tfidf/', CadTfidf.as_view()),
#     path('cadsimilarity/<str:id>/', CadSimilarityView.as_view(), name='cadsimilarity'),
#     path('cad/updateCNN/', UpdateCNNClassification.as_view(), name='download_files'),
# ]

urlpatterns = [
    path('cad/tfidf/', CadTfidf.as_view()),
    path('totalsimilarity/<str:id>/', CadTotalSimilarityView.as_view(), name='cad_total_similarity'),
    path('labelsimilarity/<str:id>/', CadLabelSimilarityView.as_view(), name='cad_label_similarity'),
    path('cad/updateCNN/', UpdateCNNClassification.as_view(), name='download_files'),
]