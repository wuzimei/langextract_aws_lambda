# 更新日志

所有重要的项目更改都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- 支持更多 LLM 提供商（OpenAI, Anthropic）
- 添加结果缓存功能
- 批量处理 API
- 异步处理支持
- 监控仪表板

## [1.0.0] - 2025-10-18

### 新增
- 🎉 初始版本发布
- ✅ Lambda 函数实现（Python 3.9）
- ✅ Docker 容器化部署
- ✅ API Gateway HTTP API 集成
- ✅ API Key 认证支持
- ✅ CORS 支持
- ✅ 完整的错误处理
- ✅ 本地测试脚本
- ✅ 自动化部署脚本
- ✅ 详细的部署指南（中文）
- ✅ Next.js 集成示例
- ✅ MIT 许可证
- ✅ 贡献指南
- ✅ 安全政策

### 功能特性
- 支持 Gemini 模型（默认 gemini-2.0-flash-exp）
- 支持长文本自动分块处理
- 支持并行处理（多线程）
- 精确的源文本定位
- 详细的响应元数据

### 文档
- README.md - 项目说明和快速开始
- AWS_LAMBDA_部署指南.md - 详细部署教程
- CONTRIBUTING.md - 贡献指南
- SECURITY.md - 安全政策
- LICENSE - MIT 许可证

### 部署
- Dockerfile - 基于 AWS Lambda Python 3.9
- deploy.sh - 自动化部署脚本
- requirements.txt - Python 依赖
- .gitignore - Git 忽略配置

### 测试
- test_local.py - 本地测试脚本
- 支持 Docker 本地测试

---

## 版本说明

### 语义化版本格式

- **主版本号（MAJOR）**: 不兼容的 API 更改
- **次版本号（MINOR）**: 向后兼容的功能新增
- **修订号（PATCH）**: 向后兼容的问题修复

### 更新类型

- **新增**: 新功能
- **更改**: 现有功能的变更
- **弃用**: 即将移除的功能
- **移除**: 已移除的功能
- **修复**: Bug 修复
- **安全**: 安全性相关更新

---

[未发布]: https://github.com/yourusername/langextract_aws_lambda/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/langextract_aws_lambda/releases/tag/v1.0.0

