# myapp/views.py

#from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.optimizers import Adam

import numpy as np


# 모델 로드
model = load_model('C:\\sanhak\\CNNmodel\\DWG_Classification_model_final.h5', compile=False)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

class_names = ['구성계통도','기타','배치도','상세도','케이블와이어다이어그램','평면도','포설직선도']

# 테스트 이미지 경로
test_image_path = 'C:\\Users\\wjdtm\\OneDrive\\바탕 화면\\test\\데이터\\테스트\\라벨링최종\\신라벨링\\train\\배치도\\[11ED05] 도면_우량국장비 배치도_수문관측소 통신시스템 개선 실시설계 용역.jpeg'

# 테스트 이미지 불러오기
img = image.load_img(test_image_path, target_size=(224, 224))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# 예측 수행
predictions = model.predict(img)

# 예측 결과를 클래스 이름으로 변환
class_index = np.argmax(predictions)
class_name = class_names[class_index] # 클래스 인덱스를 클래스 이름으로 변환
#class_labels = train_generator.class_indices
#predicted_class = [k for k, v in class_labels.items() if v == class_index][0]

print("예측된 클래스:", class_name)

    #return render(request, 'prediction_result.html', {'result': result})