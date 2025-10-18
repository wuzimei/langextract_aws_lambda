# GitHub 发布指南

本指南将帮助您将这个项目发布到 GitHub 并设置为开源项目。

## 📋 发布前检查清单

在发布到 GitHub 之前，请确认：

- [x] ✅ 已创建 MIT 许可证
- [x] ✅ 已创建 README.md（含徽章）
- [x] ✅ 已创建贡献指南（CONTRIBUTING.md）
- [x] ✅ 已创建安全政策（SECURITY.md）
- [x] ✅ 已创建行为准则（CODE_OF_CONDUCT.md）
- [x] ✅ 已创建更新日志（CHANGELOG.md）
- [x] ✅ 已配置 .gitignore（包含敏感信息）
- [x] ✅ 已创建 Issue 模板
- [x] ✅ 已创建 PR 模板
- [ ] ⚠️ 需要删除 `env.example.txt` 中的真实 API Key（如果有）
- [ ] ⚠️ 需要检查代码中是否有硬编码的敏感信息

## 🚀 发布步骤

### Step 1: 最后检查

```bash
# 确保当前在项目目录
cd /Users/leon/Documents/projects/aws_lambda/langextract_aws_lambda

# 检查是否有敏感信息
grep -r "AIza" . --exclude-dir=.git --exclude-dir=venv
grep -r "sk-" . --exclude-dir=.git --exclude-dir=venv
grep -r "AWS_SECRET" . --exclude-dir=.git --exclude-dir=venv

# 如果发现任何敏感信息，立即删除！
```

### Step 2: 初始化 Git 仓库（如果还没有）

```bash
# 查看当前 git 状态
git status

# 如果还没有初始化，运行：
# git init
# git branch -M main
```

### Step 3: 添加和提交文件

```bash
# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 确认没有敏感信息后，提交
git commit -m "feat: 初始化 LangExtract AWS Lambda 项目

- 添加 Lambda 函数实现
- 添加 Docker 容器化配置
- 添加完整部署指南
- 添加本地测试脚本
- 添加自动化部署脚本
- 添加开源社区文件（LICENSE, CONTRIBUTING, etc.）
"
```

### Step 4: 在 GitHub 上创建仓库

1. **访问 GitHub**: https://github.com/new

2. **填写仓库信息**:
   - **Repository name**: `langextract-aws-lambda`（或您喜欢的名字）
   - **Description**: `Deploy LangExtract as AWS Lambda function with Docker and API Gateway`
   - **Visibility**: 选择 `Public`（公开）
   - **不要勾选**: "Add a README file"（我们已经有了）
   - **不要勾选**: "Add .gitignore"（我们已经有了）
   - **不要勾选**: "Choose a license"（我们已经有了）

3. **点击**: "Create repository"

### Step 5: 推送到 GitHub

复制 GitHub 提供的命令，或使用以下命令：

```bash
# 添加远程仓库（替换成您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/langextract-aws-lambda.git

# 推送到 GitHub
git push -u origin main
```

**如果遇到认证问题**，使用 Personal Access Token：

```bash
# 生成 Token: https://github.com/settings/tokens
# 权限选择: repo（完整权限）

# 使用 Token 推送
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/langextract-aws-lambda.git
git push -u origin main
```

### Step 6: 配置 GitHub 仓库设置

#### 6.1 添加仓库主题（Topics）

在仓库页面点击设置图标，添加以下主题：

```
aws-lambda
langextract
docker
python
gemini
api-gateway
serverless
information-extraction
llm
nextjs
```

#### 6.2 启用功能

在 Settings → General → Features 中：

- ✅ Issues
- ✅ Discussions（可选，用于社区讨论）
- ✅ Wiki（可选）

#### 6.3 配置 GitHub Pages（可选）

如果您想要部署文档网站：

Settings → Pages → Source → 选择 `main` 分支的 `/docs` 文件夹

#### 6.4 设置仓库描述

在仓库首页点击 ⚙️ 图标，填写：

- **Description**: `🚀 Deploy LangExtract as AWS Lambda function with Docker and API Gateway. Extract structured information from text using LLMs. | 使用 Docker 将 LangExtract 部署为 AWS Lambda 函数，通过 LLM 从文本中提取结构化信息。`
- **Website**: 可以留空或填写部署指南链接
- **Topics**: 添加相关标签

### Step 7: 创建首个 Release

1. **访问**: https://github.com/YOUR_USERNAME/langextract-aws-lambda/releases/new

