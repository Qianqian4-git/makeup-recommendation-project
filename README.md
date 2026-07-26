# README.md

# 妆容推荐项目

该项目旨在通过分析用户上传的自拍照，推荐合适的妆容。项目利用机器学习技术，分析脸型、眼型及其他样貌特征，以提供个性化的妆容建议。

## 项目结构

- **data/**: 存放数据的文件夹
  - **raw/**: 原始数据，包括用户上传的自拍照和相关标签
  - **processed/**: 处理后的数据，包括清洗和特征提取后的数据集
  - **README.md**: 描述数据集的内容和结构

- **notebooks/**: Jupyter Notebook文件夹
  - **data_exploration.ipynb**: 数据探索和可视化
  - **feature_analysis.ipynb**: 特征重要性和分布分析
  - **model_evaluation.ipynb**: 模型性能评估

- **src/**: 源代码文件夹
  - **data_cleaning.py**: 数据清洗功能
  - **feature_extraction.py**: 特征提取功能
  - **model_training.py**: 模型训练功能
  - **recommendation.py**: 推荐逻辑功能
  - **utils/**: 辅助函数
    - **helpers.py**: 常见操作的辅助函数
  - **api/**: API入口文件
    - **app.py**: 处理用户上传的自拍照并返回推荐结果

- **tests/**: 测试文件夹
  - **test_data_cleaning.py**: 数据清洗模块的单元测试
  - **test_feature_extraction.py**: 特征提取模块的单元测试
  - **test_model_training.py**: 模型训练模块的单元测试
  - **test_recommendation.py**: 推荐模块的单元测试

- **requirements.txt**: 项目所需的Python库和依赖项

- **LICENSE**: 项目的许可证文件

## 使用指南

1. 克隆该项目到本地。
2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```
3. 上传自拍照并使用API获取妆容推荐。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求以帮助改进该项目。

## 许可证

该项目遵循MIT许可证。