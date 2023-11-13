from rest_framework import generics
from .serializers import CadSerializer
from .models import Cad
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework.response import Response
import boto3
import os
import json
from .CNN import updateCNNClassification
from django.http import HttpResponse
#from rest_framework.views import View
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from decouple import config
from urllib.parse import urlparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class CadList(generics.ListAPIView):
    queryset = Cad.objects.all()
    serializer_class = CadSerializer


class CadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cad.objects.all()
    serializer_class = CadSerializer


class CadTfidf(generics.ListAPIView):
    serializer_class = CadSerializer

    def get_queryset(self):
        return Cad.objects.all()
    
    def list(self, request, *args, **kwargs):
        vectorizer = TfidfVectorizer()
        queryset = list(self.get_queryset())
        texts = [' '.join([cad.author, cad.mainCategory, cad.subCategory, cad.title, cad.index]) for cad in queryset]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # tfidf_matrix를 리스트로 변환
        tfidf_list = tfidf_matrix.todense().tolist()

        # queryset에 있는 각 Cad 객체의 tfidf 필드를 업데이트
        for cad, tfidf_values in zip(queryset, tfidf_list):
            cad.tfidf = json.dumps(tfidf_values)
            cad.save(update_fields=['tfidf']) #########

        return Response(tfidf_list)  # tfidf_list를 반환
    
def decrypt_s3_url(s3_url, key, iv):
        # Base64 디코딩
        encrypted = base64.b64decode(s3_url)
        # AES cipher 객체 생성
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        # 복호화
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode()
        
def get_s3_object_key(s3_url):
    if isinstance(s3_url, bytes):
        s3_url = s3_url.decode('utf-8')
    parsed = urlparse(s3_url)
    return parsed.path.lstrip('/')
    

class UpdateCNNClassification(generics.RetrieveAPIView):
    def post(self, request):
        return self.DownloadS3Files(request)
    
    def DownloadS3Files(self, request):
        # URL 요청에서 mainCategory 값을 가져옵니다.
        data = json.loads(request.body.decode('utf-8'))
        main_category = data.get('mainCategory')
        # main_category = request.POST.get('mainCategory')

        # boto3 client 생성
        s3 = boto3.client('s3', 
                          aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                          aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

        # 암호화에 사용한 키와 초기화 벡터
        key = config('AES_KEY')
        iv = config('AES_IV')  

        # mainCategory가 main_category인 Cad 객체 조회
        cads = Cad.objects.filter(mainCategory=main_category)

        for cad in cads:
            # S3 URL 복호화하여 파일 이름 얻기
            s3_url = decrypt_s3_url(cad.s3Url, key, iv)
            print(s3_url)
            file_name = get_s3_object_key(s3_url)
            # 버킷 이름과 key 설정
            bucket_name = config('AWS_STORAGE_BUCKET_NAME')

            # 로컬에 저장할 파일 경로 생성
            local_file_path = os.path.join('cad', file_name)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            # S3에서 파일 다운로드
            s3.download_file(bucket_name, file_name, local_file_path)
            updateCNNClassification(local_file_path, s3_url)
        return HttpResponse("Files downloaded successfully")
    
    


class CadSimilarityView(generics.RetrieveAPIView):
    serializer_class = CadSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Cad.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs.get(self.lookup_url_kwarg)
        target_cad = Cad.objects.get(_id=id)
        target_tfidf = np.array(json.loads(target_cad.tfidf)).reshape(1, -1)

        all_cads = self.get_queryset()
        tfidf_list = []
        for cad in all_cads:
            tfidf_values = json.loads(cad.tfidf)
            tfidf_list.append(tfidf_values)

        tfidf_matrix = np.array(tfidf_list)
        similarities = cosine_similarity(target_tfidf, tfidf_matrix).flatten()

        # 각 Cad 객체와의 유사도를 저장합니다.
        cad_similarities = [(cad._id, similarity) for cad, similarity in zip(all_cads, similarities)]

        # 유사도가 높은 순으로 정렬합니다.
        sorted_cad_similarities = sorted(cad_similarities, key=lambda x: x[1], reverse=True)

        # 상위 5개의 Cad 객체의 id를 가져옵니다.
        top_5_cad_ids = [cad_id for cad_id, similarity in sorted_cad_similarities[:5]]

        # 상위 5개의 Cad 객체의 id를 반환합니다.
        print(Response(top_5_cad_ids))
        print(top_5_cad_ids)
        
        print("HIHI")
        return Response(top_5_cad_ids)