#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级管理员功能测试脚本
测试超级管理员的各种权限和功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://127.0.0.1:5000"
SUPER_ADMIN_ID = 1  # 默认超级管理员ID

def print_section(title):
    """打印测试段落标题"""
    print(f"\n{'='*50}")
    print(f"🔧 {title}")
    print('='*50)

def test_request(method, endpoint, data=None, params=None, description=""):
    """执行测试请求"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n🔍 测试: {description}")
    print(f"📡 {method.upper()} {endpoint}")
    if data:
        print(f"📦 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        if method.lower() == 'get':
            response = requests.get(url, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, json=data)
        elif method.lower() == 'put':
            response = requests.put(url, json=data)
        elif method.lower() == 'delete':
            response = requests.delete(url, json=data)
        
        print(f"📊 状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"📋 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        except:
            print(f"📋 响应: {response.text}")
            return {"status": "error", "message": "Invalid JSON response"}
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请确保后端服务器正在运行 (python app.py)")
        return {"status": "error", "message": "Connection failed"}
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return {"status": "error", "message": str(e)}

def main():
    print("🎯 超级管理员功能测试")
    print("="*60)
    
    # 测试1: 管理员管理
    print_section("管理员管理测试")
    
    # 查看现有管理员
    test_request('get', '/api/super-admin/admins', 
                params={'super_admin_id': SUPER_ADMIN_ID},
                description="查看所有管理员")
    
    # 创建新管理员
    new_admin_data = {
        "super_admin_id": SUPER_ADMIN_ID,
        "name": "测试管理员",
        "account": "test_admin",
        "password": "password123"
    }
    create_result = test_request('post', '/api/super-admin/admins', 
                               data=new_admin_data,
                               description="创建新管理员")
    
    # 删除管理员（如果创建成功）
    if create_result.get("status") == "success":
        admin_id = create_result.get("data", {}).get("id")
        if admin_id:
            delete_admin_data = {"super_admin_id": SUPER_ADMIN_ID}
            test_request('delete', f'/api/super-admin/admins/{admin_id}', 
                        data=delete_admin_data,
                        description=f"删除管理员 ID:{admin_id}")
    
    # 测试2: 超级管理员管理
    print_section("超级管理员管理测试")
    
    # 查看现有超级管理员
    test_request('get', '/api/super-admin/super-admins', 
                params={'super_admin_id': SUPER_ADMIN_ID},
                description="查看所有超级管理员")
    
    # 创建新超级管理员
    new_super_admin_data = {
        "super_admin_id": SUPER_ADMIN_ID,
        "name": "测试超级管理员",
        "account": "test_super_admin",
        "password": "password123"
    }
    create_super_result = test_request('post', '/api/super-admin/super-admins', 
                                     data=new_super_admin_data,
                                     description="创建新超级管理员")
    
    # 删除超级管理员（如果创建成功）
    if create_super_result.get("status") == "success":
        super_admin_id = create_super_result.get("data", {}).get("id")
        if super_admin_id:
            delete_super_admin_data = {"super_admin_id": SUPER_ADMIN_ID}
            test_request('delete', f'/api/super-admin/super-admins/{super_admin_id}', 
                        data=delete_super_admin_data,
                        description=f"删除超级管理员 ID:{super_admin_id}")
    
    # 测试3: 用户管理
    print_section("用户管理测试")
    
    # 创建新用户
    new_user_data = {
        "super_admin_id": SUPER_ADMIN_ID,
        "name": "测试用户",
        "account": "test_user",
        "password": "password123",
        "coins": 5000
    }
    create_user_result = test_request('post', '/api/super-admin/users', 
                                    data=new_user_data,
                                    description="创建新用户")
    
    test_user_id = None
    if create_user_result.get("status") == "success":
        test_user_id = create_user_result.get("data", {}).get("id")
        
        # 修改用户货币
        if test_user_id:
            coins_data = {
                "super_admin_id": SUPER_ADMIN_ID,
                "coins": 10000
            }
            test_request('put', f'/api/super-admin/users/{test_user_id}/coins', 
                        data=coins_data,
                        description=f"修改用户 ID:{test_user_id} 的货币")
            
            # 修改用户库存
            inventory_data = {
                "super_admin_id": SUPER_ADMIN_ID,
                "item_id": 1,
                "quantity": 5
            }
            test_request('put', f'/api/super-admin/users/{test_user_id}/inventory', 
                        data=inventory_data,
                        description=f"修改用户 ID:{test_user_id} 的库存")
    
    # 测试4: 物品管理
    print_section("物品管理测试")
    
    # 创建新物品
    new_item_data = {
        "super_admin_id": SUPER_ADMIN_ID,
        "name": "测试物品",
        "description": "这是一个测试物品",
        "weight": 15,
        "rarity": "稀有",
        "type": "测试"
    }
    create_item_result = test_request('post', '/api/super-admin/items', 
                                    data=new_item_data,
                                    description="创建新物品")
    
    test_item_id = None
    if create_item_result.get("status") == "success":
        test_item_id = create_item_result.get("data", {}).get("id")
        
        # 修改物品
        if test_item_id:
            update_item_data = {
                "super_admin_id": SUPER_ADMIN_ID,
                "name": "测试物品_已修改",
                "description": "这是一个修改后的测试物品",
                "weight": 25,
                "rarity": "史诗"
            }
            test_request('put', f'/api/super-admin/items/{test_item_id}', 
                        data=update_item_data,
                        description=f"修改物品 ID:{test_item_id}")
    
    # 测试5: 权限验证
    print_section("权限验证测试")
    
    # 使用非超级管理员ID测试权限
    unauthorized_data = {
        "super_admin_id": 999,  # 不存在的超级管理员ID
        "name": "未授权测试",
        "account": "unauthorized",
        "password": "test"
    }
    test_request('post', '/api/super-admin/admins', 
                data=unauthorized_data,
                description="未授权创建管理员（应该失败）")
    
    # 测试6: 清理测试数据
    print_section("清理测试数据")
    
    # 删除测试用户
    if test_user_id:
        delete_user_data = {"super_admin_id": SUPER_ADMIN_ID}
        test_request('delete', f'/api/super-admin/users/{test_user_id}', 
                    data=delete_user_data,
                    description=f"删除测试用户 ID:{test_user_id}")
    
    # 删除测试物品
    if test_item_id:
        delete_item_data = {"super_admin_id": SUPER_ADMIN_ID}
        test_request('delete', f'/api/super-admin/items/{test_item_id}', 
                    data=delete_item_data,
                    description=f"删除测试物品 ID:{test_item_id}")
    
    print_section("测试完成")
    print("✅ 超级管理员功能测试完成！")
    print("🔍 请检查以上输出，确保所有功能正常工作")
    print("\n📋 测试功能清单:")
    print("   ✅ 管理员管理 (查看/创建/删除)")
    print("   ✅ 超级管理员管理 (查看/创建/删除)")
    print("   ✅ 用户管理 (创建/删除/修改货币/修改库存)")
    print("   ✅ 物品管理 (创建/修改/删除)")
    print("   ✅ 权限验证 (未授权访问控制)")

if __name__ == "__main__":
    main()
