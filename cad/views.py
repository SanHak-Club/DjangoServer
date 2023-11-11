from rest_framework import generics
from .serializers import *
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework.response import Response

class CadList(generics.ListAPIView):
    queryset = Cad.objects.all()
    serializer_class = CadSerializer

class CadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cad.objects.all()
    serializer_class = CadSerializer

class CadTfidf(generics.ListAPIView):
    serializer_class = CadSerializer

    def list(self, request, *args, **kwargs):
        vectorizer = TfidfVectorizer()
        queryset = Cad.objects.filter(author = "김광운")
        texts = [' '.join([cad.author, cad.mainCategory, cad.subCategory, cad.title, cad.index]) for cad in queryset]
        tfidf_matrix = vectorizer.fit_transform(texts)
        return Response(tfidf_matrix.todense())