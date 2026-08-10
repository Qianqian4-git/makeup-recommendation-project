🧾 Klea 美妆助手 - 前端项目结构说明
一、技术栈概览
类别	技术	版本	用途
框架	Vue 3	^3.5.13	渐进式 JavaScript 框架（组合式 API）
构建工具	Vite	^6.2.0	极速开发服务器与构建工具
状态管理	Pinia	^2.3.1	全局状态管理（用户、推荐、聊天）
CSS 框架	Tailwind CSS	^3.4.17	原子化 CSS，实现 Apple 风格界面
开发语言	JavaScript (ES6+)	-	逻辑编写
持久化	localStorage	-	本地存储历史记录与用户偏好
二、项目目录结构
text
frontend/
├── public/
│   └── images/
│       ├── bg/                      # 卡片背景装饰图
│       │   ├── explore-bg.jpg
│       │   ├── recommend-bg.jpg
│       │   ├── ai-bg.jpg
│       │   └── report-bg.jpg
│       └── makeup/                  # 妆容推荐展示图（需与映射表对应）
│           ├── natural_nude.jpg
│           ├── korean_glow.jpg
│           ├── japanese_salty.jpg
│           └── ...（更多妆容图片）
├── src/
│   ├── api/                         # 后端接口请求封装
│   │   ├── predict.js               # POST /predict 上传图片
│   │   └── chat.js                  # POST /api/chat 发送消息（普通模式）
│   ├── components/                  # Vue 组件库
│   │   ├── LeftNav.vue              # 左侧导航栏（工作台/历史/对话/我的）
│   │   ├── UploadModal.vue          # 上传自拍弹窗（含图片压缩为 Base64）
│   │   ├── HistoryModal.vue         # 历史详情弹窗（左右分栏显示自拍+妆容图）
│   │   ├── AllHistoryModal.vue      # 全部历史记录（按日期分组、折叠、多选删除）
│   │   └── ChatDrawer.vue           # 完整对话抽屉（右侧滑出）
│   ├── stores/                      # Pinia 状态管理
│   │   └── recommend.js             # 推荐记录状态（当前推荐 + 历史列表，持久化到 localStorage）
│   ├── utils/                       # 工具函数库
│   │   └── makeupImages.js          # 妆容图片映射（中文名 → 英文文件名）
│   ├── App.vue                      # 根组件（主布局：左导航 + 右滚动内容）
│   ├── main.js                      # 应用入口（挂载 Pinia 和 App）
│   └── style.css                    # 全局样式（Tailwind 指令 + 自定义滚动条）
├── index.html                       # HTML 模板
├── package.json                     # 依赖管理
├── tailwind.config.js               # Tailwind 配置（Apple 风格主题）
├── postcss.config.js                # PostCSS 配置
└── vite.config.js                   # Vite 配置（含代理解决跨域）
三、核心文件功能详解
1. App.vue —— 主布局与业务枢纽
左侧：固定导航栏（LeftNav），用于滚动定位。

右侧：长滚动内容区，自上而下包含：

顶部问候：打招呼 + “问问 Klea” 快捷跳转按钮。

第一行卡片（2列）：

左：开始探索（点击打开 UploadModal，上传后右侧显示自拍缩略图）。

右：推荐妆容（展示 store.current 分析结果，若无则显示“今日推荐”）。

第二行卡片（3列）：

左：AI 引擎（静态信息：14项特征 + 200K训练）。

右：分析报告（展示脸型/色号/妆容方向三小块）。

妆容历史：横向滚动显示最近5条，每条悬停显示删除按钮（×），点击卡片打开 HistoryModal。底部“查看全部”打开 AllHistoryModal。

与 Klea 聊聊：预览区 + 输入框 + “展示完整对话”（打开 ChatDrawer）。

模态管理：统一控制 UploadModal、HistoryModal、AllHistoryModal、ChatDrawer 的显隐。

2. components/LeftNav.vue —— 左侧导航栏
固定宽度（w-20），含 Logo（K）和 4 个导航项（工作台、历史、对话、我的）。

点击导航：通过 scrollIntoView 平滑滚动到右侧对应区域（基于 id）。

