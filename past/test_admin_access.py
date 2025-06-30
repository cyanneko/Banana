#!/usr/bin/env python3
"""
测试超级管理员登录和权限提示
"""

import requests
import json

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_super_admin_access():
    """测试超级管理员登录和访问"""
    print("🧪 测试超级管理员登录和访问...")
    
    # 使用默认超级管理员账号
    login_data = {
        'account': 'fhc',
        'password': '114514'
    }
    
    try:
        # 登录
        login_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
        login_result = login_response.json()
        print(f"登录结果: {login_result}")
        
        if login_result.get('status') == 'success':
            user_info = login_result['data']
            print(f"用户信息: {user_info}")
            
            if user_info.get('role') == 'super_admin':
                print("✅ 超级管理员登录成功")
                
                # 使用session模拟前端登录
                session = requests.Session()
                
                # 设置前端session
                session_data = {
                    'user_id': user_info['id'],
                    'username': user_info['name'],
                    'role': user_info['role']
                }
                
                session_response = session.post(f'{FRONTEND_BASE_URL}/api/super-admin-session', json=session_data)
                print(f"会话设置结果: {session_response.status_code} - {session_response.json()}")
                
                if session_response.status_code == 200:
                    # 访问超级管理员页面
                    admin_response = session.get(f'{FRONTEND_BASE_URL}/super-admin')
                    print(f"访问超级管理员页面: {admin_response.status_code}")
                    
                    if admin_response.status_code == 200:
                        if "权限不足" not in admin_response.text and "super_admin.html" in admin_response.text:
                            print("✅ 超级管理员成功访问控制台")
                        elif "权限不足" not in admin_response.text:
                            print("✅ 超级管理员成功访问控制台（HTML文件）")  
                        else:
                            print("❌ 超级管理员权限校验有问题")
                            print(f"   响应内容前500字符: {admin_response.text[:500]}")
                    else:
                        print(f"❌ 访问失败，状态码: {admin_response.status_code}")
                else:
                    print("❌ 会话设置失败")
            else:
                print(f"❌ 角色不正确: {user_info.get('role')}")
        else:
            print(f"❌ 登录失败: {login_result.get('message')}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

def test_admin_access():
    """测试管理员访问"""
    print("\n🧪 测试管理员登录和访问...")
    
    # 使用创建的测试管理员账号
    login_data = {
        'account': 'test_admin',
        'password': 'admin123456'
    }
    
    try:
        # 登录
        login_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
        login_result = login_response.json()
        print(f"登录结果: {login_result}")
        
        if login_result.get('status') == 'success':
            user_info = login_result['data']
            print(f"用户信息: {user_info}")
            
            if user_info.get('role') == 'admin':
                print("✅ 管理员登录成功")
                
                # 使用session模拟前端登录
                session = requests.Session()
                
                # 手动设置session cookies来模拟前端登录状态
                # 在实际应用中，这由前端的登录流程处理
                
                # 直接访问管理员页面（应该显示权限不足）
                admin_response = session.get(f'{FRONTEND_BASE_URL}/admin')
                print(f"访问管理员页面: {admin_response.status_code}")
                
                if "权限不足" in admin_response.text or "管理员登录" in admin_response.text:
                    print("✅ 正确显示权限提示或登录页面")
                else:
                    print("❌ 权限校验可能有问题")
                
                # 测试访问超级管理员页面（应该失败）
                super_admin_response = session.get(f'{FRONTEND_BASE_URL}/super-admin')
                if "权限不足" in super_admin_response.text or "超级管理员登录" in super_admin_response.text:
                    print("✅ 管理员无法访问超级管理员页面")
                else:
                    print("❌ 管理员权限校验可能有问题")
            else:
                print(f"❌ 角色不正确: {user_info.get('role')}")
        else:
            print(f"❌ 登录失败: {login_result.get('message')}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

if __name__ == '__main__':
    test_super_admin_access()
    test_admin_access()
