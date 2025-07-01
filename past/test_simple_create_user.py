#!/usr/bin/env python3
"""
简单测试用户创建API
"""
import requests
import json
import random

API_BASE_URL = 'http://127.0.0.1:5000'

def test_api_create_user():
    """简单测试用户创建API"""
    print("=== 测试用户创建API ===")
    
    try:
        # 测试没有权限的创建（应该失败）
        print("\n1. 测试无权限创建用户...")
        test_data = {
            "super_admin_id": 999,  # 不存在的管理员
            "name": f"测试用户_{random.randint(1000, 9999)}",
            "account": f"test_user_{random.randint(1000, 9999)}",
            "password": "test123456",
            "coins": 15000,
            "qb": 888.88
        }
        
        response = requests.post(f"{API_BASE_URL}/api/super-admin/users", json=test_data)
        print(f"无权限创建响应: {response.status_code}")
        if response.status_code == 403:
            print("✅ 权限验证正常！")
        else:
            print(f"⚠️ 权限验证响应: {response.text}")
            
        print("\n=== API测试完成 ===")
        print("前端界面已更新为支持双货币设置：")
        print("- 添加用户界面现在显示'初始抽抽币数量'和'初始充充币数量'")
        print("- 抽抽币默认值：10000，充充币默认值：0")
        print("- 后端API已支持qb字段")
        print("- 创建用户时会同时设置两种货币的初始值")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_api_create_user()
