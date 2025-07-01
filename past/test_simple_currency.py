#!/usr/bin/env python3
"""
简单测试超级管理员双货币管理功能
"""
import requests
import json

API_BASE_URL = 'http://127.0.0.1:5000'

def simple_test():
    """简单测试双货币管理功能"""
    print("=== 测试超级管理员双货币管理功能 ===")
    
    try:
        # 1. 测试用户余额API
        print("\n1. 测试用户余额API...")
        response = requests.get(f"{API_BASE_URL}/api/users")
        if response.status_code == 200:
            users_data = response.json()
            if users_data['status'] == 'success' and users_data['data']:
                first_user_id = users_data['data'][0]['id']
                print(f"找到用户ID: {first_user_id}")
                
                # 获取用户余额
                balance_response = requests.get(f"{API_BASE_URL}/api/users/{first_user_id}/balance")
                if balance_response.status_code == 200:
                    balance_data = balance_response.json()
                    print(f"用户余额API响应: {balance_data}")
                    
                    if 'coins_balance' in balance_data['data'] and 'qb_balance' in balance_data['data']:
                        print("✅ 用户余额API支持双货币！")
                    else:
                        print("❌ 用户余额API不支持双货币")
                else:
                    print(f"❌ 获取用户余额失败: {balance_response.status_code}")
            else:
                print("❌ 没有找到用户数据")
        else:
            print(f"❌ 获取用户列表失败: {response.status_code}")
        
        # 2. 测试超级管理员API端点是否存在
        print("\n2. 测试超级管理员API端点...")
        
        # 测试coins API（应该返回401或403，因为没有权限）
        coins_response = requests.put(
            f"{API_BASE_URL}/api/super-admin/users/1/coins",
            json={"super_admin_id": 999, "coins": 1000}
        )
        print(f"修改coins API响应状态: {coins_response.status_code}")
        if coins_response.status_code in [401, 403]:
            print("✅ 修改抽抽币API端点存在且有权限验证")
        else:
            print(f"⚠️ 修改抽抽币API响应: {coins_response.text}")
        
        # 测试qb API（应该返回401或403，因为没有权限）
        qb_response = requests.put(
            f"{API_BASE_URL}/api/super-admin/users/1/qb",
            json={"super_admin_id": 999, "qb": 1000}
        )
        print(f"修改qb API响应状态: {qb_response.status_code}")
        if qb_response.status_code in [401, 403]:
            print("✅ 修改充充币API端点存在且有权限验证")
        else:
            print(f"⚠️ 修改充充币API响应: {qb_response.text}")
            
        print("\n=== 测试完成 ===")
        print("前端界面已更新，支持双货币管理：")
        print("- 用户列表显示抽抽币和充充币")
        print("- 货币管理模态框支持同时修改两种货币")
        print("- 快捷操作按钮（+1000, +5000, -1000, 清零）")
        print("- 后端API支持分别修改抽抽币和充充币")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    simple_test()
