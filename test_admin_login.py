#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试管理员登录流程
"""

import requests
import json

# API基础URL
API_BASE = 'http://127.0.0.1:5000'

def test_admin_login():
    """测试管理员登录"""
    print("=== 测试管理员登录流程 ===")
    
    # 测试管理员登录
    print("\n1. 测试管理员登录...")
    admin_login_data = {
        "account": "fhc",
        "password": "114514"
    }
    
    response = requests.post(f"{API_BASE}/api/auth/login", json=admin_login_data)
    print(f"登录响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        login_result = response.json()
        print(f"登录结果: {json.dumps(login_result, indent=2, ensure_ascii=False)}")
        
        if login_result['status'] == 'success':
            user_data = login_result['data']
            print(f"用户角色: {user_data.get('role', '未知')}")
            
            if user_data.get('role') == 'admin':
                print("✓ 管理员登录成功，角色验证正确")
            elif user_data.get('role') == 'super_admin':
                print("✓ 超级管理员登录成功，角色验证正确")
            else:
                print(f"✗ 角色验证失败，当前角色: {user_data.get('role')}")
        else:
            print(f"✗ 登录失败: {login_result['message']}")
    else:
        print(f"✗ 登录请求失败: {response.text}")
    
    # 测试普通用户登录（应该不能进入管理员界面）
    print("\n2. 测试普通用户登录...")
    user_login_data = {
        "account": "test1",
        "password": "123456"
    }
    
    response = requests.post(f"{API_BASE}/api/auth/login", json=user_login_data)
    print(f"普通用户登录响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        login_result = response.json()
        print(f"普通用户登录结果: {json.dumps(login_result, indent=2, ensure_ascii=False)}")
        
        if login_result['status'] == 'success':
            user_data = login_result['data']
            role = user_data.get('role', '未知')
            print(f"用户角色: {role}")
            
            if role == 'user':
                print("✓ 普通用户登录成功，角色验证正确（应该无法进入管理员界面）")
            else:
                print(f"✗ 普通用户角色异常: {role}")
        else:
            print(f"✗ 普通用户登录失败: {login_result['message']}")
    else:
        print(f"✗ 普通用户登录请求失败: {response.text}")

def test_invalid_admin_login():
    """测试无效的管理员登录"""
    print("\n3. 测试无效的管理员登录...")
    
    invalid_credentials = [
        {"account": "fhc", "password": "wrongpassword"},
        {"account": "wrongaccount", "password": "114514"},
        {"account": "admin", "password": "admin"}
    ]
    
    for cred in invalid_credentials:
        print(f"\n测试无效凭据: {cred['account']}/{cred['password']}")
        
        response = requests.post(f"{API_BASE}/api/auth/login", json=cred)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'error':
                print(f"✓ 正确拒绝无效登录: {result['message']}")
            else:
                print(f"✗ 意外的成功登录: {result}")
        else:
            print(f"✓ 正确拒绝无效登录: HTTP {response.status_code}")

if __name__ == "__main__":
    test_admin_login()
    test_invalid_admin_login()
    print("\n=== 测试完成 ===")
    print("\n使用说明:")
    print("1. 管理员可以使用 fhc/114514 登录")
    print("2. 访问 admin_login.html 进行管理员登录")
    print("3. 登录成功后会自动跳转到 admin.html")
    print("4. 直接访问 admin.html 会检查登录状态，未登录会重定向到登录页面")
