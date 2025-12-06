# TripCraft AI - 多代理旅行规划系统部署指南

## 🏗️ 项目概述

TripCraft AI是一个基于Agno框架的高级多代理旅行规划系统，包含6个专业AI代理协作：
- 🗺️ **目的地探索代理** (destination_agent)
- 🏨 **酒店搜索代理** (hotel_search_agent)  
- 🍽️ **餐饮代理** (dining_agent)
- 💰 **预算代理** (budget_agent)
- ✈️ **航班搜索代理** (flight_search_agent)
- 📋 **行程规划专家** (itinerary_agent)

## 🛠️ 技术架构

- **前端**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **后端**: Python 3.12+ + FastAPI + Agno框架
- **数据库**: PostgreSQL + Prisma ORM
- **AI代理**: Agno多代理协作系统
- **外部API**: Bright Data、OpenRouter、OpenAI、Cloudflare R2、Exa、FireCrawl

## 🚀 部署方案

### 方案1: 本地开发部署 (Windows优化)

#### 系统要求
- Windows 10/11
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Git

#### 步骤1: 环境准备
```bash
# 1. 安装Python 3.12+
# 下载 https://www.python.org/downloads/windows/

# 2. 安装Node.js
# 下载 https://nodejs.org/

# 3. 安装PostgreSQL
# 下载 https://www.postgresql.org/download/windows/

# 4. 安装Git (如果未安装)
# 下载 https://git-scm.com/download/win
```

#### 步骤2: 克隆项目
```bash
# 进入工作目录
cd c:/Users/Administrator/Desktop/LLM2025

# 克隆项目 (如果需要)
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/advanced_ai_agents/multi_agent_apps/agent_teams/ai_travel_planner_agent_team
```

#### 步骤3: 后端设置
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\\Scripts\\activate

# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件，配置必要的API密钥
```

#### 步骤4: 前端设置
```bash
# 打开新终端，进入前端目录
cd client

# 安装pnpm (如果未安装)
npm install -g pnpm

# 安装依赖
pnpm install

# 复制环境变量模板
copy .env.local.example .env.local (如果存在)
```

#### 步骤5: 数据库设置
```bash
# 创建PostgreSQL数据库
psql -U postgres -c "CREATE DATABASE tripcraft_ai;"

# 运行迁移 (如果使用Prisma)
cd backend
npx prisma migrate dev
npx prisma generate
```

#### 步骤6: 启动服务
```bash
# 后端服务 (终端1)
cd backend
venv\\Scripts\\activate
python main.py

# 前端服务 (终端2)  
cd client
pnpm dev
```

### 方案2: Docker容器化部署

#### Docker Compose配置
创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: tripcraft_ai
      POSTGRES_USER: tripcraft
      POSTGRES_PASSWORD: tripcraft_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://tripcraft:tripcraft_password@postgres:5432/tripcraft_ai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - BRIGHT_DATA_API_TOKEN=${BRIGHT_DATA_API_TOKEN}
      - BRIGHT_DATA_BROWSER_AUTH=${BRIGHT_DATA_BROWSER_AUTH}
      - CLOUDFLARE_ACCOUNT_ID=${CLOUDFLARE_ACCOUNT_ID}
      - CLOUDFLARE_R2_ACCESS_KEY_ID=${CLOUDFLARE_R2_ACCESS_KEY_ID}
      - CLOUDFLARE_R2_SECRET_ACCESS_KEY=${CLOUDFLARE_R2_SECRET_ACCESS_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
      - FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    volumes:
      - ./backend:/app

  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### 启动Docker部署
```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方案3: 云端部署方案

#### Vercel + Railway部署
1. **前端部署到Vercel**:
   ```bash
   cd client
   vercel deploy --prod
   ```

2. **后端部署到Railway**:
   ```bash
   cd backend
   railway deploy
   ```

3. **数据库部署到Railway/Supabase**:
   - 创建PostgreSQL实例
   - 配置数据库连接字符串

#### AWS部署
使用AWS EKS、ECS或Lambda进行部署。

## ⚙️ 配置指南

### API密钥配置

编辑 `backend/.env` 文件：

