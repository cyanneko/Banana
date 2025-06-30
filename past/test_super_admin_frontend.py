#!/usr/bin/env python3
"""
超级管理员前端界面测试脚本
测试前端界面与后端API的集成
"""

import requests
import time
import json
import sys

# API基础URL
API_BASE_URL = 'http://127.0.0.1:5000'
FRONTEND_BASE_URL = 'http://127.0.0.1:3000'

def test_backend_connection():
    """测试后端API连接"""
    print("🔍 测试后端API连接...")
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            print("✅ 后端API连接正常")
            return True
        else:
            print(f"❌ 后端API响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 后端API连接失败: {e}")
        return False

def test_frontend_connection():
    """测试前端服务器连接"""
    print("🔍 测试前端服务器连接...")
    try:
        response = requests.get(FRONTEND_BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务器连接正常")
            return True
        else:
            print(f"❌ 前端服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 前端服务器连接失败: {e}")
        return False

def test_super_admin_page():
    """测试超级管理员页面"""
    print("🔍 测试超级管理员页面...")
    try:
        response = requests.get(f'{FRONTEND_BASE_URL}/super-admin', timeout=5)
        if response.status_code == 200:
            html_content = response.text
            # 检查关键元素是否存在
            if '超级管理员控制台' in html_content and 'API_BASE_URL' in html_content:
                print("✅ 超级管理员页面加载正常")
                return True
            else:
                print("❌ 超级管理员页面内容不完整")
                return False
        else:
            print(f"❌ 超级管理员页面响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 超级管理员页面加载失败: {e}")
        return False

def test_super_admin_login():
    """测试超级管理员登录API"""
    print("🔍 测试超级管理员登录...")
    
    # 使用默认的超级管理员账号
    login_data = {
        'account': 'fhc',
        'password': '114514'
    }
    
    try:
        response = requests.post(f'{API_BASE_URL}/api/auth/login', 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and data.get('role') == 'super_admin':
                print("✅ 超级管理员登录测试成功")
                print(f"   用户信息: {data.get('data', {}).get('name', 'N/A')}")
                return data.get('data', {}).get('id')
            else:
                print(f"❌ 登录失败: {data.get('message', '未知错误')}")
                return None
        else:
            print(f"❌ 登录请求失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 登录请求异常: {e}")
        return None

def test_super_admin_apis(super_admin_id):
    """测试超级管理员相关API"""
    print("🔍 测试超级管理员API...")
    
    test_results = []
    
    # 测试管理员列表
    try:
        response = requests.post(f'{API_BASE_URL}/api/super-admin/admins',
                               json={'super_admin_id': super_admin_id}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✅ 管理员列表API正常 (找到 {len(data.get('data', []))} 个管理员)")
                test_results.append(True)
            else:
                print(f"❌ 管理员列表API失败: {data.get('message')}")
                test_results.append(False)
        else:
            print(f"❌ 管理员列表API响应异常: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ 管理员列表API异常: {e}")
        test_results.append(False)
    
    # 测试超级管理员列表
    try:
        response = requests.post(f'{API_BASE_URL}/api/super-admin/super-admins',
                               json={'super_admin_id': super_admin_id}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✅ 超级管理员列表API正常 (找到 {len(data.get('data', []))} 个超级管理员)")
                test_results.append(True)
            else:
                print(f"❌ 超级管理员列表API失败: {data.get('message')}")
                test_results.append(False)
        else:
            print(f"❌ 超级管理员列表API响应异常: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ 超级管理员列表API异常: {e}")
        test_results.append(False)
    
    # 测试用户列表API
    try:
        response = requests.get(f'{API_BASE_URL}/api/users', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✅ 用户列表API正常 (找到 {len(data.get('data', []))} 个用户)")
                test_results.append(True)
            else:
                print(f"❌ 用户列表API失败: {data.get('message')}")
                test_results.append(False)
        else:
            print(f"❌ 用户列表API响应异常: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ 用户列表API异常: {e}")
        test_results.append(False)
    
    # 测试物品列表API
    try:
        response = requests.get(f'{API_BASE_URL}/api/items', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✅ 物品列表API正常 (找到 {len(data.get('data', []))} 个物品)")
                test_results.append(True)
            else:
                print(f"❌ 物品列表API失败: {data.get('message')}")
                test_results.append(False)
        else:
            print(f"❌ 物品列表API响应异常: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ 物品列表API异常: {e}")
        test_results.append(False)
    
    return all(test_results)

def main():
    """主测试函数"""
    print("🚀 开始超级管理员前端界面测试")
    print("=" * 50)
    
    # 测试结果
    all_tests_passed = True
    
    # 1. 测试后端连接
    if not test_backend_connection():
        print("❌ 请先启动后端服务器 (python app.py)")
        all_tests_passed = False
    
    # 2. 测试前端连接
    if not test_frontend_connection():
        print("❌ 请先启动前端服务器 (python frontend_server.py)")
        all_tests_passed = False
    
    # 3. 测试超级管理员页面
    if not test_super_admin_page():
        print("❌ 超级管理员页面有问题")
        all_tests_passed = False
    
    # 4. 测试超级管理员登录
    super_admin_id = test_super_admin_login()
    if not super_admin_id:
        print("❌ 超级管理员登录失败")
        all_tests_passed = False
    
    # 5. 测试超级管理员API
    if super_admin_id:
        if not test_super_admin_apis(super_admin_id):
            print("❌ 部分超级管理员API测试失败")
            all_tests_passed = False
    
    print("=" * 50)
    
    if all_tests_passed:
        print("🎉 所有测试通过！超级管理员前端界面可以正常使用")
        print("\n📖 使用指南:")
        print("1. 访问 http://127.0.0.1:3000/super-admin")
        print("2. 使用账号 'fhc' 密码 '114514' 登录")
        print("3. 在控制台中管理系统数据")
        print("\n🌟 可用功能:")
        print("- 查看系统统计")
        print("- 管理普通管理员")
        print("- 管理超级管理员")
        print("- 管理用户账户")
        print("- 修改用户金币")
        print("- 管理物品数据")
        return True
    else:
        print("❌ 部分测试失败，请检查服务器状态和配置")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
