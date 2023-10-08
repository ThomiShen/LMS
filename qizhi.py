import face_recognition
absolute_path = "/Users/thomi/PycharmProjects/untitled/LoveManagementSystem3/static/"
# 存储前5张和后5张图片的face_encoding
face_images_1 = [face_recognition.load_image_file(f"{absolute_path}reference/大美女{i}.jpg") for i in range(1, 6)]
face_encodings_1 = [face_recognition.face_encodings(img)[0] for img in face_images_1]

face_images_2 = [face_recognition.load_image_file(f"{absolute_path}reference/气质{i}.jpg") for i in range(1, 6)]
face_encodings_2 = [face_recognition.face_encodings(img)[0] for img in face_images_2]

def get_most_similar_face(image_file):
    # 加载上传的图片
    up_image = face_recognition.load_image_file(image_file)
    up_encoding = face_recognition.face_encodings(up_image)[0]

    # 获取与上传图片的距离
    distances_1 = face_recognition.face_distance(face_encodings_1, up_encoding)
    distances_2 = face_recognition.face_distance(face_encodings_2, up_encoding)

    # 找到距离最小的图片索引
    index_1 = distances_1.argmin()
    index_2 = distances_2.argmin()

    # 根据索引获取脸型和气质
    face_shape = ["圆脸型", "卵圆形脸型", "心形脸型", "长脸型", "方脸型"][index_1]
    temperament = ["知性、优雅", "性感、活力", "高贵、淑女", "清纯、娇媚", "少女、甜美"][index_2]

    return face_shape, temperament
