from rest_framework import generics
from .serializers import CadSerializer
from .models import Cad
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework.response import Response
import boto3
import os
import json
from django.http import HttpResponse
from django.views import View
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from decouple import config
from urllib.parse import urlparse

class CadList(generics.ListAPIView):
    queryset = Cad.objects.filter(author="김광운")
    serializer_class = CadSerializer

class CadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cad.objects.all()
    serializer_class = CadSerializer


class CadTfidf(generics.ListAPIView):
    serializer_class = CadSerializer

    def get_queryset(self):
        return Cad.objects.filter(author="김광운")
    
    def list(self, request, *args, **kwargs):
        vectorizer = TfidfVectorizer()
        queryset = list(self.get_queryset())
        texts = [' '.join([cad.author, cad.mainCategory, cad.subCategory, cad.title, cad.index]) for cad in queryset]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # tfidf_matrix를 리스트로 변환
        tfidf_list = tfidf_matrix.todense().tolist()

        # queryset에 있는 각 Cad 객체의 tfidf 필드를 업데이트
        for cad, tfidf_values in zip(queryset, tfidf_list):
            cad.tfidf = json.dumps(tfidf_values)  # tfidf_values을 JSON 형식의 문자열로 변환하여 저장
            cad.save(update_fields=['tfidf'])

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

class DownloadS3FilesView(View):
    def get(self, request, *args, **kwargs):
        # boto3 client 생성
        s3 = boto3.client('s3', 
                          aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                          aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

        # 암호화에 사용한 키와 초기화 벡터
        key = config('AES_KEY')
        iv = config('AES_IV')  

        # author가 "김광운"인 Cad 객체 조회
        cads = Cad.objects.filter(author="김광운")

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

        return HttpResponse("Files downloaded successfully")