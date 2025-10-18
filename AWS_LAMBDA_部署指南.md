# AWS Lambda LangExtract 部署指南

本指南将详细指导您如何将 LangExtract 部署为 AWS Lambda 函数，并通过 API Gateway HTTP API 提供服务。

## 目录

1. [前置准备](#前置准备)
2. [本地开发环境设置](#本地开发环境设置)
3. [项目文件说明](#项目文件说明)
4. [本地测试](#本地测试)
5. [AWS 配置](#aws-配置)
6. [部署到 AWS](#部署到-aws)
7. [API Gateway 配置](#api-gateway-配置)
8. [Next.js 调用示例](#nextjs-调用示例)
9. [常见问题排查](#常见问题排查)

---

## 前置准备

### 1. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录您的 Google 账号
3. 点击 "Create API Key" 创建新的 API 密钥
4. 保存好您的 API Key（后续会用到）

### 2. 安装必要工具

#### Docker

Docker 用于构建容器镜像。

- **macOS**: 下载并安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Windows**: 下载并安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- **Linux**: 参考 [Docker 官方文档](https://docs.docker.com/engine/install/)

安装后，验证 Docker 是否正常工作：

```bash
docker --version
# 输出示例: Docker version 24.0.6, build ed223bc
```

#### AWS CLI

AWS CLI 用于与 AWS 服务交互。

安装方法：

```bash
# macOS (使用 Homebrew)
brew install awscli

# macOS/Linux (官方安装脚本)
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Windows
# 下载并运行安装程序: https://awscli.amazonaws.com/AWSCLIV2.msi
```

验证安装：

```bash
aws --version
# 输出示例: aws-cli/2.13.0 Python/3.11.4 Darwin/23.1.0 source/arm64
```

#### Python 3.9+

您的系统已安装 Python 3.9.6，可以直接使用。

---

## 本地开发环境设置

### 1. 创建 Python 虚拟环境

```bash
# 进入项目目录
cd /Users/leon/Documents/projects/aws_lambda/langextract_aws_lambda

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 升级 pip
pip install --upgrade pip
```

### 2. 安装依赖

```bash
# 安装 langextract
pip install langextract

# 验证安装
python -c "import langextract; print(langextract.__version__)"
```

### 3. 配置环境变量

创建 `.env` 文件（已提供 `.env.example` 作为模板）：

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入您的配置
nano .env  # 或使用任何文本编辑器
```

`.env` 文件内容示例：

```bash
# Gemini API Key（必需）
GEMINI_API_KEY=AIzaSyD...your_actual_key

# AWS 配置
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012  # 您的 AWS 账户 ID
ECR_REPOSITORY_NAME=langextract-lambda
LAMBDA_FUNCTION_NAME=langextract-function

# Lambda 函数配置
LAMBDA_MEMORY_SIZE=1024
LAMBDA_TIMEOUT=300
```

**如何获取 AWS Account ID:**

```bash
aws sts get-caller-identity --query Account --output text
```

---

## 项目文件说明

### lambda_function.py

这是 Lambda 函数的核心代码，主要功能：

- **`lambda_handler(event, context)`**: Lambda 入口函数
  - 解析 API Gateway 传入的 JSON 请求
  - 调用 `langextract.extract()` 进行信息提取
  - 返回标准的 API Gateway 响应格式

**支持的请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 要提取信息的文本 |
| `prompt` | string | 是 | 提取任务的描述 |
| `examples` | array | 否 | 示例数据（帮助 LLM 理解输出格式） |
| `model_id` | string | 否 | 模型 ID（默认: `gemini-2.0-flash-exp`） |
| `chunk_size` | integer | 否 | 文本分块大小（默认: 15000） |
| `chunk_overlap` | integer | 否 | 分块重叠大小（默认: 100） |
| `max_threads` | integer | 否 | 最大线程数（默认: 8） |

**响应格式：**

```json
{
  "success": true,
  "extractions": [
    {
      "data": { /* 提取的结构化数据 */ },
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

### Dockerfile

基于 AWS Lambda Python 3.9 官方镜像构建容器：

- 安装 `langextract` 和依赖
- 复制 Lambda 函数代码
- 设置入口点为 `lambda_function.lambda_handler`

### requirements.txt

Python 依赖列表，目前只需要 `langextract`。

### test_local.py

本地测试脚本，无需部署即可测试 Lambda 函数逻辑。

### deploy.sh

自动化部署脚本，执行以下步骤：
1. 构建 Docker 镜像
2. 标记镜像
3. 登录 ECR
4. 推送镜像到 ECR
5. 更新 Lambda 函数

---

## 本地测试

在部署到 AWS 之前，建议先在本地测试 Lambda 函数。

### 方法 1: 使用 test_local.py（推荐）

这是最简单的测试方法，无需 Docker。

```bash
# 确保已激活虚拟环境
source venv/bin/activate

# 设置环境变量
export GEMINI_API_KEY='your_gemini_api_key'

# 运行测试
python test_local.py
```

**预期输出：**

```
LangExtract Lambda 函数本地测试
============================================================
开始测试 Lambda 函数...
============================================================

状态码: 200

Headers: {
  "Content-Type": "application/json",
  ...
}

响应体:
{
  "success": true,
  "extractions": [...],
  ...
}

✅ 测试成功!
提取了 3 条记录
```

### 方法 2: 使用 Docker 本地测试

使用与 AWS Lambda 相同的运行环境测试。

#### Step 1: 构建镜像

```bash
docker build --platform linux/amd64 -t langextract-lambda:test .
```

#### Step 2: 运行容器

```bash
docker run -p 9000:8080 \
  -e GEMINI_API_KEY='your_gemini_api_key' \
  langextract-lambda:test
```

#### Step 3: 调用测试

打开新终端窗口，发送测试请求：

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "{\"text\": \"张三，男，45岁，患有高血压。\", \"prompt\": \"提取姓名、年龄和健康状况\", \"examples\": [{\"name\": \"张三\", \"age\": 45, \"health\": \"高血压\"}]}"
  }'
```

**成功的响应示例：**

```json
{
  "statusCode": 200,
  "headers": {...},
  "body": "{\"success\": true, \"extractions\": [...]}"
}
```

---

## AWS 配置

### 1. 配置 AWS CLI

如果您是第一次使用 AWS CLI，需要配置访问凭证：

```bash
aws configure
```

按提示输入：

- **AWS Access Key ID**: 从 IAM 控制台获取
- **AWS Secret Access Key**: 从 IAM 控制台获取
- **Default region name**: 例如 `us-east-1`
- **Default output format**: 输入 `json`

**如何获取 Access Key:**

1. 登录 [AWS Console](https://console.aws.amazon.com/)
2. 导航到 IAM → Users → 您的用户名
3. 点击 "Security credentials" 标签
4. 点击 "Create access key"
5. 下载或记录 Access Key ID 和 Secret Access Key

### 2. 创建 ECR 仓库

ECR (Elastic Container Registry) 用于存储 Docker 镜像。

```bash
# 设置变量
AWS_REGION=us-east-1
ECR_REPOSITORY_NAME=langextract-lambda

# 创建 ECR 仓库
aws ecr create-repository \
  --repository-name ${ECR_REPOSITORY_NAME} \
  --region ${AWS_REGION}
```

**成功输出示例：**

```json
{
  "repository": {
    "repositoryArn": "arn:aws:ecr:us-east-1:123456789012:repository/langextract-lambda",
    "repositoryName": "langextract-lambda",
    "repositoryUri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/langextract-lambda"
  }
}
```

记录 `repositoryUri`，后续会用到。

### 3. 创建 Lambda 执行角色

Lambda 函数需要一个 IAM 角色来执行。

#### Step 1: 创建信任策略文件

```bash
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
```

#### Step 2: 创建 IAM 角色

```bash
aws iam create-role \
  --role-name langextract-lambda-role \
  --assume-role-policy-document file://trust-policy.json
```

#### Step 3: 附加基本执行策略

```bash
aws iam attach-role-policy \
  --role-name langextract-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

#### Step 4: 获取角色 ARN

```bash
aws iam get-role \
  --role-name langextract-lambda-role \
  --query 'Role.Arn' \
  --output text
```

记录输出的 ARN，例如：`arn:aws:iam::123456789012:role/langextract-lambda-role`

---

## 部署到 AWS

### 方法 1: 使用自动化脚本（推荐）

我们提供了 `deploy.sh` 脚本来自动化整个部署流程。

#### Step 1: 赋予执行权限

```bash
chmod +x deploy.sh
```

#### Step 2: 确保 .env 文件配置正确

检查 `.env` 文件中的配置：

```bash
cat .env
```

确保以下变量已正确设置：
- `AWS_REGION`
- `AWS_ACCOUNT_ID`
- `ECR_REPOSITORY_NAME`
- `LAMBDA_FUNCTION_NAME`

#### Step 3: 首次部署 - 创建 Lambda 函数

在运行部署脚本之前，需要先创建 Lambda 函数：

```bash
# 设置变量（从 .env 加载）
source .env

# 构建并推送镜像到 ECR
docker build --platform linux/amd64 -t langextract-lambda .
docker tag langextract-lambda:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

# 创建 Lambda 函数
aws lambda create-function \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --package-type Image \
  --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/langextract-lambda-role \
  --timeout ${LAMBDA_TIMEOUT:-300} \
  --memory-size ${LAMBDA_MEMORY_SIZE:-1024} \
  --environment "Variables={GEMINI_API_KEY=${GEMINI_API_KEY}}" \
  --region ${AWS_REGION}
```

**重要配置说明：**

- `--timeout 300`: 超时时间 300 秒（5 分钟），因为 LLM 推理可能需要较长时间
- `--memory-size 1024`: 内存 1GB，根据实际使用情况可以调整（512MB - 10GB）
- `--environment`: 设置环境变量，包括 `GEMINI_API_KEY`

#### Step 4: 后续更新使用部署脚本

创建函数后，后续更新只需运行：

```bash
./deploy.sh
```

脚本会自动完成：
1. ✅ 构建 Docker 镜像
2. ✅ 标记镜像
3. ✅ 登录 ECR
4. ✅ 推送镜像到 ECR
5. ✅ 更新 Lambda 函数

**输出示例：**

```
[INFO] 开始部署流程...
[INFO] AWS 区域: us-east-1
[INFO] ECR 仓库: 123456789012.dkr.ecr.us-east-1.amazonaws.com/langextract-lambda
[INFO] Lambda 函数: langextract-function
[INFO] 镜像标签: latest

[INFO] Step 1/5: 构建 Docker 镜像...
[INFO] ✅ Docker 镜像构建成功

[INFO] Step 2/5: 标记镜像...
[INFO] ✅ 镜像标记完成

[INFO] Step 3/5: 登录到 AWS ECR...
[INFO] ✅ ECR 登录成功

[INFO] Step 4/5: 推送镜像到 ECR...
[INFO] ✅ 镜像推送成功

[INFO] Step 5/5: 更新 Lambda 函数...
[INFO] ✅ Lambda 函数更新成功

[INFO] 🎉 部署完成！
```

### 方法 2: 手动部署

如果您想了解每一步的细节，可以手动执行：

```bash
# 1. 构建镜像
docker build --platform linux/amd64 -t langextract-lambda .

# 2. 标记镜像
docker tag langextract-lambda:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

# 3. 登录 ECR
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 4. 推送镜像
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

# 5. 更新 Lambda 函数
aws lambda update-function-code \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest \
  --region ${AWS_REGION}
```

### 验证部署

```bash
# 检查 Lambda 函数状态
aws lambda get-function \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --region ${AWS_REGION}
```

---

## API Gateway 配置

现在 Lambda 函数已经部署，我们需要创建 API Gateway 来暴露 HTTP 接口。

### Step 1: 创建 HTTP API

```bash
# 创建 HTTP API
API_ID=$(aws apigatewayv2 create-api \
  --name "LangExtract API" \
  --protocol-type HTTP \
  --region ${AWS_REGION} \
  --query 'ApiId' \
  --output text)

echo "API ID: ${API_ID}"
```

### Step 2: 创建 Lambda 集成

```bash
# 获取 Lambda ARN
LAMBDA_ARN=$(aws lambda get-function \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --region ${AWS_REGION} \
  --query 'Configuration.FunctionArn' \
  --output text)

# 创建集成
INTEGRATION_ID=$(aws apigatewayv2 create-integration \
  --api-id ${API_ID} \
  --integration-type AWS_PROXY \
  --integration-uri ${LAMBDA_ARN} \
  --payload-format-version 2.0 \
  --region ${AWS_REGION} \
  --query 'IntegrationId' \
  --output text)

echo "Integration ID: ${INTEGRATION_ID}"
```

### Step 3: 创建路由

```bash
# 创建 POST /extract 路由
aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "POST /extract" \
  --target integrations/${INTEGRATION_ID} \
  --region ${AWS_REGION}
```

### Step 4: 创建部署阶段

```bash
# 创建 $default 阶段（自动部署）
aws apigatewayv2 create-stage \
  --api-id ${API_ID} \
  --stage-name '$default' \
  --auto-deploy \
  --region ${AWS_REGION}
```

### Step 5: 授予 API Gateway 调用 Lambda 的权限

```bash
aws lambda add-permission \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigatewayv2.amazonaws.com \
  --source-arn "arn:aws:execute-api:${AWS_REGION}:${AWS_ACCOUNT_ID}:${API_ID}/*/*" \
  --region ${AWS_REGION}
```

### Step 6: 获取 API 端点

```bash
API_ENDPOINT="https://${API_ID}.execute-api.${AWS_REGION}.amazonaws.com/extract"
echo "API 端点: ${API_ENDPOINT}"
```

保存这个端点 URL，在 Next.js 中会用到。

### Step 7: 配置 API Key 认证（可选但推荐）

为了安全，建议配置 API Key 认证。

#### 创建 API Key

```bash
API_KEY_ID=$(aws apigatewayv2 create-api-key \
  --name "LangExtract API Key" \
  --region ${AWS_REGION} \
  --query 'ApiKeyId' \
  --output text)

# 获取 API Key 值
API_KEY_VALUE=$(aws apigatewayv2 get-api-key \
  --api-key-id ${API_KEY_ID} \
  --region ${AWS_REGION} \
  --query 'ApiKey' \
  --output text)

echo "API Key: ${API_KEY_VALUE}"
```

#### 更新路由以要求 API Key

```bash
# 获取路由 ID
ROUTE_ID=$(aws apigatewayv2 get-routes \
  --api-id ${API_ID} \
  --region ${AWS_REGION} \
  --query 'Items[0].RouteId' \
  --output text)

# 更新路由，要求 API Key
aws apigatewayv2 update-route \
  --api-id ${API_ID} \
  --route-id ${ROUTE_ID} \
  --api-key-required \
  --region ${AWS_REGION}
```

### 测试 API

```bash
# 不使用 API Key 的测试
curl -X POST ${API_ENDPOINT} \
  -H "Content-Type: application/json" \
  -d '{
    "text": "张三，男，45岁，患有高血压。",
    "prompt": "提取姓名、年龄、性别和健康状况",
    "examples": [{"name": "张三", "age": 45, "gender": "男", "health": "高血压"}]
  }'

# 使用 API Key 的测试（如果配置了 API Key）
curl -X POST ${API_ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY_VALUE}" \
  -d '{
    "text": "张三，男，45岁，患有高血压。",
    "prompt": "提取姓名、年龄、性别和健康状况",
    "examples": [{"name": "张三", "age": 45, "gender": "男", "health": "高血压"}]
  }'
```

---

## Next.js 调用示例

在您的 Next.js 后端代码中调用 Lambda 函数。

### API Route 示例 (App Router)

创建 `app/api/extract/route.ts`:

```typescript
// app/api/extract/route.ts
import { NextRequest, NextResponse } from 'next/server';

const LAMBDA_API_ENDPOINT = process.env.LAMBDA_API_ENDPOINT!;
const LAMBDA_API_KEY = process.env.LAMBDA_API_KEY;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // 验证必需参数
    if (!body.text || !body.prompt) {
      return NextResponse.json(
        { error: '缺少必需参数: text 或 prompt' },
        { status: 400 }
      );
    }

    // 调用 Lambda 函数
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    // 如果配置了 API Key，添加到请求头
    if (LAMBDA_API_KEY) {
      headers['X-API-Key'] = LAMBDA_API_KEY;
    }

    const response = await fetch(LAMBDA_API_ENDPOINT, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        text: body.text,
        prompt: body.prompt,
        examples: body.examples || [],
        model_id: body.model_id || 'gemini-2.0-flash-exp',
        chunk_size: body.chunk_size || 15000,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: 'Lambda 函数调用失败', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('调用 Lambda 函数时出错:', error);
    return NextResponse.json(
      { error: '服务器内部错误', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}
```

### 环境变量配置

在 Next.js 项目的 `.env.local` 文件中添加：

```bash
LAMBDA_API_ENDPOINT=https://your-api-id.execute-api.us-east-1.amazonaws.com/extract
LAMBDA_API_KEY=your-api-key-value  # 如果配置了 API Key
```

### 前端调用示例

```typescript
// 在组件或客户端代码中
async function extractInformation(text: string, prompt: string, examples: any[]) {
  try {
    const response = await fetch('/api/extract', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        prompt,
        examples,
      }),
    });

    if (!response.ok) {
      throw new Error('提取失败');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('提取信息时出错:', error);
    throw error;
  }
}

// 使用示例
const result = await extractInformation(
  '张三，男，45岁，患有高血压。',
  '提取姓名、年龄、性别和健康状况',
  [{ name: '张三', age: 45, gender: '男', health: '高血压' }]
);

console.log('提取结果:', result.extractions);
```

### Pages Router 示例

如果您使用 Pages Router，创建 `pages/api/extract.ts`:

```typescript
// pages/api/extract.ts
import type { NextApiRequest, NextApiResponse } from 'next';

const LAMBDA_API_ENDPOINT = process.env.LAMBDA_API_ENDPOINT!;
const LAMBDA_API_KEY = process.env.LAMBDA_API_KEY;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: '仅支持 POST 请求' });
  }

  try {
    const { text, prompt, examples, model_id, chunk_size } = req.body;

    if (!text || !prompt) {
      return res.status(400).json({ error: '缺少必需参数: text 或 prompt' });
    }

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (LAMBDA_API_KEY) {
      headers['X-API-Key'] = LAMBDA_API_KEY;
    }

    const response = await fetch(LAMBDA_API_ENDPOINT, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        text,
        prompt,
        examples: examples || [],
        model_id: model_id || 'gemini-2.0-flash-exp',
        chunk_size: chunk_size || 15000,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json({
        error: 'Lambda 函数调用失败',
        details: errorData,
      });
    }

    const data = await response.json();
    return res.status(200).json(data);

  } catch (error) {
    console.error('调用 Lambda 函数时出错:', error);
    return res.status(500).json({
      error: '服务器内部错误',
      details: error instanceof Error ? error.message : String(error),
    });
  }
}
```

---

## 常见问题排查

### 1. Lambda 函数超时

**症状**: 请求返回 504 Gateway Timeout

**原因**: Lambda 函数执行时间超过配置的超时限制（默认 3 秒）

**解决方案**:

```bash
# 增加超时时间到 5 分钟
aws lambda update-function-configuration \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --timeout 300 \
  --region ${AWS_REGION}
```

### 2. 内存不足

**症状**: Lambda 函数日志显示 "Process exited before completing request" 或内存不足错误

**原因**: Lambda 函数分配的内存太少

**解决方案**:

```bash
# 增加内存到 2GB
aws lambda update-function-configuration \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --memory-size 2048 \
  --region ${AWS_REGION}
```

**提示**: Lambda 的 CPU 性能与内存成正比，增加内存也会提升 CPU 性能。

### 3. API Key 无效

**症状**: 返回 403 Forbidden

**原因**: 

- 未提供 API Key
- API Key 不正确
- API Key 未正确配置到 API Gateway

**解决方案**:

```bash
# 验证 API Key
aws apigatewayv2 get-api-key \
  --api-key-id ${API_KEY_ID} \
  --region ${AWS_REGION}

# 确认路由要求 API Key
aws apigatewayv2 get-route \
  --api-id ${API_ID} \
  --route-id ${ROUTE_ID} \
  --region ${AWS_REGION} \
  --query 'ApiKeyRequired'
```

### 4. GEMINI_API_KEY 未设置

**症状**: Lambda 函数返回 "GEMINI_API_KEY 环境变量未设置"

**解决方案**:

```bash
# 更新环境变量
aws lambda update-function-configuration \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --environment "Variables={GEMINI_API_KEY=your_actual_api_key}" \
  --region ${AWS_REGION}
```

### 5. Docker 镜像构建失败

**症状**: `docker build` 命令失败

**常见原因和解决方案**:

```bash
# 问题: 平台不匹配
# 解决: 明确指定平台
docker build --platform linux/amd64 -t langextract-lambda .

# 问题: 网络问题导致依赖安装失败
# 解决: 使用国内镜像源
# 在 Dockerfile 中添加:
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 6. ECR 推送失败

**症状**: `docker push` 失败，提示认证错误

**解决方案**:

```bash
# 重新登录 ECR
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 验证登录状态
docker info | grep Registry
```

### 7. 查看 Lambda 日志

Lambda 函数的日志存储在 CloudWatch Logs 中。

**通过 AWS CLI 查看**:

```bash
# 获取最新的日志流
LOG_STREAM=$(aws logs describe-log-streams \
  --log-group-name /aws/lambda/${LAMBDA_FUNCTION_NAME} \
  --order-by LastEventTime \
  --descending \
  --max-items 1 \
  --region ${AWS_REGION} \
  --query 'logStreams[0].logStreamName' \
  --output text)

# 查看日志
aws logs get-log-events \
  --log-group-name /aws/lambda/${LAMBDA_FUNCTION_NAME} \
  --log-stream-name ${LOG_STREAM} \
  --region ${AWS_REGION}
```

**通过 AWS Console 查看**:

1. 打开 [CloudWatch Console](https://console.aws.amazon.com/cloudwatch/)
2. 导航到 "Logs" → "Log groups"
3. 找到 `/aws/lambda/langextract-function`
4. 点击查看最新的日志流

### 8. 测试 Lambda 函数（不通过 API Gateway）

```bash
# 创建测试事件文件
cat > test-event.json << 'EOF'
{
  "body": "{\"text\": \"张三，男，45岁，患有高血压。\", \"prompt\": \"提取姓名、年龄、性别和健康状况\", \"examples\": [{\"name\": \"张三\", \"age\": 45, \"gender\": \"男\", \"health\": \"高血压\"}]}"
}
EOF

# 调用 Lambda 函数
aws lambda invoke \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --payload file://test-event.json \
  --region ${AWS_REGION} \
  response.json

# 查看响应
cat response.json | jq .
```

### 9. API Gateway 返回 500 错误

**可能原因**:

- Lambda 函数未正确配置
- Lambda 函数返回格式不正确
- Lambda 执行角色权限不足

**排查步骤**:

1. 检查 Lambda 函数日志
2. 测试 Lambda 函数（绕过 API Gateway）
3. 验证 Lambda 返回格式符合 API Gateway 要求

### 10. CORS 错误

**症状**: 浏览器报 CORS 错误

**解决方案**: Lambda 函数已经包含了 CORS 头，但如果仍有问题：

```bash
# 为 API Gateway 启用 CORS
aws apigatewayv2 update-api \
  --api-id ${API_ID} \
  --cors-configuration AllowOrigins='*',AllowMethods='POST,OPTIONS',AllowHeaders='Content-Type,X-API-Key' \
  --region ${AWS_REGION}
```

---

## 成本估算

### Lambda 定价（us-east-1 区域）

- **请求费用**: $0.20 / 百万请求
- **计算费用**: $0.0000166667 / GB-秒

**示例计算（假设配置 1GB 内存，平均执行 10 秒）**:

- 每月 10,000 次请求
- 请求费用: 10,000 / 1,000,000 × $0.20 = $0.002
- 计算费用: 10,000 × 10 秒 × 1 GB × $0.0000166667 = $1.67
- **总计**: ~$1.67/月

### API Gateway HTTP API 定价

- $1.00 / 百万请求

**示例计算**:

- 每月 10,000 次请求
- API Gateway 费用: 10,000 / 1,000,000 × $1.00 = $0.01
- **总计**: ~$0.01/月

### 总计

每月 10,000 次请求的总成本约 **$1.68**。

**注意**: 

- AWS 提供免费套餐（前 12 个月）
- Lambda 免费套餐: 每月 100 万次请求和 400,000 GB-秒
- API Gateway 免费套餐: 每月 100 万次调用（前 12 个月）

---

## 优化建议

### 1. 使用 Lambda 预留并发

如果您的应用需要低延迟，可以配置预留并发避免冷启动：

```bash
aws lambda put-provisioned-concurrency-config \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --provisioned-concurrent-executions 1 \
  --qualifier $LATEST \
  --region ${AWS_REGION}
```

**注意**: 预留并发会产生额外费用。

### 2. 启用 API Gateway 缓存

对于相同的请求，可以启用缓存减少 Lambda 调用次数：

```bash
aws apigatewayv2 update-stage \
  --api-id ${API_ID} \
  --stage-name '$default' \
  --route-settings 'POST /extract={ThrottlingBurstLimit=100,ThrottlingRateLimit=50}' \
  --region ${AWS_REGION}
```

### 3. 监控和告警

设置 CloudWatch 告警监控 Lambda 函数：

```bash
# 创建告警（Lambda 错误率 > 5%）
aws cloudwatch put-metric-alarm \
  --alarm-name langextract-lambda-errors \
  --alarm-description "Lambda function error rate > 5%" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=${LAMBDA_FUNCTION_NAME} \
  --evaluation-periods 1 \
  --region ${AWS_REGION}
```

### 4. 使用 Lambda Layers（可选）

如果您有多个 Lambda 函数使用相同的依赖，可以将依赖打包成 Layer：

```bash
# 创建 Layer 目录
mkdir -p layer/python
pip install langextract -t layer/python

# 打包 Layer
cd layer
zip -r ../langextract-layer.zip .
cd ..

# 发布 Layer
aws lambda publish-layer-version \
  --layer-name langextract \
  --zip-file fileb://langextract-layer.zip \
  --compatible-runtimes python3.9 \
  --region ${AWS_REGION}
```

---

## 下一步

恭喜！您已成功部署了 LangExtract Lambda 函数。

**建议的后续步骤**:

1. ✅ 在 Next.js 中集成 API 调用
2. ✅ 添加错误处理和重试逻辑
3. ✅ 设置 CloudWatch 监控和告警
4. ✅ 考虑添加请求限流保护
5. ✅ 实施生产环境的安全最佳实践

**相关资源**:

- [AWS Lambda 文档](https://docs.aws.amazon.com/lambda/)
- [API Gateway HTTP API 文档](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
- [LangExtract GitHub](https://github.com/google/langextract)
- [Gemini API 文档](https://ai.google.dev/docs)

---

## 支持

如有问题或需要帮助，请：

- 查看 AWS CloudWatch 日志
- 参考本指南的常见问题排查部分
- 查看 LangExtract 官方文档

祝您使用愉快！🎉

