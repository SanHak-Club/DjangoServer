# myapp/views.py

#from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.optimizers import Adam
import PIL
import os
from .models import Cad
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from decouple import config

def encrypt_s3_url(s3_url, key, iv):
    # 패딩
    padded = pad(s3_url.encode(), AES.block_size)
    # AES cipher 객체 생성
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    # 암호화
    encrypted = cipher.encrypt(padded)
    # Base64 인코딩
    return base64.b64encode(encrypted).decode()

def updateCNNClassification(imageDir, s3_url):
    model = load_model(config('CNN_MODEL'), compile=False)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    class_names = ['구성계통도','기타','배치도','상세도','케이블와이어다이어그램','평면도','포설직선도']
    
    key = config('AES_KEY')
    iv = config('AES_IV')  

    s3_url = encrypt_s3_url(s3_url,key,iv)
    img = image.load_img(imageDir, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    # 예측 수행
    predictions = model.predict(img)
            # 예측 결과를 클래스 이름으로 변환
    class_index = np.argmax(predictions)
    class_name = class_names[class_index] # 클래스 인덱스를 클래스 이름으로 변환
            
    target_cad = Cad.objects.get(s3Url=s3_url)
    target_cad.CadLabel = class_name
    target_cad.save()