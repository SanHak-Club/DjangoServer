from django.urls import path
from . import views
from .views import *
from .models import *


app_name = 'cad'


urlpatterns = [
    # path('tfidf/', Tfidf.s_veiw()),
    # path('similar/', get_similar_cad),
    path('cad/', CadList.as_view()),
    path('cad/<int:pk>/', CadDetail.as_view()),
    path('cad/tfidf/', CadTfidf.as_view()),
    path('totalsimilarity/<str:id>/', CadTotalSimilarityView.as_view(), name='cad_total_similarity'),
    path('labelsimilarity/<str:id>/', CadLabelSimilarityView.as_view(), name='cad_label_similarity'),
    path('download/', DownloadS3FilesView.as_view(), name='download_files'),
]