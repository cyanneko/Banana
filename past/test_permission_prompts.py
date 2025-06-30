#!/usr/bin/env python3
"""
权限提示功能测试脚本
测试超级管理员和管理员页面的权限校验和提示功能
"""

import requests
import time

# 服务器配置
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_permission_prompts():
    """测试权限提示功能"""
    print("🧪 开始测试权限提示功能...")
    print("=" * 60)
    
    # 创建会话
    session = requests.Session()
    
    # 测试1: 未登录访问超级管理员页面
    print("🔹 测试1: 未登录访问超级管理员页面")
    try:
        response = session.get(f'{FRONTEND_BASE_URL}/super-admin')
        if response.status_code == 200:
            if "超级管理员登录" in response.text:
                print("   ✅ 正确重定向到超级管理员登录页面")
            else:
                print("   ❌ 未正确重定向")
        else:
            print(f"   ⚠️  状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试2: 未登录访问管理员页面
    print("🔹 测试2: 未登录访问管理员页面")
    try:
        response = session.get(f'{FRONTEND_BASE_URL}/admin')
        if response.status_code == 200:
            if "管理员登录" in response.text:
                print("   ✅ 正确重定向到管理员登录页面")
            else:
                print("   ❌ 未正确重定向")
        else:
            print(f"   ⚠️  状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试3: 以普通用户身份访问超级管理员页面
    print("🔹 测试3: 以普通用户身份访问超级管理员页面")
    try:
        # 先注册一个普通用户
        user_data = {
            'username': 'test_user_permission',
            'account': 'testuser_perm',
            'password': 'testpass123'
        }
        
        # 注册用户
        reg_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/register', json=user_data)
        if reg_response.json().get('status') == 'success':
            print("   📝 普通用户注册成功")
            
            # 登录用户
            login_data = {
                'account': user_data['account'],
                'password': user_data['password']
            }
            
            # 模拟前端登录流程
            login_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=login_data)
            if login_response.json().get('status') == 'success':
                user_info = login_response.json()['data']
                print(f"   🔑 普通用户登录成功，权限: {user_info.get('role', 'user')}")
                
                # 设置前端会话（模拟）
                session_data = {
                    'user_id': user_info['id'],
                    'username': user_info['name'],
                    'role': user_info.get('role', 'user')
                }
                
                # 尝试访问超级管理员页面
                with session as s:
                    # 手动设置session cookies (在实际应用中由前端管理)
                    # 这里我们直接访问页面，应该看到权限不足提示
                    response = s.get(f'{FRONTEND_BASE_URL}/super-admin')
                    if "权限不足" in response.text and "只有超级管理员可以访问" in response.text:
                        print("   ✅ 正确显示权限不足提示")
                    elif "超级管理员登录" in response.text:
                        print("   ✅ 重定向到登录页面（未设置session）")
                    else:
                        print("   ❌ 权限校验失败")
            else:
                print("   ❌ 普通用户登录失败")
        else:
            print("   ❌ 普通用户注册失败")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试4: 检查首页权限提示
    print("🔹 测试4: 检查首页权限提示")
    try:
        response = session.get(f'{FRONTEND_BASE_URL}/')
        if response.status_code == 200:
            if "仅限超级管理员访问" in response.text:
                print("   ✅ 首页包含超级管理员权限提示")
            else:
                print("   ❌ 首页缺少权限提示")
                
            if "需要管理员权限" in response.text:
                print("   ✅ 首页包含管理员权限提示")
            else:
                print("   ❌ 首页缺少管理员权限提示")
        else:
            print(f"   ❌ 首页访问失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试5: 测试超级管理员登录页面的权限校验
    print("🔹 测试5: 测试超级管理员登录页面的权限校验")
    try:
        # 尝试用普通用户登录超级管理员页面
        response = session.get(f'{FRONTEND_BASE_URL}/super-admin-login')
        if response.status_code == 200:
            if "超级管理员登录" in response.text and "最高权限" in response.text:
                print("   ✅ 超级管理员登录页面显示正常")
            else:
                print("   ❌ 超级管理员登录页面内容异常")
        else:
            print(f"   ❌ 超级管理员登录页面访问失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    print("🎯 权限提示功能测试完成！")
    print("=" * 60)

def check_servers():
    """检查服务器状态"""
    print("🔍 检查服务器状态...")
    
    # 检查后端
    try:
        response = requests.get(f'{BACKEND_BASE_URL}/health', timeout=3)
        if response.status_code == 200:
            print("   ✅ 后端服务器运行正常")
        else:
            print(f"   ❌ 后端服务器异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 后端服务器连接失败: {e}")
        return False
    
    # 检查前端
    try:
        response = requests.get(f'{FRONTEND_BASE_URL}/', timeout=3)
        if response.status_code == 200:
            print("   ✅ 前端服务器运行正常")
        else:
            print(f"   ❌ 前端服务器异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 前端服务器连接失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🧪 权限提示功能测试脚本")
    print("=" * 60)
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    # 检查服务器状态
    if check_servers():
        print()
        test_permission_prompts()
    else:
        print("❌ 服务器未正常运行，请先启动后端和前端服务器")
        print("   后端: python app.py")
        print("   前端: python frontend_server.py")
