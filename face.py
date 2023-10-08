import base64
import requests
import math
# 定义API Key和Secret Key
APP_ID = '40079341'     #ID短号
API_KEY = '0f5GrnbmAHsksnagaUDpFW3l'  #无规律很长
SECRET_KEY = 'P4MNGHY2m17X3QUUiOaFcxnqhcgSnCTL'   #无规律很长

# 获取access_token
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_KEY, SECRET_KEY)
response = requests.get(host)
access_token = response.json()['access_token']

# def scale_similarity(value):
#     min_input = 0.4
#     max_input = 0.6
#     min_output = 0
#     max_output = 1
#     scaled_value = ((value - min_input) / (max_input - min_input)) * (max_output - min_output) + min_output
#     return scaled_value

import face_recognition
def calculate_face_similarity(image_data, ref_images):
    # 加载图片并获取面部编码
    uploaded_image = face_recognition.load_image_file(image_data)
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]
    # Calculate similarity with the reference images
    similarities = []
    # 计算两个面部编码之间的欧氏距离
    for ref_image_path in ref_images:
        ref_image = face_recognition.load_image_file(ref_image_path)
        ref_encoding = face_recognition.face_encodings(ref_image)[0]
        face_distance = face_recognition.face_distance([ref_encoding], uploaded_encoding)[0]
        similarities.append(1 - face_distance)  # Convert distance to similarity
    avg_similarity=0
    for s in similarities:
        avg_similarity+=s
    avg_similarity=avg_similarity*100
    if avg_similarity < 60:
        avg_similarity = 60
    return  avg_similarity

def analyze_face(image_data):
    # 将图片文件转换为base64编码
    base64_data = base64.b64encode(image_data)

    # 调用百度API进行人脸识别
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {
        "image": base64_data,
        "image_type": "BASE64",
        "face_field": "age,beauty,expression,face_shape,gender,glasses,emotion,face_type,spoofing",
        "face_type": "LIVE"
    }
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    face_result = response.json()

    # 返回分析结果
    return face_result['result']['face_list'][0]
