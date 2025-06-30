"""
服务器启动脚本
"""

import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False
    return True

def start_server():
    """启动服务器"""
    print("🚀 启动后端服务器...")
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("Python后端服务器启动器")
    print("=" * 30)
    
    # 检查是否存在requirements.txt
    if not os.path.exists("requirements.txt"):
        print("❌ 找不到requirements.txt文件")
        return
    
    # 询问是否要安装依赖
    install = input("是否需要安装/更新依赖包？(y/n): ").lower()
    if install in ['y', 'yes', '是']:
        if not install_requirements():
            return
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()
