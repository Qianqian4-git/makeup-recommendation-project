# Klea · AI 美妆助手

> 上传自拍照，AI 分析面部特征，推荐最适合你的妆容风格。

Klea 是一个基于深度学习的智能妆容推荐系统。它通过分析用户上传的自拍照，识别脸型、肤色、五官等 14 项面部特征，结合美妆专业规则，为用户提供个性化的妆容推荐。同时内置 AI 美妆顾问，可随时解答化妆相关问题。

## 核心功能

- **妆容推荐**：上传自拍照，AI 自动分析面部特征，输出妆容名称、推荐理由、脸型、肤色、色号、匹配度。
- **AI 美妆顾问**：基于通义千问大模型，支持多轮对话，可询问妆容步骤、产品推荐、场合搭配等。
- **上下文感知**：推荐结果自动注入对话上下文，AI 顾问能根据你的妆容推荐给出针对性建议。
- **个性化体验**：支持用户输入昵称，界面提供个性化问候。

## 技术架构

整体分为四层：

- **前端层**：单一 HTML 页面（Klea 品牌风格，含 CSS + JS）
- **API 层**：FastAPI，包含两个路由
  - `POST /predict`：妆容推荐
  - `POST /api/chat`：AI 对话
- **业务逻辑层**：`recommendation`（推荐服务）、`chat_service`（对话服务）、`context_store`（上下文存储）
- **模型层**：端到端 ResNet18（微调），输入 224×224 图片，输出 14 个面部属性（0/1）

### 技术栈

| 层级       | 技术                              |
| :--------- | :-------------------------------- |
| 前端       | HTML5 + CSS3 + JavaScript         |
| API 框架   | FastAPI                           |
| 深度学习   | PyTorch + torchvision（ResNet18） |
| 大语言模型 | 阿里云灵积（Qwen-Turbo）          |
| 部署       | Uvicorn                           |

## 项目结构

text

```
makeup-recommendation-project/
├── frontend/
│   └── index.html                # 前端页面
├── src/
│   ├── api/
│   │   ├── main.py               # FastAPI 应用入口
│   │   └── routers/
│   │       ├── predict.py        # POST /predict
│   │       └── chat.py           # POST /api/chat
│   ├── services/
│   │   ├── recommendation.py     # 妆容推荐服务
│   │   ├── chat_service.py       # AI 对话服务
│   │   └── context_store.py      # 上下文存储
│   ├── core/
│   │   └── config.py             # 统一配置
│   ├── utils/
│   │   └── feature_utils.py      # 特征提取工具
│   ├── config.py                 # TARGET_ATTRS 定义
│   ├── inference_end2end.py      # 模型推理
│   ├── recommendation_engine.py  # 推荐规则引擎
│   └── legacy/                   # 已弃用代码
├── models/
│   └── best_model_end2end.pth    # 模型权重
├── .env                          # 环境变量
├── requirements.txt              # Python 依赖
└── README.md
```



## 快速开始

**环境要求**：Python 3.10+，支持 Windows / macOS / Linux。

**1. 克隆项目**

bash

```
git clone https://github.com/Qianqian4-git/makeup-recommendation-project.git
cd makeup-recommendation-project
```



**2. 创建虚拟环境**

bash

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```



**3. 安装依赖**

bash

```
pip install -r requirements.txt
```



**4. 配置环境变量**

复制 `.env.example` 为 `.env`，填入以下内容：

env

```
API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
MODEL_SAVE_PATH=./models/best_model_end2end.pth
DEVICE=cpu
HOST=127.0.0.1
PORT=8000
```



> **注意**：AI 对话功能依赖阿里云灵积 API，请前往阿里云灵积控制台申请 API Key。

**5. 启动服务**

bash

```
python src/api/main.py
```



**6. 访问应用**

浏览器打开 `http://127.0.0.1:8000`

## API 文档

启动服务后，访问 `/docs` 查看自动生成的 Swagger 文档。

### POST /predict

上传图片，返回妆容推荐结果。

- **请求**：`multipart/form-data`，字段 `file`
- **响应示例**：

json

```
{
  "makeup": "韩系水光妆",
  "reason": "根据您的面部特征分析：您拥有标准的鹅蛋脸、柔和的弯眉、白皙的肤色...",
  "face_shape": "鹅蛋脸",
  "skin_tone": "冷白皮",
  "shade": "兰蔻 #01",
  "match": 92,
  "features": "标准的鹅蛋脸、柔和的弯眉、白皙的肤色、年轻有活力的状态",
  "filename": "photo.jpg"
}
```



### POST /api/chat

发送消息，AI 美妆顾问回复。

- **请求**：`application/x-www-form-urlencoded`，字段 `question`
- **响应示例**：

json

```
{
  "code": 200,
  "answer": "韩系水光妆适合日常通勤和约会场景..."
}
```



## 模型说明

**训练数据集**：CelebA（Large-scale CelebFaces Attributes Dataset），包含 202,599 张人脸图片、40 种属性标注。按身份划分训练集/测试集，确保同一人不跨集。

**模型架构**：

| 组件     | 说明                        |
| :------- | :-------------------------- |
| 主干网络 | ResNet18（ImageNet 预训练） |
| 全连接层 | 3 层（256 → 128 → 14）      |
| 训练方式 | 端到端微调                  |
| 输入尺寸 | 224 × 224                   |
| 输出     | 14 个面部属性（0/1）        |

**训练结果**：

| 指标            | 数值       |
| :-------------- | :--------- |
| 训练集规模      | 126,621 张 |
| 验证集规模      | 31,656 张  |
| 最佳验证 Loss   | 0.2786     |
| 测试集宏平均 F1 | 0.52+      |

系统可识别 14 项面部属性（脸型、眉形、眼型、鼻型、唇形、肤色等），作为妆容推荐的依据。

## 开发与训练

**重新训练模型**：

bash

```
python src/model_training_end2end.py
```



**模型评估**：

bash

```
python src/evaluate_end2end.py
```



**运行 API 服务**：

bash

```
python src/api/main.py
```



## 注意事项

- **API Key**：AI 对话功能需要在 `.env` 中配置 `API_KEY`，否则对话功能不可用。
- **模型文件**：`best_model_end2end.pth` 约 100+ MB，请确保磁盘空间充足。
- **首次启动**：ResNet18 权重会从 PyTorch 官方源下载，请确保网络通畅。
- **前端说明**：当前前端为单一 HTML 文件，后续可用 React/Vue 重写。

## 后续计划

- 前端框架迁移（React/Vue）
- 用户系统与妆容历史记录
- 支持更多妆容风格与精细化推荐
- 模型持续优化（全量数据训练）

## 许可证

本项目仅供学习与研究使用。

## 作者

GitHub: [Qianqian4-git](https://github.com/Qianqian4-git)

如有问题或建议，欢迎提交 Issue 或 Pull Request。