# LangExtract AWS Lambda 服务

这是一个基于 AWS Lambda 和 Docker 的 LangExtract 信息提取服务，通过 API Gateway HTTP API 暴露为 REST API，供 Next.js 或其他应用调用。

## 项目简介

LangExtract 是一个使用大语言模型（LLM）从非结构化文本中提取结构化信息的 Python 库。本项目将 LangExtract 部署为无服务器函数，提供高可用、可扩展的信息提取 API 服务。

### 主要特性

- ✅ **无服务器架构**: 基于 AWS Lambda，按需付费，自动扩展
- ✅ **Docker 容器部署**: 使用容器镜像，支持大型依赖包（最大 10GB）
- ✅ **HTTP API**: 通过 API Gateway 暴露标准 REST API
- ✅ **API Key 认证**: 支持 API Key 保护端点安全
- ✅ **CORS 支持**: 支持跨域请求，方便前端调用
- ✅ **本地测试**: 提供本地测试脚本和 Docker 测试环境
- ✅ **自动化部署**: 一键部署脚本，简化更新流程

### 技术栈

- **运行时**: Python 3.9
- **LLM 提供商**: Google Gemini
- **云平台**: AWS Lambda + API Gateway + ECR
- **容器化**: Docker

## 快速开始

### 前置要求

