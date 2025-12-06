# AI Travel Agent - Docker 部署指南

## 为什么选择 Docker？

我们之前在本地运行项目时遇到了 `pyarrow` 和 `numpy` 等库的编译问题。这是因为：
1. **缺少C/C++编译器**：Windows环境中需要安装Visual Studio Build Tools
2. **复杂的依赖链**：`streamlit` 依赖的包需要编译安装

**Docker完美解决了这些问题**：
- ✅ **环境隔离**：容器内包含所有必要的编译工具和依赖
- ✅ **跨平台一致**：在Windows、macOS、Linux上行为完全一致
- ✅ **零配置**：无需安装Python、编译器或处理依赖冲突
- ✅ **易于部署**：可以轻松部署到任何Docker环境

## 部署步骤

### 方式一：使用 Docker Compose（推荐）

1. **克隆项目或准备文件**
   ```bash
   cd awesome-llm-apps/starter_ai_agents/ai_travel_agent
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   打开浏览器访问：`http://localhost:8501`

4. **停止服务**
   ```bash
   docker-compose down
   ```

### 方式二：使用 Docker 命令

1. **构建镜像**
   ```bash
   docker build -t ai-travel-agent .
   ```

2. **运行容器**
   ```bash
   docker run -p 8501:8501 ai-travel-agent
   ```

## Docker 配置说明

### Dockerfile 解析
- **基础镜像**：`python:3.11-slim` - 轻量级Python环境
- **系统依赖**：安装 `build-essential` 用于编译Python包
- **依赖安装**：使用 `requirements_simple.txt` 避免复杂依赖
- **端口暴露**：8501 (Streamlit默认端口)

### docker-compose.yml 解析
- **端口映射**：本地8501端口 → 容器8501端口
- **数据卷挂载**：可选挂载 `output` 目录保存生成的ICS文件
- **环境配置**：Streamlit服务器配置
- **重启策略**：`unless-stopped` - 容器异常退出时自动重启

## 应用功能

启动后，你将看到一个**中文界面**的AI旅行计划助手：

### 主要功能
1. **输入目的地**：支持北京、上海、杭州等预设城市
2. **选择天数**：1-30天可选择
3. **生成计划**：点击按钮立即生成详细行程
4. **下载日历**：生成.ics格式的日历文件，可导入手机/电脑日历

### 技术特点
- ✅ **无需API密钥**：完全离线运行
- ✅ **即时生成**：计划立即可用
- ✅ **日历兼容**：支持各种日历应用
- ✅ **响应式设计**：适合手机和电脑使用

## 生产部署建议

### 对于完整版项目（travel_agent.py）
如果需要运行包含真正AI Agent协作的版本，需要：

1. **修改Dockerfile**：
   ```dockerfile
   # 安装完整依赖
   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt
   
   # 启动完整版本
   CMD ["streamlit", "run", "travel_agent.py", "--server.address", "0.0.0.0"]
   ```

2. **配置API密钥**：
   ```yaml
   environment:
     - OPENAI_API_KEY=your_openai_key
     - SERPAPI_KEY=your_serpapi_key
   ```

### 安全建议
- 不要在Dockerfile中硬编码API密钥
- 使用环境变量或Docker secrets
- 考虑使用反向代理（如Nginx）处理HTTPS

## 故障排除

### 常见问题

1. **端口占用**：
   ```bash
   # 检查端口占用
   netstat -an | grep 8501
   
   # 修改端口映射
   docker run -p 8502:8501 ai-travel-agent
   ```

2. **权限问题**（Linux/macOS）：
   ```bash
   # 确保Docker有权限访问目录
   sudo chown -R $USER:$USER .
   ```

3. **内存不足**：
   ```bash
   # 增加Docker内存限制
   docker run --memory=2g -p 8501:8501 ai-travel-agent
   ```

## 优势总结

通过Docker部署，你获得了：
1. **零配置体验**：无需安装Python或处理依赖
2. **环境一致性**：开发、测试、生产环境完全一致
3. **易于维护**：更新只需重新构建镜像
4. **可移植性**：可以轻松部署到云服务或不同机器
5. **隔离性**：不会影响主机系统的Python环境

这种部署方式特别适合：
- 学习AI Agent项目
- 原型开发和测试
- 小规模生产部署
- 团队协作开发