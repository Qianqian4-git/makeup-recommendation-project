from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from src.feature_extraction import extract_features
from src.recommendation import recommend_makeup

app = Flask(__name__)

# 配置上传文件的目录
UPLOAD_FOLDER = 'data/raw'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # 提取特征
    features = extract_features(file_path)

    # 推荐妆容
    recommendations = recommend_makeup(features)

    return jsonify({'recommendations': recommendations}), 200

if __name__ == '__main__':
    app.run(debug=True)