- AWS 账号
- Docker Desktop
- AWS CLI
- Python 3.9+
- Gemini API Key（从 [AI Studio](https://aistudio.google.com/app/apikey) 获取）

### 安装步骤

1. **克隆或进入项目目录**

```bash
cd /Users/leon/Documents/projects/aws_lambda/langextract_aws_lambda
```

2. **配置环境变量**

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的配置
nano .env
```

3. **本地测试（可选）**

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install langextract

# 设置 API Key
export GEMINI_API_KEY='your-gemini-api-key'

# 运行测试
python test_local.py
```

4. **部署到 AWS**

详细步骤请参考 [**AWS_LAMBDA_部署指南.md**](./AWS_LAMBDA_部署指南.md)

简要步骤：

```bash
# 1. 配置 AWS CLI
aws configure

# 2. 创建 ECR 仓库
aws ecr create-repository --repository-name langextract-lambda --region us-east-1

# 3. 创建 Lambda 执行角色
# （参考部署指南）

# 4. 创建 Lambda 函数
# （参考部署指南）

# 5. 后续更新使用部署脚本
chmod +x deploy.sh
./deploy.sh
```

## 项目结构

```
langextract_aws_lambda/
├── README.md                   # 项目说明（本文件）
├── AWS_LAMBDA_部署指南.md      # 详细部署指南
├── lambda_function.py          # Lambda 函数主代码
├── requirements.txt            # Python 依赖
├── Dockerfile                  # Docker 配置
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略文件
├── test_local.py               # 本地测试脚本
└── deploy.sh                   # 自动化部署脚本
```

## API 使用说明

### 端点

```
POST https://{api-id}.execute-api.{region}.amazonaws.com/extract
```

### 请求格式

```json
{
  "text": "要提取信息的文本内容",
  "prompt": "提取任务的描述",
  "examples": [
    {
      "field1": "示例值1",
      "field2": "示例值2"
    }
  ],
  "model_id": "gemini-2.0-flash-exp",
  "chunk_size": 15000
}
```

### 请求参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 要提取信息的文本 |
| `prompt` | string | 是 | 提取任务的描述 |
| `examples` | array | 否 | 示例数据（帮助 LLM 理解输出格式） |
| `model_id` | string | 否 | 模型 ID（默认: `gemini-2.0-flash-exp`） |
| `chunk_size` | integer | 否 | 文本分块大小（默认: 15000） |
| `chunk_overlap` | integer | 否 | 分块重叠大小（默认: 100） |
| `max_threads` | integer | 否 | 最大线程数（默认: 8） |

### 响应格式

```json
{
  "success": true,
  "extractions": [
    {
      "data": {
        "field1": "提取的值1",
        "field2": "提取的值2"
      },
      "source_text": "原始文本片段",
      "chunk_index": 0,
      "char_start": 0,
      "char_end": 100
    }
  ],
  "metadata": {
    "total_extractions": 3,
    "model_used": "gemini-2.0-flash-exp",
    "chunk_size": 15000
  }
}
```

### 请求头（如果配置了 API Key）

```
Content-Type: application/json
X-API-Key: your-api-key
```

### cURL 示例

```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/extract \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "text": "张三，男，45岁，患有高血压。李四，女，32岁，患有糖尿病。",
    "prompt": "提取每个人的姓名、年龄、性别和健康状况",
    "examples": [
      {
        "name": "张三",
        "age": 45,
        "gender": "男",
        "health_condition": "高血压"
      }
    ]
  }'
```

## Next.js 集成示例

### App Router

```typescript
// app/api/extract/route.ts
import { NextRequest, NextResponse } from 'next/server';

const LAMBDA_API_ENDPOINT = process.env.LAMBDA_API_ENDPOINT!;
const LAMBDA_API_KEY = process.env.LAMBDA_API_KEY;

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  const response = await fetch(LAMBDA_API_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(LAMBDA_API_KEY && { 'X-API-Key': LAMBDA_API_KEY }),
    },
    body: JSON.stringify(body),
  });
  
  const data = await response.json();
  return NextResponse.json(data);
}
```

### 环境变量 (.env.local)

```bash
LAMBDA_API_ENDPOINT=https://your-api-id.execute-api.us-east-1.amazonaws.com/extract
LAMBDA_API_KEY=your-api-key
```

完整的集成示例请参考 [部署指南](./AWS_LAMBDA_部署指南.md#nextjs-调用示例)。

## 本地开发

### 使用 Python 测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 设置环境变量
export GEMINI_API_KEY='your-api-key'

# 运行测试
python test_local.py
```

### 使用 Docker 测试

```bash
# 构建镜像
docker build --platform linux/amd64 -t langextract-lambda:test .

# 运行容器
docker run -p 9000:8080 \
  -e GEMINI_API_KEY='your-api-key' \
  langextract-lambda:test

# 在另一个终端发送测试请求
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{"body": "{\"text\": \"测试文本\", \"prompt\": \"提取信息\", \"examples\": []}"}'
```

## 部署更新

当您修改了代码后，使用以下命令更新 Lambda 函数：

```bash
./deploy.sh
```

部署脚本会自动：
1. 构建新的 Docker 镜像
2. 推送到 ECR
3. 更新 Lambda 函数
4. 等待更新完成

## 监控和日志

### 查看 Lambda 日志

```bash
# 通过 AWS CLI
aws logs tail /aws/lambda/langextract-function --follow --region us-east-1

# 或访问 CloudWatch Console
# https://console.aws.amazon.com/cloudwatch/
```

### 查看 API Gateway 日志

在 API Gateway Console 中启用访问日志和执行日志。

## 成本估算

以每月 10,000 次请求为例（假设 1GB 内存，平均 10 秒执行时间）：

- **Lambda**: ~$1.67/月
- **API Gateway HTTP API**: ~$0.01/月
- **ECR 存储**: ~$0.10/月（500MB 镜像）

**总计**: ~$1.78/月

**注意**: AWS 提供免费套餐，前 12 个月可能无需付费。

## 常见问题

### 1. Lambda 函数超时怎么办？

增加超时时间：

```bash
aws lambda update-function-configuration \
  --function-name langextract-function \
  --timeout 300 \
  --region us-east-1
```

### 2. 如何增加内存？

```bash
aws lambda update-function-configuration \
  --function-name langextract-function \
  --memory-size 2048 \
  --region us-east-1
```

### 3. 如何查看错误日志？

```bash
aws logs tail /aws/lambda/langextract-function --follow --region us-east-1
```

更多问题请参考 [部署指南的常见问题排查部分](./AWS_LAMBDA_部署指南.md#常见问题排查)。

## 相关资源

- [LangExtract GitHub](https://github.com/google/langextract)
- [AWS Lambda 文档](https://docs.aws.amazon.com/lambda/)
- [API Gateway HTTP API 文档](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
- [Gemini API 文档](https://ai.google.dev/docs)
- [完整部署指南](./AWS_LAMBDA_部署指南.md)

## 许可证

本项目代码采用 MIT 许可证。

LangExtract 采用 Apache 2.0 许可证。

## 支持

如有问题，请：

1. 查看 [部署指南](./AWS_LAMBDA_部署指南.md)
2. 检查 CloudWatch 日志
3. 参考常见问题排查部分

---

**祝您使用愉快！** 🚀
