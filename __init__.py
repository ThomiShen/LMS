from flask import Flask, render_template, request,url_for,send_from_directory,jsonify,flash,redirect
from face import analyze_face,calculate_face_similarity  # 从face模块导入analyze_face函数
import os
import math
def sigmoid_similarity(value):
    return 1 / (1 + math.exp(-10 * (value - 0.5)))
ref_image_paths = ['/Users/thomi/PycharmProjects/untitled/LoveManagementSystem/static/reference/大美女2.jpg','/Users/thomi/PycharmProjects/untitled/LoveManagementSystem/static/reference/大美女1.jpg']
up='/Users/thomi/PycharmProjects/untitled/LoveManagementSystem2/static/uploads/死胖子.JPG'
with open(up, 'rb') as f:
    image_data = f.read()
face_features=analyze_face(image_data)
beauty=face_features["beauty"]
print(beauty)
avg_similarity=calculate_face_similarity(up,ref_image_paths)
avg_similarity=round(avg_similarity,4)
#基于相似度高颜值和低颜值都在0.4-0.6之间因此要均匀分布0-1的分数应该处理为？
def scale_similarity(value):
    min_input = 0.4
    max_input = 0.6
    min_output = 0
    max_output = 1
    scaled_value = ((value - min_input) / (max_input - min_input)) * (max_output - min_output) + min_output
    return scaled_value

avg_similarity1=scale_similarity(avg_similarity)*100
if avg_similarity1<30:
    avg_similarity1=30
score=round(beauty*0.4+avg_similarity1*0.6,2)
# print(score)
avg_similarity1=sigmoid_similarity(avg_similarity)
print(avg_similarity1)