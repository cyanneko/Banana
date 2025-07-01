#!/usr/bin/env python3
"""
测试超级管理员双货币管理功能
"""
import requests
import json

API_BASE_URL = 'http://127.0.0.1:5000'

def test_super_admin_currency_management():
    """测试超级管理员双货币管理功能"""
    print("=== 测试超级管理员双货币管理功能 ===")
    
    # 1. 创建超级管理员
    print("\n1. 创建超级管理员...")
    create_super_admin_data = {
        "name": "测试超级管理员",
        "account": "test_super_admin",
        "password": "test123456"
    }
    
    response = requests.post(f"{API_BASE_URL}/api/auth/register", json=create_super_admin_data)
    print(f"创建超级管理员响应: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"创建结果: {data}")
        
        # 手动将用户设置为超级管理员
        user_id = data['data']['id']
        modify_response = requests.put(f"{API_BASE_URL}/api/debug/set-super-admin/{user_id}")
        print(f"设置超级管理员权限: {modify_response.status_code}")
    
    # 2. 创建测试普通用户
    print("\n2. 创建测试普通用户...")
    create_user_data = {
        "name": "测试普通用户",
        "account": "test_user_currency",
        "password": "test123456"
    }
    
    response = requests.post(f"{API_BASE_URL}/api/auth/register", json=create_user_data)
    print(f"创建普通用户响应: {response.status_code}")
    
    if response.status_code == 200:
        user_data = response.json()
        test_user_id = user_data['data']['id']
        print(f"创建的用户ID: {test_user_id}")
        
        # 3. 检查用户初始余额
        print(f"\n3. 检查用户初始余额...")
        balance_response = requests.get(f"{API_BASE_URL}/api/users/{test_user_id}/balance")
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            print(f"初始余额: {balance_data}")
            
            initial_coins = balance_data['data']['coins_balance']
            initial_qb = balance_data['data']['qb_balance']
            print(f"初始抽抽币: {initial_coins}, 初始充充币: {initial_qb}")
        
        # 4. 超级管理员修改抽抽币
        print(f"\n4. 超级管理员修改抽抽币...")
        update_coins_data = {
            "super_admin_id": user_id,
            "coins": 50000
        }
        
        coins_response = requests.put(
            f"{API_BASE_URL}/api/super-admin/users/{test_user_id}/coins",
            json=update_coins_data
        )
        print(f"修改抽抽币响应: {coins_response.status_code}")
        if coins_response.status_code == 200:
            coins_result = coins_response.json()
            print(f"修改抽抽币结果: {coins_result}")
        else:
            print(f"修改抽抽币失败: {coins_response.text}")
        
        # 5. 超级管理员修改充充币
        print(f"\n5. 超级管理员修改充充币...")
        update_qb_data = {
            "super_admin_id": user_id,
            "qb": 8888.88
        }
        
        qb_response = requests.put(
            f"{API_BASE_URL}/api/super-admin/users/{test_user_id}/qb",
            json=update_qb_data
        )
        print(f"修改充充币响应: {qb_response.status_code}")
        if qb_response.status_code == 200:
            qb_result = qb_response.json()
            print(f"修改充充币结果: {qb_result}")
        else:
            print(f"修改充充币失败: {qb_response.text}")
        
        # 6. 再次检查用户余额
        print(f"\n6. 再次检查用户余额...")
        balance_response = requests.get(f"{API_BASE_URL}/api/users/{test_user_id}/balance")
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            print(f"修改后余额: {balance_data}")
            
            final_coins = balance_data['data']['coins_balance']
            final_qb = balance_data['data']['qb_balance']
            print(f"最终抽抽币: {final_coins}, 最终充充币: {final_qb}")
            
            # 验证修改是否成功
            if final_coins == 50000 and final_qb == 8888.88:
                print("✅ 双货币管理功能测试成功！")
            else:
                print(f"❌ 双货币管理功能测试失败！期望: coins=50000, qb=8888.88, 实际: coins={final_coins}, qb={final_qb}")
        
        # 7. 测试权限验证（使用普通用户ID尝试修改）
        print(f"\n7. 测试权限验证...")
        unauthorized_data = {
            "super_admin_id": test_user_id,  # 使用普通用户ID
            "coins": 99999
        }
        
        unauthorized_response = requests.put(
            f"{API_BASE_URL}/api/super-admin/users/{test_user_id}/coins",
            json=unauthorized_data
        )
        print(f"无权限修改响应: {unauthorized_response.status_code}")
        if unauthorized_response.status_code == 403:
            print("✅ 权限验证正常！")
        else:
            print(f"❌ 权限验证失败: {unauthorized_response.text}")

if __name__ == "__main__":
    test_super_admin_currency_management()
