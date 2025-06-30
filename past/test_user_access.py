#!/usr/bin/env python3
"""
测试用户登录后访问超级管理员页面的权限提示
"""

import requests
import json

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_user_permission():
    """测试普通用户访问超级管理员页面"""
    print("🧪 测试普通用户权限提示...")
    
    # 1. 注册普通用户
    user_data = {
        'name': 'test_permission_user',  # 修正：使用name而不是username
        'account': 'test_perm_user',
        'password': 'testpass123'
    }
    
    try:
        # 注册
        reg_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/register', json=user_data)
        print(f"注册结果: {reg_response.json()}")
        
        # 登录
        login_data = {
            'account': user_data['account'],
            'password': user_data['password']
        }
        
        login_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
        login_result = login_response.json()
        print(f"登录结果: {login_result}")
        
        if login_result.get('status') == 'success':
            user_info = login_result['data']
            print(f"用户信息: {user_info}")
            
            # 2. 使用session模拟前端登录状态
            session = requests.Session()
            
            # 设置前端session (模拟POST到/api/super-admin-session但使用普通用户数据)
            session_data = {
                'user_id': user_info['id'],
                'username': user_info['name'],
                'role': user_info.get('role', 'user')  # 普通用户
            }
            
            # 尝试设置session (这应该失败，因为不是超级管理员)
            session_response = session.post(f'{FRONTEND_BASE_URL}/api/super-admin-session', json=session_data)
            print(f"会话设置结果: {session_response.status_code} - {session_response.text}")
            
            # 3. 访问超级管理员页面
            admin_response = session.get(f'{FRONTEND_BASE_URL}/super-admin')
            print(f"访问超级管理员页面: {admin_response.status_code}")
            
            if "权限不足" in admin_response.text:
                print("✅ 正确显示权限不足页面")
            elif "超级管理员登录" in admin_response.text:
                print("✅ 重定向到登录页面")
            else:
                print("❌ 权限校验可能有问题")
                
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

def test_super_admin_login_permission():
    """测试超级管理员登录时的权限校验"""
    print("\n🧪 测试超级管理员登录权限校验...")
    
    # 使用普通用户账号尝试超级管理员登录
    login_data = {
        'account': 'test_perm_user',  # 普通用户账号
        'password': 'testpass123'
    }
    
    try:
        # 直接调用登录API
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
        result = response.json()
        
        if result.get('status') == 'success':
            user_role = result['data'].get('role', 'user')
            print(f"用户角色: {user_role}")
            
            if user_role != 'super_admin':
                print("✅ 普通用户无法获得超级管理员权限")
            else:
                print("❌ 权限系统可能有问题")
        else:
            print(f"登录失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

if __name__ == '__main__':
    test_user_permission()
    test_super_admin_login_permission()