2. **填写信息**:
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - 首次发布 🎉`
   - **Description**: 
   
   ```markdown
   ## 🎉 首次发布
   
   LangExtract AWS Lambda 项目的第一个正式版本！
   
   ### ✨ 主要特性
   
   - ✅ Lambda 函数实现（Python 3.9）
   - ✅ Docker 容器化部署
   - ✅ API Gateway HTTP API 集成
   - ✅ API Key 认证支持
   - ✅ 完整的中文部署指南
   - ✅ 本地测试和自动化部署脚本
   - ✅ Next.js 集成示例
   
   ### 📚 文档
   
   - [README.md](./README.md) - 快速开始
   - [AWS_LAMBDA_部署指南.md](./AWS_LAMBDA_部署指南.md) - 详细教程
   - [CONTRIBUTING.md](./CONTRIBUTING.md) - 贡献指南
   
   ### 🚀 快速开始
   
   详见 [部署指南](./AWS_LAMBDA_部署指南.md)
   
   ### 🙏 致谢
   
   感谢 [LangExtract](https://github.com/google/langextract) 项目！
   ```

3. **点击**: "Publish release"

### Step 8: 添加 README 徽章（自动生成）

GitHub 会自动显示以下徽章：

- Stars 数量
- Forks 数量
- License
- 最后提交时间

您可以在 https://shields.io/ 创建更多自定义徽章。

### Step 9: 设置 GitHub Actions（可选）

在 `.github/workflows/` 目录下可以添加 CI/CD 工作流：

**示例：代码检查工作流**

创建 `.github/workflows/lint.yml`:

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install pylint black isort
          pip install -r requirements.txt
      - name: Run linters
        run: |
          black --check lambda_function.py test_local.py
          pylint lambda_function.py
```

### Step 10: 宣传您的项目

#### 在社交媒体分享

- Twitter/X
- LinkedIn
- Reddit (r/aws, r/Python)
- Hacker News

#### 提交到目录

- [Awesome AWS Lambda](https://github.com/simplemerchant/awesome-aws-lambda)
- [Awesome LLM](https://github.com/Hannibal046/Awesome-LLM)
- [Awesome Gemini](搜索相关项目)

#### 撰写博客文章

分享您的部署经验和学习心得。

## 📊 维护项目

### 定期更新

```bash
# 更新依赖
pip list --outdated
pip install --upgrade langextract

# 更新 requirements.txt
pip freeze > requirements.txt

# 提交更新
git add requirements.txt
git commit -m "chore: 更新依赖"
git push
```

### 响应 Issues 和 PRs

- 及时回复 Issues
- 审查 Pull Requests
- 更新文档
- 发布新版本

### 版本管理

遵循语义化版本：

- **主版本号（MAJOR）**: 不兼容的 API 更改
- **次版本号（MINOR）**: 向后兼容的功能新增
- **修订号（PATCH）**: 向后兼容的问题修复

## 🔒 安全提醒

### 永远不要提交的内容

- ❌ `.env` 文件
- ❌ API Keys
- ❌ AWS 访问密钥
- ❌ 私钥文件（.pem, .key）
- ❌ 数据库密码

### 如果不小心提交了敏感信息

1. **立即撤销 API Key**（在服务提供商处）

2. **从 Git 历史中删除**:
   
   ```bash
   # 使用 BFG Repo-Cleaner
   # https://rtyley.github.io/bfg-repo-cleaner/
   
   # 或使用 git filter-branch
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/sensitive/file' \
     --prune-empty --tag-name-filter cat -- --all
   
   # 强制推送（危险！）
   git push --force --all
   ```

3. **通知用户**（如果已经有人 fork 了）

## 📈 推广技巧

### 编写优秀的 README

- ✅ 清晰的项目描述
- ✅ 视觉吸引力（徽章、截图、GIF）
- ✅ 快速开始指南
- ✅ 详细的文档链接
- ✅ 贡献指南
- ✅ 许可证信息

### 创建演示视频

使用工具如：
- Loom
- Asciinema（命令行录制）
- OBS Studio

### 写技术博客

分享：
- 为什么创建这个项目
- 遇到的挑战
- 解决方案
- 最佳实践

## 🎉 完成！

恭喜！您的项目现在已经是一个专业的开源项目了！

### 后续步骤

1. 监控 GitHub Stars 和 Forks
2. 响应社区反馈
3. 持续改进文档
4. 定期发布新版本
5. 建立社区

### 有用的资源

- [GitHub 文档](https://docs.github.com/zh)
- [开源指南](https://opensource.guide/zh-hans/)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/)

---

**祝您的开源项目取得成功！** 🚀⭐

