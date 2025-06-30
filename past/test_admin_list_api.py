#!/usr/bin/env python3
"""
测试超级管理员列表API修复
"""

import requests

# 服务器配置
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def test_admin_list_api():
    """测试管理员列表API"""
    print("🧪 测试管理员列表API...")
    
    # 使用超级管理员ID 1
    super_admin_id = 1
    
    try:
        # 测试GET方式获取管理员列表
        response = requests.get(f'{BACKEND_BASE_URL}/api/super-admin/admins', 
                              params={'super_admin_id': super_admin_id})
        
        print(f"管理员列表API状态码: {response.status_code}")
        result = response.json()
        print(f"管理员列表API响应: {result}")
        
        if response.status_code == 200 and result.get('status') == 'success':
            print(f"✅ 管理员列表获取成功，共 {result.get('count', 0)} 个管理员")
            return True
        else:
            print("❌ 管理员列表获取失败")
            return False
            
    except Exception as e:
        print(f"❌ 管理员列表API测试失败: {e}")
        return False

def test_super_admin_list_api():
    """测试超级管理员列表API"""
    print("\n🧪 测试超级管理员列表API...")
    
    # 使用超级管理员ID 1
    super_admin_id = 1
    
    try:
        # 测试GET方式获取超级管理员列表
        response = requests.get(f'{BACKEND_BASE_URL}/api/super-admin/super-admins', 
                              params={'super_admin_id': super_admin_id})
        
        print(f"超级管理员列表API状态码: {response.status_code}")
        result = response.json()
        print(f"超级管理员列表API响应: {result}")
        
        if response.status_code == 200 and result.get('status') == 'success':
            print(f"✅ 超级管理员列表获取成功，共 {result.get('count', 0)} 个超级管理员")
            return True
        else:
            print("❌ 超级管理员列表获取失败")
            return False
            
    except Exception as e:
        print(f"❌ 超级管理员列表API测试失败: {e}")
        return False

def test_users_api():
    """测试用户列表API"""
    print("\n🧪 测试用户列表API...")
    
    try:
        response = requests.get(f'{BACKEND_BASE_URL}/api/users')
        
        print(f"用户列表API状态码: {response.status_code}")
        result = response.json()
        print(f"用户列表API响应: {result}")
        
        if response.status_code == 200 and result.get('status') == 'success':
            print(f"✅ 用户列表获取成功，共 {len(result.get('data', []))} 个用户")
            return True
        else:
            print("❌ 用户列表获取失败")
            return False
            
    except Exception as e:
        print(f"❌ 用户列表API测试失败: {e}")
        return False

def test_items_api():
    """测试物品列表API"""
    print("\n🧪 测试物品列表API...")
    
    try:
        response = requests.get(f'{BACKEND_BASE_URL}/api/items')
        
        print(f"物品列表API状态码: {response.status_code}")
        result = response.json()
        print(f"物品列表API响应前3个: {result.get('data', [])[:3] if result.get('data') else []}")
        
        if response.status_code == 200 and result.get('data'):
            print(f"✅ 物品列表获取成功，共 {len(result.get('data', []))} 个物品")
            return True
        else:
            print("❌ 物品列表获取失败")
            return False
            
    except Exception as e:
        print(f"❌ 物品列表API测试失败: {e}")
        return False

def main():
    print("🚀 测试超级管理员控制台API修复...")
    print("=" * 60)
    
    # 检查后端服务器
    try:
        health_check = requests.get(f'{BACKEND_BASE_URL}/health', timeout=5)
        if health_check.status_code != 200:
            print("❌ 后端服务器未运行")
            return
        print("✅ 后端服务器运行正常")
    except Exception as e:
        print(f"❌ 后端服务器连接失败: {e}")
        return
    
    # 运行API测试
    admin_test = test_admin_list_api()
    super_admin_test = test_super_admin_list_api()
    users_test = test_users_api()
    items_test = test_items_api()
    
    print("\n" + "=" * 60)
    print("📊 API测试结果汇总:")
    print(f"管理员列表API: {'✅ 正常' if admin_test else '❌ 异常'}")
    print(f"超级管理员列表API: {'✅ 正常' if super_admin_test else '❌ 异常'}")
    print(f"用户列表API: {'✅ 正常' if users_test else '❌ 异常'}")
    print(f"物品列表API: {'✅ 正常' if items_test else '❌ 异常'}")
    
    if admin_test and super_admin_test and users_test and items_test:
        print("\n🎉 所有API测试通过！")
        print("超级管理员控制台的列表功能应该能正常工作了。")
    else:
        print("\n⚠️ 部分API测试未通过，请检查相关问题。")

if __name__ == '__main__':
    main()
