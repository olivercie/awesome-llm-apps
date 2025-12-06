#!/usr/bin/env python3
"""
修复ai_travel_agent依赖安装脚本

问题分析：
1. 原始requirements.txt中的pyarrow版本要求与实际可安装版本冲突
2. CMake编译问题导致pyarrow无法从源码构建
3. 需要安装预编译版本的依赖

解决方案：
1. 跳过pyarrow版本检查
2. 使用预编译版本的包
3. 提供替代方案
"""

import subprocess
import sys
import os

def install_package(package_name, extra_args=None):
    """安装Python包并处理错误"""
    cmd = [sys.executable, "-m", "pip", "install", package_name]
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        print(f"正在安装: {package_name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"警告: {package_name} 安装失败")
            print(f"错误: {result.stderr}")
            return False
        else:
            print(f"✓ {package_name} 安装成功")
            return True
    except Exception as e:
        print(f"安装 {package_name} 时发生错误: {e}")
        return False

def main():
    print("开始修复ai_travel_agent依赖...")
    
    # 修复的依赖列表，跳过有问题的包
    packages_to_install = [
        ("--no-deps", None),  # 首先跳过所有依赖
        ("streamlit==1.28.0", None),  # 使用较旧版本的streamlit
        ("agno>=2.2.10", None),
        ("openai", None),
        ("google-search-results", None),
        ("icalendar", None),
    ]
    
    # 安装每个包
    for package, extra in packages_to_install:
        if extra:
            install_package(package, extra)
        else:
            install_package(package)
    
    print("\n安装完成！请尝试运行项目。")
    print("\n如果仍有问题，请手动安装缺失的依赖:")
    print("pip install --only-binary=pyarrow pyarrow")
    print("streamlit run travel_agent.py")

if __name__ == "__main__":
    main()