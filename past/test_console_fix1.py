#!/usr/bin/env python3
"""
测试超级管理员控制台前端修复
"""

import requests
import time

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'

def test_super_admin_console():
    """测试超级管理员控制台访问"""
    print("🧪 测试超级管理员控制台访问...")
    
    # 使用session来模拟浏览器
    session = requests.Session()
    
    # 1. 模拟用户登录流程
    print("1. 执行超级管理员登录...")
    
    # 先调用后端API登录
    backend_login = session.post('http://127.0.0.1:5000/api/auth/login', json={
        'account': 'fhc',
        'password': '114514'
    })
    
    if backend_login.status_code == 200:
        backend_data = backend_login.json()
        print(f"   后端登录结果: {backend_data.get('message')}")
        
        if backend_data.get('status') == 'success' and backend_data['data'].get('role') == 'super_admin':
            # 设置前端session
            session_response = session.post(f'{FRONTEND_BASE_URL}/api/super-admin-session', json={
                'user_id': backend_data['data']['id'],
                'username': backend_data['data']['name'],
                'role': backend_data['data']['role']
            })
            
            print(f"   前端session设置: {session_response.json().get('message')}")
            
            # 2. 访问超级管理员控制台
            print("2. 访问超级管理员控制台页面...")
            console_response = session.get(f'{FRONTEND_BASE_URL}/super-admin')
            print(f"   页面访问状态码: {console_response.status_code}")
            
            # 3. 测试登录状态检查API
            print("3. 测试登录状态检查...")
            status_response = session.get(f'{FRONTEND_BASE_URL}/api/check-super-admin-status')
            status_data = status_response.json()
            print(f"   登录状态: {'已登录' if status_data.get('logged_in') else '未登录'}")
            
            if status_data.get('logged_in') and status_data.get('role') == 'super_admin':
                print("   ✅ 用户状态正确，页面应显示控制台")
                return True
            else:
                print("   ❌ 用户状态异常")
        else:
            print("   ❌ 后端登录失败或权限不足")
    else:
        print("   ❌ 后端登录请求失败")
    
    return False

def main():
    print("🚀 测试超级管理员控制台前端修复...")
    print("=" * 60)
    
    # 检查服务器状态
    try:
        frontend_health = requests.get(f'{FRONTEND_BASE_URL}/', timeout=5)
        backend_health = requests.get('http://127.0.0.1:5000/health', timeout=5)
        
        if frontend_health.status_code != 200:
            print("❌ 前端服务器未运行")
            return
            
        if backend_health.status_code != 200:
            print("❌ 后端服务器未运行")  
            return
            
        print("✅ 服务器状态正常")
        
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return
    
    # 运行测试
    result = test_super_admin_console()
    
    print("\n" + "=" * 60)
    if result:
        print("🎉 超级管理员控制台修复成功！")
        print("\n📝 现在的工作流程:")
        print("1. 访问 http://127.0.0.1:3000/super-admin")
        print("2. 如果未登录，页面会显示登录表单")
        print("3. 登录成功后，页面会自动切换到控制台界面")
        print("4. JavaScript会自动检查登录状态并显示相应内容")
    else:
        print("❌ 测试未通过，请检查相关配置")

if __name__ == '__main__':
    main()
