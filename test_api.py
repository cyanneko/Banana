"""
API测试脚本
用于测试后端API的各个端点
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """测试健康检查端点"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_users():
    """测试用户相关API"""
    print("👥 测试用户API...")
    
    # 获取所有用户
    print("获取所有用户:")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 创建新用户
    print("创建新用户:")
    new_user = {
        "name": "测试用户",
        "email": "test@example.com",
        "age": 22
    }
    try:
        response = requests.post(f"{BASE_URL}/api/users", json=new_user)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_todos():
    """测试待办事项API"""
    print("📝 测试待办事项API...")
    
    # 获取所有待办事项
    print("获取所有待办事项:")
    try:
        response = requests.get(f"{BASE_URL}/api/todos")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 创建新待办事项
    print("创建新待办事项:")
    new_todo = {
        "title": "测试任务",
        "user_id": 1,
        "completed": False
    }
    try:
        response = requests.post(f"{BASE_URL}/api/todos", json=new_todo)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def main():
    """主测试函数"""
    print("🚀 开始API测试...")
    print("=" * 50)
    
    test_health()
    test_users()
    test_todos()
    
    print("✅ 测试完成！")

if __name__ == "__main__":
    main()
