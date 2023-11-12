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
    path('download_s3_files/', DownloadS3FilesView.as_view(), name='download_s3_files'),
]