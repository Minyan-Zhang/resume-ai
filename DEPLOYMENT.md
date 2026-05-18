# 部署指南 | Deployment Guide

## 快速部署到 Vercel (Quick Deploy to Vercel)

### 步骤 1: 推送更新到 GitHub

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### 步骤 2: 导入到 Vercel

1. 访问 https://vercel.com/new
2. 选择 "Import Git Repository"
3. 输入你的 GitHub 仓库 URL：`https://github.com/Minyan-Zhang/resume-ai`
4. 点击 "Import"

### 步骤 3: 配置环境变量

在 Vercel 的 "Environment Variables" 部分添加：

- **变量名**: `ANTHROPIC_API_KEY`
- **值**: 你的 Anthropic API Key (从 https://console.anthropic.com 获取)

### 步骤 4: 部署

1. 点击 "Deploy"
2. 等待部署完成（通常需要 2-3 分钟）
3. 获得你的部署 URL，例如：`https://resume-ai-xxxxx.vercel.app`

### 步骤 5: 使用应用

部署完成后，你可以：
- 直接访问 HTML 前端：`https://resume-ai-xxxxx.vercel.app`
- 调用 API 端点：
  - `POST /api/analyze` - 完整评估
  - `POST /api/parse-resume` - 仅解析简历
  - `POST /api/parse-jd` - 仅解析 JD

## 替代部署方案 | Alternative Deployment Options

### 使用 Railway 部署

Railway 对 Python 应用的支持更好，推荐用于全栈部署。

1. 访问 https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub"
4. 授权并选择 `resume-ai` 仓库
5. 添加环境变量 `ANTHROPIC_API_KEY`
6. 在 `requirements.txt` 下添加 Python 版本指定：

```
python-3.11
```

7. 部署完成后，Railway 会分配一个 URL

### 本地测试 | Local Testing

部署前，可以在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ANTHROPIC_API_KEY=sk-ant-xxx

# 启动本地服务器
uvicorn api.index:app --reload

# 访问 http://127.0.0.1:8000
```

## 常见问题 | FAQ

**Q: API Key 是否安全？**
A: 是的。API Key 存储在 Vercel 的安全环境变量中，不会被暴露。

**Q: 可以离线使用吗？**
A: 否，需要 Anthropic API Key 和网络连接来调用 Claude。

**Q: 使用成本是多少？**
A: 取决于 Claude API 的调用量。详见 https://www.anthropic.com/pricing

**Q: 我的简历数据会被保存吗？**
A: 否，数据只在处理时使用，不会被存储。

## 支持 | Support

如有问题，请：
1. 检查 Vercel/Railway 的部署日志
2. 确认 API Key 是否有效
3. 在 GitHub 上提交 Issue
