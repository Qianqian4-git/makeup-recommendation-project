import cv2
import numpy as np

def extract_features(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像，请检查路径。")

    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用Haar级联分类器检测面部特征
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    features = []

    for (x, y, w, h) in faces:
        # 提取脸型特征
        face_shape = (w, h)
        features.append({'face_shape': face_shape})

        # 提取眼型特征
        roi_gray = gray_image[y:y+h, x:x+w]
        eyes = eyes_cascade.detectMultiScale(roi_gray)
        eye_shapes = [(ex, ey, ew, eh) for (ex, ey, ew, eh) in eyes]
        features[-1]['eye_shapes'] = eye_shapes

    return features

def preprocess_features(features):
    # 将提取的特征转化为模型可用的特征向量
    feature_vector = []
    for feature in features:
        face_shape = feature['face_shape']
        eye_shapes = feature['eye_shapes']
        
        # 将脸型和眼型特征转化为向量
        feature_vector.append([face_shape[0], face_shape[1], len(eye_shapes)])

    return np.array(feature_vector)