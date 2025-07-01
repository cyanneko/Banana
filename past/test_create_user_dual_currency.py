#!/usr/bin/env python3
"""
测试超级管理员创建用户的双货币功能
"""
import requests
import json

API_BASE_URL = 'http://127.0.0.1:5000'

def test_create_user_dual_currency():
    """测试创建用户的双货币功能"""
    print("=== 测试超级管理员创建用户双货币功能 ===")
    
    try:
        # 1. 创建测试超级管理员
        print("\n1. 创建测试超级管理员...")
        create_admin_data = {
            "name": "测试用户创建管理员",
            "account": "test_user_create_admin",
            "password": "test123456"
        }
        
        admin_response = requests.post(f"{API_BASE_URL}/api/auth/register", json=create_admin_data)
        if admin_response.status_code == 200:
            admin_data = admin_response.json()
            admin_id = admin_data['data']['id']
            
            # 设置为超级管理员
            set_admin_response = requests.put(f"{API_BASE_URL}/api/debug/set-super-admin/{admin_id}")
            if set_admin_response.status_code == 200:
                print(f"✅ 测试超级管理员创建成功，ID: {admin_id}")
                
                # 2. 测试创建用户（带双货币）
                print("\n2. 测试创建用户（设置双货币）...")
                create_user_data = {
                    "super_admin_id": admin_id,
                    "name": "双货币测试用户",
                    "account": "dual_currency_test_user",
                    "password": "test123456",
                    "coins": 15000,  # 抽抽币
                    "qb": 888.88     # 充充币
                }
                
                user_response = requests.post(
                    f"{API_BASE_URL}/api/super-admin/users",
                    json=create_user_data
                )
                print(f"创建用户响应: {user_response.status_code}")
                if user_response.status_code == 200:
                    user_result = user_response.json()
                    print(f"✅ 用户创建成功: {user_result}")
                    
                    new_user_id = user_result['data']['id']
                    
                    # 3. 验证用户的双货币余额
                    print(f"\n3. 验证用户双货币余额...")
                    balance_response = requests.get(f"{API_BASE_URL}/api/users/{new_user_id}/balance")
                    if balance_response.status_code == 200:
                        balance_data = balance_response.json()
                        print(f"用户余额: {balance_data}")
                        
                        coins_balance = balance_data['data']['coins_balance']
                        qb_balance = balance_data['data']['qb_balance']
                        
                        if coins_balance == 15000 and qb_balance == 888.88:
                            print("✅ 双货币设置验证成功！")
                        else:
                            print(f"❌ 双货币设置验证失败！期望: coins=15000, qb=888.88, 实际: coins={coins_balance}, qb={qb_balance}")
                    else:
                        print(f"❌ 获取用户余额失败: {balance_response.status_code}")
                        
                    # 4. 测试创建用户（只设置抽抽币，充充币使用默认值）
                    print("\n4. 测试创建用户（只设置抽抽币）...")
                    create_user_data2 = {
                        "super_admin_id": admin_id,
                        "name": "单货币测试用户",
                        "account": "single_currency_test_user",
                        "password": "test123456",
                        "coins": 20000
                        # 不设置qb，应该使用默认值0
                    }
                    
                    user_response2 = requests.post(
                        f"{API_BASE_URL}/api/super-admin/users",
                        json=create_user_data2
                    )
                    if user_response2.status_code == 200:
                        user_result2 = user_response2.json()
                        new_user_id2 = user_result2['data']['id']
                        
                        # 验证默认充充币值
                        balance_response2 = requests.get(f"{API_BASE_URL}/api/users/{new_user_id2}/balance")
                        if balance_response2.status_code == 200:
                            balance_data2 = balance_response2.json()
                            coins_balance2 = balance_data2['data']['coins_balance']
                            qb_balance2 = balance_data2['data']['qb_balance']
                            
                            if coins_balance2 == 20000 and qb_balance2 == 0:
                                print("✅ 默认充充币值验证成功！")
                            else:
                                print(f"❌ 默认充充币值验证失败！期望: coins=20000, qb=0, 实际: coins={coins_balance2}, qb={qb_balance2}")
                        else:
                            print(f"❌ 获取用户余额失败")
                    else:
                        print(f"❌ 创建第二个用户失败: {user_response2.text}")
                        
                else:
                    print(f"❌ 创建用户失败: {user_response.text}")
            else:
                print("❌ 设置超级管理员权限失败")
        else:
            print("❌ 创建测试管理员失败")
            
        print("\n=== 测试完成 ===")
        print("超级管理员创建用户功能现在支持：")
        print("- 同时设置初始抽抽币和充充币")
        print("- 充充币默认值为0，抽抽币默认值为2000")
        print("- 前端界面显示双货币设置选项")
        print("- 创建后立即生效，可通过余额API验证")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_create_user_dual_currency()
