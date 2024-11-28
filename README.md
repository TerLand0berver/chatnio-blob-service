# 📦 Chat Nio Blob Service

> 一个功能强大的文件服务系统，为 Chat Nio 提供文件处理支持

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Deeptrain-Community/chatnio-blob-service)
[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/RWGFOH)

## ✨ 主要特性

- 🚀 **开箱即用**: 无需外部依赖，支持 Vercel/Render 一键部署
- 📄 **多文件格式**: 支持文本、PDF、Word、Excel、图片、音频等多种格式
- 💾 **多存储选项**: 支持 Base64、本地存储、S3、Cloudflare R2、MinIO、Telegram CDN 等
- 🔍 **OCR 支持**: 图片文字提取 (需要 Paddle OCR API)
- 🎵 **音频转换**: 音频转文本 (需要 Azure Speech to Text 服务)

## 📋 支持的文件类型

- 文本文件 (.txt, .log, .ini, .conf)
- Markdown文件 (.md)
- CSV文件 (.csv)
- RTF文档 (.rtf)
- Word文档 (.docx，不支持 .doc)
- PDF文件
- PowerPoint (.pptx，不支持 .ppt)
- Excel (.xlsx，支持 .xls)
- 图片 (需要视觉模型)
  - 支持格式：.jpg, .jpeg, .png, .gif, .bmp
- 音频 (需要 Azure Speech to Text 服务)
  - 支持格式：.mp3, .wav, .m4a, .ogg

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

### 源码部署

```bash
# 克隆项目
git clone --branch=main https://github.com/Deeptrain-Community/chatnio-blob-service
cd chatnio-blob-service

# 安装依赖
pip install -r requirements.txt

# 运行服务
uvicorn main:app

# 开发模式（热重载）
# uvicorn main:app --reload
```

## 📝 API 接口

### 文件上传

**POST** `/upload`

请求参数：
```json
{
    "file": "[file]",
    "enable_ocr": false,
    "enable_vision": true,
    "save_all": false
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| file | File | 要上传的文件 |
| enable_ocr | Boolean | 是否启用 OCR (默认: false) |
| enable_vision | Boolean | 是否启用视觉处理 (默认: true) |
| save_all | Boolean | 是否保存所有文件 (默认: false) |

响应格式（可配置）：
```json
{
  "status": true,           // 状态字段，名称可配置
  "type": "pdf",           // 类型字段，可选
  "content": "...",        // 内容字段，支持自定义包装
  "error": ""             // 错误字段，名称可配置
}
```

响应格式配置说明：
1. 字段名称：可自定义状态、类型、内容、错误等字段的名称
2. 状态值：可配置成功/失败的返回值（如 true/false, 1/0, "success"/"error" 等）
3. 类型字段：可选择是否包含在响应中
4. 内容包装：支持自定义内容字段的包装格式，例如：
   ```json
   {
     "status": "success",
     "content": {
       "text": "实际内容",
       "timestamp": "2024-01-20",
       "extra": "附加信息"
     }
   }
   ```

## ⚙️ 配置说明

### 基础配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| PDF_MAX_IMAGES | PDF 文件最大提取图片数 | 10 |
| MAX_FILE_SIZE | 最大上传文件大小(MiB) | -1 (无限制) |
| CORS_ALLOW_ORIGINS | CORS 允许的域名 | * |

### 动态配置

服务启动后，访问 `/config` 路径可以进入配置页面，支持在线修改以下配置：

- 基础配置（PDF最大图片数、最大文件大小、CORS设置等）
- 存储配置（支持切换和配置不同的存储方式）
- 功能配置（Azure Speech、OCR等服务配置）

所有配置都会自动保存，无需重启服务即可生效。

### 存储配置

支持多种存储方式：

1. **Base64 存储** (默认)
   - 无需额外配置
   - 适合无状态部署
   - 不支持直接 URL 访问

2. **本地存储**
   ```bash
   STORAGE_TYPE=local
   LOCAL_STORAGE_DOMAIN=http://your-domain.com
   ```

3. **S3 兼容存储** (AWS S3/Cloudflare R2/MinIO)
   ```bash
   STORAGE_TYPE=s3
   S3_ACCESS_KEY=your-access-key
   S3_SECRET_KEY=your-secret-key
   S3_BUCKET=your-bucket
   S3_REGION=your-region
   ```

4. **Telegram CDN**
   ```bash
   STORAGE_TYPE=tg
   TG_ENDPOINT=your-tgstate-endpoint
   TG_PASSWORD=your-password  # 可选
   ```

5. **Alist存储**
   ```bash
   STORAGE_TYPE=alist
   ALIST_ENDPOINT=http://your-alist-server:5244
   ALIST_USERNAME=your-username
   ALIST_PASSWORD=your-password
   ALIST_PATH=/blob  # 存储路径，默认为 /blob
   ```
   - 支持多种存储后端（本地、阿里云盘、OneDrive等）
   - 文件按日期自动分类存储
   - 支持文件直接访问

### 功能配置

1. **音频转换** (Azure Speech)
   ```bash
   AZURE_SPEECH_KEY=your-key
   AZURE_SPEECH_REGION=your-region
   ```

2. **OCR 支持**
   ```bash
   OCR_ENDPOINT=http://your-paddleocr-endpoint:8000
   ```

### 环境变量配置

如果你更倾向于使用环境变量进行配置，以下是所有支持的环境变量：

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
