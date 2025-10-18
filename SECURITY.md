# 安全政策

## 报告安全漏洞

我们非常重视项目的安全性。如果您发现了安全漏洞，请不要在公开的 Issue 中报告。

### 报告流程

1. **私密报告**: 请通过 GitHub 的 Security Advisories 功能报告
   - 访问仓库的 "Security" 标签
   - 点击 "Report a vulnerability"
   - 填写详细信息

2. **包含信息**:
   - 漏洞描述
   - 重现步骤
   - 潜在影响
   - 可能的解决方案（如果有）

3. **响应时间**:
   - 我们会在 48 小时内确认收到报告
   - 我们会在 7 天内提供初步评估
   - 根据严重程度，会在 30-90 天内发布修复

## 安全最佳实践

### API Key 管理

**切勿将 API Key 提交到代码仓库！**

✅ **正确做法**:
```bash
# 使用环境变量
export GEMINI_API_KEY='your-key'

# 或使用 .env 文件（确保在 .gitignore 中）
echo "GEMINI_API_KEY=your-key" > .env
```

❌ **错误做法**:
```python
# 不要在代码中硬编码
api_key = "AIzaSyD..."  # ❌ 危险！
```

### Lambda 环境变量

在 Lambda 中存储敏感信息时：

1. **使用 AWS Secrets Manager**（推荐）:
```bash
# 创建 Secret
aws secretsmanager create-secret \
  --name langextract/gemini-api-key \
  --secret-string "your-api-key"

# Lambda 中使用 boto3 读取
```

2. **使用加密的环境变量**:
```bash
aws lambda update-function-configuration \
  --function-name langextract-function \
  --environment "Variables={GEMINI_API_KEY=your-key}" \
  --kms-key-id "your-kms-key-id"
```

### API Gateway 安全

1. **启用 API Key 认证**（已在部署指南中说明）

2. **配置请求限流**:
```bash
aws apigatewayv2 update-stage \
  --api-id ${API_ID} \
  --stage-name '$default' \
  --route-settings 'POST /extract={ThrottlingBurstLimit=100,ThrottlingRateLimit=50}'
```

3. **启用 WAF（Web Application Firewall）**:
```bash
# 创建 WAF Web ACL 并关联到 API Gateway
```

4. **限制 CORS 源**:
```python
# 在 lambda_function.py 中
'Access-Control-Allow-Origin': 'https://your-domain.com'  # 替代 '*'
```

### IAM 权限

遵循最小权限原则：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### 数据保护

1. **不记录敏感数据**:
```python
# ✅ 正确
print(f"处理请求 - 文本长度: {len(text)}")

# ❌ 错误
print(f"处理文本: {text}")  # 可能包含 PII
```

2. **在传输中加密**:
- 使用 HTTPS（API Gateway 默认支持）
- 配置 TLS 1.2+

3. **在存储中加密**:
- Lambda 环境变量加密
- S3 存储加密（如果使用）

### Docker 镜像安全

1. **定期更新基础镜像**:
```dockerfile
FROM public.ecr.aws/lambda/python:3.9
# 定期检查更新
```

2. **扫描镜像漏洞**:
```bash
# 使用 AWS ECR 镜像扫描
aws ecr start-image-scan \
  --repository-name langextract-lambda \
  --image-id imageTag=latest
```

3. **不在镜像中包含秘密**:
```dockerfile
# ❌ 不要这样做
ENV GEMINI_API_KEY=your-key
```

### 监控和告警

1. **启用 CloudTrail**:
```bash
# 记录所有 API 调用
```

2. **配置 CloudWatch 告警**:
```bash
# 异常错误率告警
aws cloudwatch put-metric-alarm \
  --alarm-name high-error-rate \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --period 300 \
  --statistic Sum \
  --threshold 10
```

3. **定期审查日志**:
```bash
aws logs tail /aws/lambda/langextract-function --follow
```

## 依赖项安全

### 定期更新依赖

1. **检查更新**:
```bash
pip list --outdated
```

2. **更新依赖**:
```bash
pip install --upgrade langextract
```

3. **锁定版本**（推荐）:
```
# requirements.txt
langextract==1.0.9  # 锁定特定版本
```

### 漏洞扫描

使用工具扫描依赖漏洞：

```bash
# 安装 safety
pip install safety

# 扫描已知漏洞
safety check -r requirements.txt
```

## 已知安全注意事项

### 1. 成本控制

Lambda 函数可能被恶意调用导致高额费用：

**缓解措施**:
- 配置 Lambda 预留并发上限
- 设置 AWS Budgets 告警
- 启用 API Gateway 请求限流

### 2. 输入验证

Lambda 函数会处理用户输入：

**缓解措施**:
- 验证输入长度
- 清理特殊字符
- 限制 chunk_size 上限

```python
# 在 lambda_function.py 中添加
MAX_TEXT_LENGTH = 100000
if len(text) > MAX_TEXT_LENGTH:
    return create_response(400, {'error': '文本太长'})
```

### 3. 提示注入

用户可能通过 prompt 参数进行提示注入：

**缓解措施**:
- 限制 prompt 长度
- 记录可疑的 prompt
- 考虑添加内容过滤

### 4. 速率限制

防止单个用户滥用服务：

**缓解措施**:
```bash
# API Gateway 级别
aws apigatewayv2 update-stage \
  --api-id ${API_ID} \
  --stage-name '$default' \
  --route-settings 'POST /extract={ThrottlingRateLimit=10}'
```

## 合规性

### GDPR（欧盟）

如果处理欧盟用户数据：

1. 不记录个人身份信息（PII）
2. 提供数据删除机制
3. 明确的隐私政策

### HIPAA（美国医疗）

如果处理医疗数据：

1. 使用 HIPAA 合规的 AWS 服务
2. 签署 AWS BAA（Business Associate Agreement）
3. 加密所有数据（传输和存储）
4. 完整的审计日志

**注意**: 本项目默认配置不符合 HIPAA 要求，需要额外配置。

## 安全检查清单

部署前检查：

- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 没有硬编码的 API Key
- [ ] Lambda 环境变量已加密
- [ ] API Gateway 已配置 API Key 认证
- [ ] 已设置请求限流
- [ ] CORS 配置为特定域名（非 `*`）
- [ ] Lambda IAM 角色遵循最小权限
- [ ] 已启用 CloudWatch 日志
- [ ] 已配置告警通知
- [ ] Docker 镜像已扫描漏洞
- [ ] 依赖项已更新到最新版本

## 联系方式

**安全问题**: 请使用 GitHub Security Advisories

**一般问题**: 请使用 GitHub Issues

## 更新日志

- 2025-10-18: 初始安全政策发布

---

感谢您帮助保持项目的安全！🔒

