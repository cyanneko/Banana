#!/usr/bin/env python3
"""
测试超级管理员登录修复
"""

import requests
import time

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_backend_login_api():
    """测试后端登录API是否正常"""
    print("🧪 测试后端登录API...")
    
    try:
        # 测试超级管理员登录
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json={
            'account': 'fhc',
            'password': '114514'
        })
        
        print(f"后端API响应状态: {response.status_code}")
        print(f"后端API响应内容: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success' and result['data'].get('role') == 'super_admin':
                print("✅ 后端登录API正常工作")
                return True
            else:
                print("❌ 后端登录API返回错误")
        else:
            print("❌ 后端登录API状态码错误")
            
    except Exception as e:
        print(f"❌ 后端API测试失败: {e}")
    
    return False

def test_frontend_session_api():
    """测试前端session设置API"""
    print("\n🧪 测试前端session设置API...")
    
    try:
        response = requests.post(f'{FRONTEND_BASE_URL}/api/super-admin-session', json={
            'user_id': 1,
            'username': 'fhc',
            'role': 'super_admin'
        })
        
        print(f"前端session API响应状态: {response.status_code}")
        print(f"前端session API响应内容: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 前端session API正常工作")
            return True
        else:
            print("❌ 前端session API状态码错误")
            
    except Exception as e:
        print(f"❌ 前端session API测试失败: {e}")
    
    return False

def test_cross_origin():
    """测试跨域请求"""
    print("\n🧪 测试跨域请求...")
    
    try:
        # 模拟前端JavaScript的跨域请求
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://127.0.0.1:3000'
        }
        
        response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', 
                               json={'account': 'fhc', 'password': '114514'},
                               headers=headers)
        
        print(f"跨域请求状态: {response.status_code}")
        print(f"跨域请求响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 跨域请求正常")
            return True
        else:
            print("❌ 跨域请求失败")
            
    except Exception as e:
        print(f"❌ 跨域请求测试失败: {e}")
    
    return False

def main():
    print("🚀 开始测试超级管理员登录修复...")
    print("=" * 50)
    
    # 检查服务器状态
    try:
        backend_health = requests.get(f'{BACKEND_BASE_URL}/health', timeout=5)
        frontend_health = requests.get(f'{FRONTEND_BASE_URL}/', timeout=5)
        
        if backend_health.status_code != 200:
            print("❌ 后端服务器未运行，请先启动app.py")
            return
            
        if frontend_health.status_code != 200:
            print("❌ 前端服务器未运行，请先启动frontend_server.py")
            return
            
        print("✅ 服务器状态正常")
        
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return
    
    # 运行测试
    backend_ok = test_backend_login_api()
    frontend_ok = test_frontend_session_api()
    cors_ok = test_cross_origin()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"后端登录API: {'✅ 正常' if backend_ok else '❌ 异常'}")
    print(f"前端session API: {'✅ 正常' if frontend_ok else '❌ 异常'}")
    print(f"跨域请求: {'✅ 正常' if cors_ok else '❌ 异常'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 登录功能修复成功！")
        print("现在可以正常使用超级管理员登录功能了。")
    else:
        print("\n⚠️ 仍有问题需要解决。")

if __name__ == '__main__':
    main()