底部：用户头像（林）。

3. components/UploadModal.vue —— 上传自拍弹窗
交互：点击/拖拽上传图片，预览原始图片。

核心逻辑：

调用 resizeImage 将图片压缩为 200x200 的 JPEG（质量 60%），生成 Base64 缩略图。
调用后端 /predict 接口获取分析结果。
将结果 + Base64 缩略图存入 recommend store，并持久化到 localStorage。
限制：防止 localStorage 溢出（单张缩略图约 20~40KB）。

4. components/HistoryModal.vue —— 历史详情弹窗（毛玻璃风格）
布局：左右分栏（左：用户自拍，右：妆容推荐图）。

内容：展示妆容名、日期、脸型、肤色、色号、匹配度进度条、完整分析理由（reason）。

图片：自拍使用 record.imageBase64，妆容图使用 getMakeupImagePath 映射路径。

关闭：点击 ✕ 或外部遮罩关闭。

5. components/AllHistoryModal.vue —— 全部历史记录（高级管理）
分组与折叠：按 dateStr（如“2026年8月10日”）分组，点击日期头部可折叠/展开该组。

双模式交互：

普通模式：卡片悬停显示删除按钮（×），点击单条删除。

多选模式：点击头部“多选”进入，显示复选框，支持：

单张卡片勾选。

日期组头部圆形全选按钮（选中该组所有卡片）。

顶部“全选”按钮（选中全部）。

“删除 (n)”批量删除，带二次确认。

数据同步：删除后自动更新 store.history 和 localStorage，若删除当前推荐则清空 store.current。

6. components/ChatDrawer.vue —— 完整对话抽屉
滑出效果：从右侧滑入，覆盖主内容，左侧导航保持可见。

功能：

消息列表（用户蓝色气泡，AI 灰色气泡）。

流式输出占位（“正在输入...”动画）。

底部固定输入框，支持 Enter 发送。

当前状态：使用普通请求（非流式），后续可升级为 SSE 流式接收。

7. stores/recommend.js —— 推荐与历史状态管理
State：

current：当前展示的推荐结果（对象）。

history：所有历史记录数组（按时间倒序）。

Actions：

addRecord(record)：添加到历史头部（unshift），限制最多保存 20 条（防止存储溢出），并持久化。

clear()：清空所有数据。

持久化：基于 localStorage，键名为 klea_history_guest（后续可扩展为 klea_history_${userId}）。

8. utils/makeupImages.js —— 妆容图片映射表
功能：将后端返回的中文妆容名（如“自然裸妆”）映射到实际的图片文件名（如 natural_nude.jpg）。

导出函数：getMakeupImagePath(name)，返回图片路径（如 /images/makeup/natural_nude.jpg）。

维护：新增妆容时只需在此文件中添加一行映射，所有组件自动生效。

四、数据流与核心交互逻辑
用户上传自拍 → 获取推荐 → 展示
用户在“开始探索”卡片或“添加新自拍”处点击 → 打开 UploadModal。

选择图片 → 压缩为 Base64 → 调用 /predict。

后端返回 { makeup, reason, face_shape, skin_tone, shade, match, features }。

前端构造完整记录（含 Base64 缩略图）→ 存入 recommend store → 更新界面（推荐卡片、分析报告、历史列表）。

历史记录自动保存到 localStorage，刷新页面不丢失。

查看历史详情
主页或全部历史模态中点击任意历史卡片 → 触发 openHistoryModal(item)。

弹出 HistoryModal，传入 item 数据。

弹窗左右分栏展示自拍与妆容图，并展示脸型、肤色、色号、匹配度、分析理由。

删除历史记录
单条删除：主页卡片悬停 × 按钮 或 全部历史普通模式悬停 × 按钮 → 确认删除。

批量删除：全部历史模态 → 点击“多选” → 勾选目标卡片 → 点击“删除 (n)” → 确认删除。

五、启动与构建命令
bash
# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
注意：开发环境下 Vite 已配置代理（/predict 和 /api 转发至 http://127.0.0.1:8000），确保后端服务已启动。