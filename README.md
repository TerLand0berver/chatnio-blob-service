# 📦 Chat Nio Blob Service

> 一个功能强大的文件服务系统，为 Chat Nio 提供文件处理支持

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Deeptrain-Community/chatnio-blob-service)
[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/RWGFOH)

## 🎯 最新更新

### 2024 年主要更新
- 🆕 **新增存储支持**
  - Alist 存储集成
  - 支持更多 S3 兼容存储（如 Cloudflare R2）
  - Telegram CDN 存储优化
- 🔄 **API 响应格式增强**
  - 可自定义响应字段名称
  - 灵活的状态值配置
  - 支持内容包装选项
- 📝 **新增文件格式支持**
  - Markdown (.md) 文件处理
  - CSV (.csv) 文件解析
  - RTF (.rtf) 文档支持
- ⚙️ **配置系统升级**
  - 新增 Web 配置界面 (/config)
  - 运行时配置修改
  - 配置持久化支持

## ✨ 核心特性

- 🚀 **开箱即用**: 无需外部依赖，支持 Vercel/Render 一键部署
- 📄 **全面的文件支持**: 
  - 文档：PDF、Word、Excel、PowerPoint、Markdown、RTF
  - 媒体：图片、音频
  - 数据：CSV、文本文件
- 💾 **多样化存储方案**: 
  - 云存储：S3、Cloudflare R2、MinIO
  - CDN：Telegram CDN
  - 文件系统：Alist、本地存储
  - 内存：Base64
- 🎛️ **灵活配置**:
  - Web 配置界面
  - 动态配置更新
  - 自定义 API 响应
- 🔍 **增强功能**: 
  - OCR 图片文字识别
  - 语音转文本 (Azure Speech)
  - 批量文件处理

## 📋 文件格式支持

### 文档处理
- 📝 文本类
  - Markdown (.md) `新增`
  - RTF (.rtf) `新增`
  - 纯文本 (.txt, .log, .ini, .conf)
- 📊 数据类
  - CSV (.csv) `新增`
  - Excel (.xlsx, .xls)
- 📄 办公类
  - Word (.docx)
  - PowerPoint (.pptx)
  - PDF

### 媒体处理
- 🖼️ 图片
  - 常见格式：.jpg, .jpeg, .png, .gif, .bmp
  - OCR 文字提取 (需要 Paddle OCR API)
- 🎵 音频
  - 支持格式：.mp3, .wav, .m4a, .ogg
  - 语音转文本 (需要 Azure Speech)

## 🚀 快速开始

### Docker 部署

```bash
# 基础运行
docker run -p 8000:8000 teraccc/chatnio-blob-service

# 使用环境变量
docker run -p 8000:8000 \
  -e AZURE_SPEECH_KEY="your-key" \
  -e AZURE_SPEECH_REGION="your-region" \
  teraccc/chatnio-blob-service

# 使用本地存储时，需要挂载卷
docker run -p 8000:8000 \
  -v /path/to/static:/static \
  teraccc/chatnio-blob-service
```

## ⚙️ 配置说明

### 存储配置
支持多种存储后端，通过环境变量或 Web 配置界面配置：

1. **本地存储**
```bash
STORAGE_TYPE=local
STATIC_PATH=/path/to/static
```

2. **S3 兼容存储** (AWS S3, Cloudflare R2 等)
```bash
STORAGE_TYPE=s3
S3_BUCKET=your-bucket
S3_ENDPOINT=your-endpoint
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_REGION=your-region
```

3. **Telegram CDN**
```bash
STORAGE_TYPE=telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

4. **Alist 存储** `新增`
```bash
STORAGE_TYPE=alist
ALIST_URL=your-alist-url
ALIST_TOKEN=your-token
ALIST_PATH=/path/to/store
```

### 功能配置

1. **OCR 服务**
```bash
PADDLE_OCR_API=http://your-paddle-ocr-api
```

2. **语音转文本**
```bash
AZURE_SPEECH_KEY=your-key
AZURE_SPEECH_REGION=your-region
```

3. **API 响应格式** `新增`
```bash
# 示例配置
API_RESPONSE_FORMAT={
  "status_field": "code",
  "content_field": "data",
  "error_field": "message",
  "success_value": "success",
  "error_value": "error"
}
```

## 📝 API 文档

### 文件上传
**POST** `/upload`

请求参数：
| 参数 | 类型 | 说明 |
|------|------|------|
| file | File | 要上传的文件 |
| enable_ocr | Boolean | 是否启用 OCR (默认: false) |
| enable_vision | Boolean | 是否启用视觉处理 (默认: true) |
| save_all | Boolean | 是否保存所有文件 (默认: false) |

### 配置管理
**GET/POST** `/config`

Web 配置界面，支持在线修改所有配置项。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
