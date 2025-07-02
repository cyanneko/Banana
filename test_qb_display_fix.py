#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试充充币显示小数点位数和自定义充值功能
"""

import requests
import json
import time

# API基础URL
API_BASE = 'http://127.0.0.1:5000'

def test_qb_display_and_custom_recharge():
    """测试充充币显示格式和自定义充值"""
    print("=== 测试充充币显示格式和自定义充值功能 ===")
    
    # 1. 登录测试用户
    print("\n1. 登录测试用户...")
    login_data = {
        "account": "test1",
        "password": "123456"
    }
    
    response = requests.post(f"{API_BASE}/api/auth/login", json=login_data)
    print(f"登录响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        login_result = response.json()
        print(f"登录结果: {login_result}")
        
        if login_result['status'] == 'success':
            user_data = login_result['data']
            user_id = user_data['id']
            print(f"登录成功，用户ID: {user_id}")
            
            # 2. 获取用户余额
            print(f"\n2. 获取用户当前余额...")
            balance_response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
            print(f"余额查询状态码: {balance_response.status_code}")
            
            if balance_response.status_code == 200:
                balance_data = balance_response.json()
                print(f"余额数据: {balance_data}")
                
                if balance_data['status'] == 'success':
                    initial_qb = balance_data['data']['qb_balance']
                    print(f"初始充充币余额: {initial_qb}")
                    
                    # 3. 测试自定义充值 - 小数金额
                    print(f"\n3. 测试自定义充值小数金额...")
                    recharge_amounts = [10.5, 25.75, 100.25, 999.99]
                    
                    for amount in recharge_amounts:
                        print(f"\n充值 {amount} 软妹币...")
                        recharge_data = {
                            "user_id": user_id,
                            "rmb_amount": amount
                        }
                        
                        recharge_response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
                        print(f"充值响应状态码: {recharge_response.status_code}")
                        
                        if recharge_response.status_code == 200:
                            recharge_result = response.json()
                            print(f"充值结果: {recharge_result}")
                            
                            # 验证余额更新
                            balance_response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
                            if balance_response.status_code == 200:
                                balance_data = balance_response.json()
                                if balance_data['status'] == 'success':
                                    current_qb = balance_data['data']['qb_balance']
                                    print(f"充值后充充币余额: {current_qb}")
                                    
                                    # 验证充充币金额精度（应该保持小数位）
                                    if isinstance(current_qb, float):
                                        print(f"✓ 充充币余额保持小数精度: {current_qb:.2f}")
                                    else:
                                        print(f"✗ 充充币余额类型异常: {type(current_qb)} - {current_qb}")
                        else:
                            print(f"✗ 充值失败: {recharge_response.text}")
                        
                        time.sleep(0.5)  # 短暂暂停避免频繁请求
                    
                    # 4. 测试边界值充值
                    print(f"\n4. 测试边界值充值...")
                    boundary_amounts = [0.01, 1, 1000000]
                    
                    for amount in boundary_amounts:
                        print(f"\n充值边界值 {amount} 软妹币...")
                        recharge_data = {
                            "user_id": user_id,
                            "rmb_amount": amount
                        }
                        
                        recharge_response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
                        print(f"充值响应状态码: {recharge_response.status_code}")
                        
                        if recharge_response.status_code == 200:
                            recharge_result = recharge_response.json()
                            print(f"边界值充值结果: {recharge_result}")
                        else:
                            print(f"边界值充值失败: {recharge_response.text}")
                    
                    # 5. 最终余额查询
                    print(f"\n5. 最终余额查询...")
                    final_balance_response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
                    if final_balance_response.status_code == 200:
                        final_balance_data = final_balance_response.json()
                        if final_balance_data['status'] == 'success':
                            final_qb = final_balance_data['data']['qb_balance']
                            qb_rate = final_balance_data['data']['qb_to_rmb_rate']
                            print(f"最终充充币余额: {final_qb}")
                            print(f"充充币兑软妹币汇率: {qb_rate}")
                            
                            # 验证前端显示格式
                            if isinstance(final_qb, float):
                                formatted_qb = f"{final_qb:.2f}"
                                print(f"✓ 前端应显示格式: {formatted_qb}")
                            
                else:
                    print(f"✗ 获取余额失败: {balance_data}")
            else:
                print(f"✗ 余额查询请求失败: {balance_response.text}")
        else:
            print(f"✗ 登录失败: {login_result}")
    else:
        print(f"✗ 登录请求失败: {response.text}")

def test_invalid_recharge():
    """测试无效充值输入"""
    print("\n=== 测试无效充值输入 ===")
    
    # 使用test1用户
    user_id = 1
    
    invalid_amounts = [
        -1,        # 负数
        0,         # 零
        "abc",     # 非数字字符串
        None,      # 空值
        10000001,  # 超大金额
    ]
    
    for amount in invalid_amounts:
        print(f"\n测试无效充值金额: {amount}")
        recharge_data = {
            "user_id": user_id,
            "rmb_amount": amount
        }
        
        try:
            recharge_response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
            print(f"响应状态码: {recharge_response.status_code}")
            
            if recharge_response.status_code != 200:
                print(f"✓ 正确拒绝无效充值: {recharge_response.text}")
            else:
                result = recharge_response.json()
                if result['status'] == 'error':
                    print(f"✓ 后端正确验证: {result['message']}")
                else:
                    print(f"✗ 应该拒绝的充值被接受: {result}")
        except Exception as e:
            print(f"请求异常: {e}")

if __name__ == "__main__":
    test_qb_display_and_custom_recharge()
    test_invalid_recharge()
    print("\n=== 测试完成 ===")
