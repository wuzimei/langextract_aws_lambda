#!/bin/bash

# AWS Lambda LangExtract 部署脚本
# 此脚本自动化 Docker 镜像构建、推送到 ECR 以及更新 Lambda 函数的过程

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    print_error ".env 文件不存在"
    print_info "请复制 .env.example 并填写相关配置："
    print_info "  cp .env.example .env"
    exit 1
fi

# 加载环境变量
source .env

# 验证必需的环境变量
if [ -z "$AWS_REGION" ] || [ -z "$AWS_ACCOUNT_ID" ] || [ -z "$ECR_REPOSITORY_NAME" ] || [ -z "$LAMBDA_FUNCTION_NAME" ]; then
    print_error "缺少必需的环境变量"
    print_info "请确保 .env 文件中设置了以下变量："
    print_info "  AWS_REGION, AWS_ACCOUNT_ID, ECR_REPOSITORY_NAME, LAMBDA_FUNCTION_NAME"
    exit 1
fi

# 构建变量
IMAGE_NAME="langextract-lambda"
IMAGE_TAG="${1:-latest}"  # 默认使用 latest 标签
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}"

print_info "开始部署流程..."
print_info "AWS 区域: ${AWS_REGION}"
print_info "ECR 仓库: ${ECR_URI}"
print_info "Lambda 函数: ${LAMBDA_FUNCTION_NAME}"
print_info "镜像标签: ${IMAGE_TAG}"
echo ""

# Step 1: 构建 Docker 镜像
print_info "Step 1/5: 构建 Docker 镜像..."
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${IMAGE_TAG} .
if [ $? -eq 0 ]; then
    print_info "✅ Docker 镜像构建成功"
else
    print_error "❌ Docker 镜像构建失败"
    exit 1
fi
echo ""

# Step 2: 标记镜像
print_info "Step 2/5: 标记镜像..."
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
print_info "✅ 镜像标记完成"
echo ""

# Step 3: 登录到 ECR
print_info "Step 3/5: 登录到 AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
if [ $? -eq 0 ]; then
    print_info "✅ ECR 登录成功"
else
    print_error "❌ ECR 登录失败"
    exit 1
fi
echo ""

# Step 4: 推送镜像到 ECR
print_info "Step 4/5: 推送镜像到 ECR..."
docker push ${ECR_URI}:${IMAGE_TAG}
if [ $? -eq 0 ]; then
    print_info "✅ 镜像推送成功"
else
    print_error "❌ 镜像推送失败"
    exit 1
fi
echo ""

# Step 5: 更新 Lambda 函数
print_info "Step 5/5: 更新 Lambda 函数..."
aws lambda update-function-code \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --image-uri ${ECR_URI}:${IMAGE_TAG} \
    --region ${AWS_REGION} \
    > /dev/null

if [ $? -eq 0 ]; then
    print_info "✅ Lambda 函数更新成功"
else
    print_error "❌ Lambda 函数更新失败"
    exit 1
fi
echo ""

# 等待函数更新完成
print_info "等待 Lambda 函数更新完成..."
aws lambda wait function-updated \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --region ${AWS_REGION}

print_info "✅ Lambda 函数已成功更新并处于活动状态"
echo ""

# 获取函数信息
print_info "Lambda 函数信息:"
aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} --query 'Configuration.[FunctionName,LastModified,State,MemorySize,Timeout]' --output table

echo ""
print_info "🎉 部署完成！"
print_info "您现在可以通过 API Gateway 调用 Lambda 函数"

