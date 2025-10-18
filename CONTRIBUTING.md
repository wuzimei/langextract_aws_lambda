# 贡献指南

感谢您考虑为 LangExtract AWS Lambda 项目做出贡献！

## 行为准则

请保持友好和尊重。我们致力于为所有人提供一个友好的环境。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请创建一个 Issue，并包含：

- **清晰的标题** - 简明扼要地描述问题
- **重现步骤** - 详细列出如何重现问题
- **预期行为** - 您认为应该发生什么
- **实际行为** - 实际发生了什么
- **环境信息** - Python 版本、AWS 区域、Lambda 配置等
- **日志和错误信息** - 相关的 CloudWatch 日志或错误消息

**Issue 模板示例：**

```markdown
**问题描述**
简要描述问题

**重现步骤**
1. 配置 Lambda 函数为...
2. 发送请求...
3. 看到错误...

**预期行为**
应该返回...

**实际行为**
返回了...

**环境**
- Python 版本: 3.9
- AWS 区域: us-east-1
- Lambda 内存: 1024MB
- 模型: gemini-2.0-flash-exp

**日志**
```
粘贴相关日志
```
```

### 提出新功能

如果您有功能建议，请创建一个 Issue 并说明：

- **功能描述** - 详细描述您想要的功能
- **使用场景** - 为什么需要这个功能？
- **替代方案** - 您考虑过的其他解决方案
- **其他信息** - 任何相关的上下文或截图

### 提交代码

我们欢迎 Pull Requests！

#### 开发流程

1. **Fork 仓库**

   点击 GitHub 页面右上角的 "Fork" 按钮

2. **克隆您的 Fork**

   ```bash
   git clone https://github.com/your-username/langextract_aws_lambda.git
   cd langextract_aws_lambda
   ```

3. **创建分支**

   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

   分支命名规范：
   - `feature/` - 新功能
   - `fix/` - Bug 修复
   - `docs/` - 文档更新
   - `refactor/` - 代码重构
   - `test/` - 测试相关

4. **设置开发环境**

   ```bash
   # 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或
   venv\Scripts\activate  # Windows

   # 安装依赖
   pip install langextract
   pip install pytest pylint black isort  # 开发工具

   # 复制环境变量模板
   cp env.example.txt .env
   # 填入您的配置
   ```

5. **进行更改**

   - 编写清晰、有注释的代码
   - 遵循 Python PEP 8 风格指南
   - 添加或更新相关文档
   - 编写或更新测试（如果适用）

6. **代码格式化**

   ```bash
   # 格式化代码
   black lambda_function.py test_local.py
   isort lambda_function.py test_local.py

   # 运行 linter
   pylint lambda_function.py
   ```

7. **测试更改**

   ```bash
   # 运行本地测试
   export GEMINI_API_KEY='your-test-api-key'
   python test_local.py

   # 运行 Docker 测试（可选）
   docker build --platform linux/amd64 -t langextract-lambda:test .
   docker run -p 9000:8080 -e GEMINI_API_KEY='your-key' langextract-lambda:test
   ```

8. **提交更改**

   ```bash
   git add .
   git commit -m "feat: 添加新功能的简短描述"
   ```

   提交信息规范：
   - `feat:` - 新功能
   - `fix:` - Bug 修复
   - `docs:` - 文档更新
   - `style:` - 代码格式化
   - `refactor:` - 代码重构
   - `test:` - 添加测试
   - `chore:` - 构建/工具更改

9. **推送到您的 Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

10. **创建 Pull Request**

    - 访问 GitHub 上的原仓库
    - 点击 "New Pull Request"
    - 选择您的分支
    - 填写 PR 描述（见下方模板）
    - 提交 PR

#### Pull Request 模板

```markdown
## 更改描述

简要描述您的更改

## 更改类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 其他（请说明）

## 相关 Issue

Closes #issue_number

## 测试

描述您如何测试这些更改：

- [ ] 本地 Python 测试通过
- [ ] Docker 测试通过
- [ ] 在 AWS Lambda 上测试通过
- [ ] 添加了新的测试

## 检查清单

- [ ] 代码遵循项目的代码风格
- [ ] 已运行 linter 检查
- [ ] 已更新相关文档
- [ ] 所有测试通过
- [ ] 提交信息清晰明确
```

## 代码风格

### Python 风格

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用 4 个空格缩进（不使用 Tab）
- 最大行长度 88 字符（Black 默认）
- 使用有意义的变量和函数名
- 添加文档字符串（docstrings）

**示例：**

```python
def process_extraction(text: str, prompt: str, examples: list) -> dict:
    """
    处理信息提取请求
    
    参数:
        text (str): 输入文本
        prompt (str): 提取任务描述
        examples (list): 示例数据
    
    返回:
        dict: 提取结果
    """
    # 实现代码
    pass
```

### 文档风格

- 使用清晰的标题和子标题
- 提供代码示例
- 包含实际的使用场景
- 保持简洁但完整

## 开发工具

### 推荐的 IDE 设置

**VS Code**

安装扩展：
- Python
- Pylance
- Black Formatter
- isort

`.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.sortImports.path": "isort"
}
```

**PyCharm**

- 启用 Black 集成
- 配置 PEP 8 检查
- 启用自动导入排序

## 测试指南

### 单元测试

```python
# 添加到 tests/ 目录
import unittest
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_missing_text(self):
        event = {'body': '{"prompt": "test"}'}
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
```

### 集成测试

在 AWS 环境中测试：

```bash
aws lambda invoke \
  --function-name langextract-function \
  --payload file://test-event.json \
  response.json
```

## 文档贡献

文档和代码一样重要！

### 需要文档的地方

- **README.md** - 项目概述和快速开始
- **AWS_LAMBDA_部署指南.md** - 详细部署步骤
- **代码注释** - 解释复杂逻辑
- **API 文档** - 端点、参数、响应格式
- **故障排查** - 常见问题和解决方案

### 文档更新流程

1. 在与代码相同的 PR 中更新文档
2. 确保示例代码可以运行
3. 检查拼写和语法
4. 保持中英文文档同步（如果适用）

## 发布流程

（维护者使用）

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 发布 GitHub Release

## 问题和讨论

- **Bug 报告**: 使用 GitHub Issues
- **功能建议**: 使用 GitHub Issues
- **问题求助**: 使用 GitHub Discussions
- **安全问题**: 请通过私人渠道联系维护者

## 许可证

提交贡献即表示您同意您的贡献将在 MIT 许可证下发布。

## 联系方式

- **GitHub Issues**: 用于 bug 报告和功能请求
- **GitHub Discussions**: 用于一般性讨论和问题

## 致谢

感谢所有贡献者！每一个贡献，无论大小，都让这个项目变得更好。

---

**再次感谢您的贡献！** 🎉

