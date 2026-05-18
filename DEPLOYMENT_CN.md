# Zeabur 部署指南

## 步骤说明

### 1. Zeabur 账户注册
- 访问 https://zeabur.com
- 使用 GitHub 账号登录（推荐）
- 或使用邮箱注册

### 2. 创建新项目
- 点击 Dashboard 的 "New Project"
- 选择 "Deploy from Git"
- 选择 "GitHub" 源
- 授权 Zeabur 访问 GitHub

### 3. 选择仓库
- 搜索或选择 `resume-ai` 仓库
- 点击 "Import"

### 4. 配置环境
Zeabur 会自动检测项目类型。在项目设置中：

**Environment Variables（环境变量）**：
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxx
```

### 5. 部署
- 点击 "Deploy" 或 "Redeploy"
- 等待 3-5 分钟（国内速度很快）
- 部署完成后自动生成公网 URL

### 6. 访问应用
- 前端：访问 Zeabur 生成的 URL
- API：`https://your-domain.zeabur.app/api/analyze` 等

## Zeabur 优势

✅ 国内访问速度快
✅ 自动 HTTPS
✅ 无需备案
✅ 支持自动部署（GitHub Push 时自动更新）
✅ 环境变量管理方便
✅ 免费额度足够个人使用

## 遇到问题？

如果部署失败，检查：
1. 确认 requirements.txt 包含所有依赖
2. 确认 API Key 正确
3. 查看 Zeabur 的构建日志
