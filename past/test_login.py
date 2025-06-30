#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能 - 验证超级管理员、管理员、普通用户的角色识别
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_login(account, password, expected_role):
    """测试登录功能"""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "account": account,
        "password": password
    }
    
    print(f"\n🔍 测试登录: {account}")
    print(f"🎯 预期角色: {expected_role}")
    
    try:
        response = requests.post(url, json=data)
        print(f"📊 状态码: {response.status_code}")
        
        result = response.json()
        print(f"📋 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get('status') == 'success':
            role = result.get('data', {}).get('role')
            print(f"✅ 实际角色: {role}")
            if role == expected_role:
                print("✅ 角色识别正确!")
            else:
                print(f"❌ 角色识别错误，期望 {expected_role}，实际 {role}")
        else:
            print("❌ 登录失败")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

def main():
    print("🎯 登录功能和角色识别测试")
    print("="*50)
    
    # 测试超级管理员登录
    test_login("fhc", "114514", "super_admin")
    
    # 创建一个管理员账号来测试
    print("\n📝 创建测试管理员...")
    try:
        response = requests.post(f"{BASE_URL}/api/super-admin/admins", json={
            "super_admin_id": 1,
            "name": "测试管理员",
            "account": "test_admin",
            "password": "admin123"
        })
        if response.status_code == 201:
            print("✅ 测试管理员创建成功")
            # 测试管理员登录
            test_login("test_admin", "admin123", "admin")
            
            # 清理 - 删除测试管理员
            admin_data = response.json().get('data', {})
            admin_id = admin_data.get('id')
            if admin_id:
                requests.delete(f"{BASE_URL}/api/super-admin/admins/{admin_id}", json={
                    "super_admin_id": 1
                })
                print("🧹 测试管理员已清理")
        else:
            print("❌ 测试管理员创建失败")
    except Exception as e:
        print(f"❌ 管理员测试失败: {e}")
    
    # 创建一个普通用户来测试
    print("\n📝 创建测试用户...")
    try:
        response = requests.post(f"{BASE_URL}/api/super-admin/users", json={
            "super_admin_id": 1,
            "name": "测试用户",
            "account": "test_user",
            "password": "user123"
        })
        if response.status_code == 201:
            print("✅ 测试用户创建成功")
            # 测试用户登录
            test_login("test_user", "user123", "user")
            
            # 清理 - 删除测试用户
            user_data = response.json().get('data', {})
            user_id = user_data.get('id')
            if user_id:
                requests.delete(f"{BASE_URL}/api/super-admin/users/{user_id}", json={
                    "super_admin_id": 1
                })
                print("🧹 测试用户已清理")
        else:
            print("❌ 测试用户创建失败")
    except Exception as e:
        print(f"❌ 用户测试失败: {e}")
    
    # 测试错误登录
    test_login("nonexistent", "wrongpassword", "none")
    
    print("\n" + "="*50)
    print("✅ 登录功能测试完成!")

if __name__ == "__main__":
    main()
