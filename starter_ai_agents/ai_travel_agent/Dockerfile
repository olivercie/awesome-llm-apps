# 使用官方的Python 3.11镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖 (一些包编译时可能需要)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements_simple.txt requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements_simple.txt

# 复制应用代码
COPY . .

# 暴露Streamlit的默认端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "simple_travel_agent.py", "--server.address", "0.0.0.0"]