```bash
# Bright Data (网页数据采集)
BRIGHT_DATA_API_TOKEN=your_bright_data_api_token
BRIGHT_DATA_BROWSER_AUTH=your_bright_data_browser_auth

# 数据库连接
DATABASE_URL=postgresql://tripcraft:tripcraft_password@localhost:5432/tripcraft_ai

# OpenRouter (AI模型访问)
OPENROUTER_API_KEY=your_openrouter_api_key

# OpenAI (GPT模型)
OPENAI_API_KEY=your_openai_api_key

# Cloudflare R2 (文件存储)
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_R2_ACCESS_KEY_ID=your_r2_access_key_id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_r2_secret_access_key

# Exa (搜索引擎)
EXA_API_KEY=your_exa_api_key

# FireCrawl (网页抓取)
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

### API密钥获取指南

1. **OpenRouter API**:
   - 访问 https://openrouter.ai/
   - 注册账户并获取API密钥
   - 用于访问各种AI模型

2. **OpenAI API**:
   - 访问 https://platform.openai.com/
   - 创建API密钥
   - 用于GPT模型访问

3. **Bright Data**:
   - 访问 https://brightdata.com/
   - 注册开发者账户
   - 用于网页数据采集

4. **Exa API**:
   - 访问 https://exa.ai/
   - 获取API密钥
   - 用于智能搜索

5. **FireCrawl API**:
   - 访问 https://firecrawl.dev/
   - 注册并获取API密钥
   - 用于网页内容抓取

6. **Cloudflare R2**:
   - 在Cloudflare控制台创建R2存储桶
   - 获取访问密钥和密钥ID

## 🧪 测试验证

### 1. 健康检查
```bash
# 检查API服务
curl http://localhost:8000/api/health

# 预期响应
{
  "status": "healthy",
  "timestamp": "2025-11-16T07:41:17.823Z"
}
```

### 2. 前端访问
- 打开浏览器访问 http://localhost:3000
- 验证TripCraft AI界面加载

### 3. 代理系统测试
发送旅行规划请求到后端API：
```bash
curl -X POST http://localhost:8000/api/plan \\
  -H "Content-Type: application/json" \\
  -d '{
    "destination": "Tokyo",
    "start_date": "2025-12-01",
    "end_date": "2025-12-07",
    "travel_style": "cultural",
    "budget": "mid-range"
  }'
```

### 4. 数据库连接测试
```python
# 在backend目录创建test_db.py
import asyncio
from sqlalchemy import text

async def test_db():
    from services.db_service import engine
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("数据库连接成功:", result.fetchone()[0])

if __name__ == "__main__":
    asyncio.run(test_db())
```

## 🛠️ 故障排除

### 常见问题

1. **Python 3.12+要求**:
   ```bash
   # 检查Python版本
   python --version
   
   # 如果版本过低，升级Python到3.12+
   ```

2. **PostgreSQL连接问题**:
   ```bash
   # 测试数据库连接
   psql -h localhost -U postgres -d tripcraft_ai
   ```

3. **依赖安装失败**:
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 清理缓存
   pip cache purge
   
   # 重新安装
   pip install -r requirements.txt
   ```

4. **端口冲突**:
   - 确保端口3000和8000未被占用
   ```bash
   # 查看端口占用
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   ```

5. **权限问题** (Windows):
   ```bash
   # 以管理员身份运行命令提示符
   # 或在PowerShell中以管理员身份运行
   ```

### 性能优化

1. **数据库优化**:
   - 启用PostgreSQL连接池
   - 配置适当的缓存策略

2. **API优化**:
   - 使用异步处理
   - 实现请求限流

3. **前端优化**:
   - 启用Next.js Turbopack
   - 配置CDN加速

## 📝 开发建议

1. **环境隔离**:
   - 使用虚拟环境隔离Python依赖
   - 使用不同数据库进行开发和生产环境

2. **监控和日志**:
   - 配置Loguru日志记录
   - 实施健康检查和监控

3. **安全性**:
   - 安全存储API密钥
   - 配置CORS策略
   - 实施输入验证

4. **备份策略**:
   - 定期备份PostgreSQL数据库
   - 备份配置文件和自定义设置

## 📞 支持

如有问题，请：
1. 检查系统要求和依赖
2. 查看详细日志
3. 参考官方文档
4. 联系开发团队

---

*此部署指南基于2025年11月16日的项目状态，建议定期更新以适应新的依赖和API变化。*