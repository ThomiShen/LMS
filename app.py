from flask import Flask, render_template, request,url_for,send_from_directory,jsonify,flash,redirect
from face import analyze_face,calculate_face_similarity  # 从face模块导入analyze_face函数
import os
from qizhi import get_most_similar_face
app = Flask(__name__)
# 定义存储上传图片的文件夹
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
STATIC_FOLDER = 'static/reference'
app.config['STATIC_FOLDER'] = STATIC_FOLDER
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取上传的图片文件
        image_file = request.files['image']
        #获取名字处理
        file_name = image_file.filename
        file_name = file_name.split('.')[0]

        # 保存图片到上传文件夹
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filename)
        face_shape1, temperament = get_most_similar_face(filename)
        # 重新打开文件以读取数据
        # 如果之后需要读取文件内容，可以这样做：
        with open(filename, 'rb') as f:
            image_data = f.read()
        # 获取图片的 URL
        image_url = url_for('static', filename=os.path.join('uploads', image_file.filename))
        print("Image URL:", image_url)
        # 调用analyze_face函数分析人脸
        face_features = analyze_face(image_data)
        # Get selected reference images
        selected_refs = request.form.getlist('reference')
        ref_image_paths = [os.path.join(app.config['STATIC_FOLDER'], ref) for ref in selected_refs]
        # similarity=calculate_face_similarity(filename,ref_image_paths)
        # 调用我们的函数
        # 提取分析结果并显示
        name = file_name
        age = face_features['age']
        beauty = face_features['beauty']
        gender = face_features['gender']['type']
        face_shape = face_features['face_shape']['type']
        glasses = face_features['glasses']['type']
        glasses_translation = {
            "none": "无眼镜",
            "common": "普通眼镜",
            "sun": "太阳眼镜"
        }
        glasses=glasses_translation[glasses]
        emotion_translation = {
            "angry": "生气气的人",
            "disgust": "抖S",
            "fear": "小胆子",
            "happy": "喜悦小天使",
            "sad": "忧伤感",
            "surprise": "惊呆呆",
            "neutral": "高冷的人",
            "grimace": "爱说笑的ren"
        }

        emotion = face_features['emotion']['type']
        emotion=emotion_translation[emotion]
        score = round(beauty , 2)
        return render_template('result.html', name=name,age=age, score=score, gender=gender, face_shape=face_shape1,image_url=image_url,temperament=temperament,glasses=glasses,emotion=emotion)

    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
