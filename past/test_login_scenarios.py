#!/usr/bin/env python3 
"""
测试超级管理员登录的各种场景
"""

import requests
import json

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_valid_login():
    """测试有效登录"""
    print("🧪 测试1: 有效的超级管理员登录")
    
    data = {
        'account': 'fhc',
        'password': '114514'
    }
    
    try:
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=data)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        if result.get('status') == 'success' and result['data'].get('role') == 'super_admin':
            print("✅ 有效登录测试通过")
            return True
        else:
            print("❌ 有效登录测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def test_invalid_login():
    """测试无效登录"""
    print("\n🧪 测试2: 无效的登录信息")
    
    data = {
        'account': 'wrong_user',
        'password': 'wrong_password'
    }
    
    try:
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=data)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        if response.status_code == 401 and result.get('status') == 'error':
            print("✅ 无效登录测试通过")
            return True
        else:
            print("❌ 无效登录测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def test_missing_fields():
    """测试缺少字段"""
    print("\n🧪 测试3: 缺少必要字段")
    
    data = {
        'account': 'fhc'
        # 缺少password字段
    }
    
    try:
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=data)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        if response.status_code == 400 and result.get('status') == 'error':
            print("✅ 缺少字段测试通过")
            return True
        else:
            print("❌ 缺少字段测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def test_user_login():
    """测试普通用户登录（但权限不足）"""
    print("\n🧪 测试4: 普通用户登录")
    
    # 先注册一个普通用户
    register_data = {
        'name': 'test_user_login',
        'account': 'test_user_login',
        'password': 'testpass123'
    }
    
    try:
        # 注册
        reg_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/register', json=register_data)
        print(f"注册状态: {reg_response.status_code}")
        
        # 登录
        login_data = {
            'account': 'test_user_login',
            'password': 'testpass123'
        }
        
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
        result = response.json()
        
        print(f"登录状态码: {response.status_code}")
        print(f"登录响应: {result}")
        
        if result.get('status') == 'success' and result['data'].get('role') == 'user':
            print("✅ 普通用户登录测试通过（但权限不足访问超级管理员功能）")
            return True
        else:
            print("❌ 普通用户登录测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def main():
    print("🚀 开始测试超级管理员登录的各种场景...")
    print("=" * 60)
    
    tests = [
        test_valid_login,
        test_invalid_login,
        test_missing_fields,
        test_user_login
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！登录功能工作正常。")
    else:
        print("⚠️ 部分测试未通过，请检查相关功能。")

if __name__ == '__main__':
    main()
