#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多货币体系测试脚本
测试充充币(qb)和抽抽币(coins)的相关功能
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api_call(method, endpoint, data=None, description=""):
    """统一的API调用测试函数"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🧪 测试: {description}")
    print(f"📍 {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ 不支持的HTTP方法: {method}")
            return None
            
        print(f"📊 状态码: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"📝 返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        else:
            print(f"📝 返回内容: {response.text}")
            return response.text
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保服务器正在运行")
        return None
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return None

def main():
    print("🚀 多货币体系测试开始")
    print("=" * 60)
    
    # 1. 测试API根端点
    test_api_call("GET", "/", description="获取API信息")
    
    # 2. 注册新用户测试
    test_user_data = {
        "name": "测试用户",
        "account": "test_multi_currency",
        "password": "123456"
    }
    register_result = test_api_call("POST", "/api/auth/register", test_user_data, "注册新用户（检查初始货币）")
    
    if register_result and register_result.get("status") == "success":
        user_id = register_result["data"]["id"]
        print(f"✅ 用户注册成功，ID: {user_id}")
        
        # 3. 测试充充币余额查询
        test_api_call("GET", f"/api/qb/balance/{user_id}", description="查询用户货币余额")
        
        # 4. 测试软妹币充值充充币
        qb_recharge_data = {
            "user_id": user_id,
            "rmb_amount": 100
        }
        test_api_call("POST", "/api/qb/recharge", qb_recharge_data, "使用100软妹币充值充充币")
        
        # 5. 再次查询余额
        test_api_call("GET", f"/api/qb/balance/{user_id}", description="充值后查询余额")
        
        # 6. 测试获取兑换套餐
        test_api_call("GET", "/api/recharge/packages", description="获取充充币兑换抽抽币套餐")
        
        # 7. 测试充充币兑换抽抽币
        exchange_data = {
            "user_id": user_id,
            "package_id": 2  # 小额兑换：500qb -> 550coins
        }
        test_api_call("POST", "/api/recharge", exchange_data, "使用充充币兑换抽抽币")
        
        # 8. 测试余额不足的情况
        insufficient_data = {
            "user_id": user_id,
            "package_id": 6  # 王者兑换：10000qb -> 12500coins
        }
        test_api_call("POST", "/api/recharge", insufficient_data, "测试充充币不足的情况")
        
        # 9. 测试充充币提现
        withdraw_data = {
            "user_id": user_id,
            "qb_amount": 50
        }
        test_api_call("POST", "/api/qb/withdraw", withdraw_data, "提现50充充币为软妹币")
        
        # 10. 最终余额查询
        test_api_call("GET", f"/api/qb/balance/{user_id}", description="最终余额查询")
        
        # 11. 测试单抽（消耗抽抽币）
        single_draw_data = {
            "user_id": user_id,
            "pool_id": 1
        }
        test_api_call("POST", "/api/draw/single", single_draw_data, "使用抽抽币进行单抽")
        
        # 12. 抽卡后余额查询
        test_api_call("GET", f"/api/qb/balance/{user_id}", description="抽卡后余额查询")
        
    else:
        print("❌ 用户注册失败，无法继续测试")
    
    print("\n" + "=" * 60)
    print("🏁 多货币体系测试完成")

if __name__ == "__main__":
    main()
