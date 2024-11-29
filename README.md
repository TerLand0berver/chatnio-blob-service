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

### Docker Compose 部署（推荐）

#### 方式一：使用预构建镜像（最简单）

1. 创建 `docker-compose.yml`:

```yaml
version: '3'

services:
  blob-service:
    image: teraccc/chatnio-blob-service:latest
    container_name: chatnio-blob-service
    ports:
      - "8009:8000"  # 修改为你需要的端口
    volumes:
      - ./static:/app/static
    environment:
      - STORAGE_TYPE=local
      - LOCAL_STORAGE_DOMAIN=https://your-domain.com  # 替换为你的域名
      - MAX_FILE_SIZE=10
      - PDF_MAX_IMAGES=10
      - CORS_ALLOW_ORIGINS=*
      - API_RESPONSE_FORMAT={"code":200,"message":"success","data":"$DATA"}
    restart: unless-stopped
    user: "1000:1000"
```

#### 方式二：本地构建（用于开发或自定义）

1. 创建 `docker-compose.yml`:

```yaml
version: '3'

services:
  blob-service:
    build: .
    container_name: chatnio-blob-service
    ports:
      - "8009:8000"
    volumes:
      - ./static:/app/static
    environment:
      - STORAGE_TYPE=local
      - LOCAL_STORAGE_DOMAIN=https://your-domain.com
      - MAX_FILE_SIZE=10
      - PDF_MAX_IMAGES=10
      - CORS_ALLOW_ORIGINS=*
      - API_RESPONSE_FORMAT={"code":200,"message":"success","data":"$DATA"}
    restart: unless-stopped
    user: "1000:1000"
```

2. 启动服务：

```bash
docker-compose up -d
```

3. 停止服务：

```bash
docker-compose down
```

### 快速命令行部署

如果不想使用 docker-compose，也可以直接使用 docker 命令：

```bash
docker run -d \
  --name chatnio-blob-service \
  -p 8009:8000 \
  -v ./static:/app/static \
  -e STORAGE_TYPE=local \
  -e LOCAL_STORAGE_DOMAIN=https://your-domain.com \
  -e MAX_FILE_SIZE=10 \
  -e PDF_MAX_IMAGES=10 \
  -e CORS_ALLOW_ORIGINS=* \
  teraccc/chatnio-blob-service:latest
```

### 环境变量配置

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| STORAGE_TYPE | 存储类型 | common | local, s3, tg |
| LOCAL_STORAGE_DOMAIN | 本地存储域名 | - | https://example.com |
| MAX_FILE_SIZE | 最大文件大小(MB) | -1 | 10 |
| CORS_ALLOW_ORIGINS | CORS 允许域名 | * | https://example.com |
| PDF_MAX_IMAGES | PDF最大图片数 | 10 | 20 |
| API_RESPONSE_FORMAT | API响应格式 | - | {"code":200,"message":"success","data":"$DATA"} |

#### 重要说明:
- 使用本地存储时，`LOCAL_STORAGE_DOMAIN` 应设置为您的域名（如果使用反向代理）
- 如果使用反向代理（如 Nginx），`LOCAL_STORAGE_DOMAIN` 不需要包含端口号
- 文件上传后的URL格式将是：`${LOCAL_STORAGE_DOMAIN}/static/filename.ext`
- 所有上传的文件都存储在 `static` 目录中
- 文件名使用 MD5 哈希值生成，保证唯一性

### 存储配置示例

#### 本地存储 (Local Storage)
```env
STORAGE_TYPE=local
LOCAL_STORAGE_DOMAIN=https://your-domain.com
```

#### S3 存储
```env
STORAGE_TYPE=s3
S3_ENDPOINT=https://s3.amazonaws.com
S3_BUCKET=your-bucket
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
```

#### Telegram 存储
```env
STORAGE_TYPE=telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

#### Alist 存储
```env
STORAGE_TYPE=alist
ALIST_DOMAIN=https://your-alist-domain
ALIST_USERNAME=your-username
ALIST_PASSWORD=your-password
ALIST_PATH=/path/to/store
```

### API 使用示例

#### 上传文件
```bash
curl -X POST http://localhost:8009/upload \
     -F "file=@example.pdf" \
     -F "save_all=true"
```

#### 更新配置
```bash
curl -X POST http://localhost:8009/config \
     -H "Content-Type: application/json" \
     -d '{"storage_type": "local", "max_file_size": 10}'
```

### 配置优先级
1. Web 配置界面 (/config)
2. 环境变量
3. 默认值

### 最佳实践
1. 总是设置 `MAX_FILE_SIZE` 限制上传文件大小
2. 在生产环境中配置具体的 `CORS_ALLOW_ORIGINS`
3. 使用非 root 用户运行容器（已在配置中设置）
4. 定期清理 static 目录中的过期文件
5. 在反向代理配置中添加适当的缓存头

### 常见问题
1. 文件上传失败
   - 检查文件大小是否超过限制
   - 确认存储配置是否正确
   - 查看容器日志获取详细错误信息

2. 无法访问上传的文件
   - 确认 `LOCAL_STORAGE_DOMAIN` 配置正确
   - 检查反向代理配置
   - 验证文件权限是否正确

3. CORS 错误
   - 检查 `CORS_ALLOW_ORIGINS` 配置
   - 确认前端域名是否在允许列表中
   - 查看浏览器控制台获取具体错误

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

### 配置热重载

本服务支持配置热重载，您可以通过以下方式动态更新配置：

1. Web 界面配置 (`/config`)
   - 直接在 Web 界面修改配置
   - 修改会立即生效，无需重启容器

2. 配置文件修改
   - 编辑 `config.json` 文件
   - 通过 API 更新配置：
     ```bash
     curl -X POST http://localhost:8000/api/config \
       -H "Content-Type: application/json" \
       -d '{"storage_type": "local", "max_file_size": 10}'
     ```

支持热重载的配置项：
- 存储配置（storage_type 及相关配置）
- API 响应格式
- CORS 设置
- 文件大小限制
- PDF 处理配置
- OCR 和语音识别配置

> 注意：某些配置的更改（如存储类型）可能会影响到正在处理的请求，建议在低负载时进行更改。

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
