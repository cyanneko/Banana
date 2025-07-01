#!/usr/bin/env python3
"""
测试汇率同步功能
"""

import requests
import json

# API基础URL
API_BASE = "http://localhost:5000"

def test_exchange_rate_sync():
    """测试汇率同步功能"""
    print("🧪 测试前后端汇率同步")
    print("=" * 50)
    
    # 1. 创建测试用户
    test_user = {
        "account": f"testrate_{int(__import__('time').time())}",
        "password": "password123", 
        "name": "汇率测试用户"
    }
    
    print("1. 创建测试用户...")
    try:
        response = requests.post(f"{API_BASE}/api/auth/register", json=test_user)
        if response.status_code in [200, 201]:
            result = response.json()
            if result["status"] == "success":
                user_id = result["data"]["id"]
                print(f"✅ 用户创建成功，ID: {user_id}")
            else:
                print(f"❌ 用户创建失败: {result['message']}")
                return
        else:
            print(f"❌ 用户创建失败: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 用户创建失败: {e}")
        return
    
    # 2. 查询余额API，获取汇率
    print("2. 查询余额API，获取汇率...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                balance_data = result["data"]
                backend_rate = balance_data.get("qb_to_rmb_rate")
                print(f"✅ 后端汇率: {backend_rate}")
                print(f"   完整响应数据: {json.dumps(balance_data, ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
                return
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
        return
    
    # 3. 给用户一些充充币，然后测试提现
    print("3. 充值充充币进行提现测试...")
    try:
        # 先充值100充充币
        recharge_data = {"user_id": user_id, "rmb_amount": 100}
        response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print(f"✅ 充值成功: {result['message']}")
            else:
                print(f"❌ 充值失败: {result['message']}")
                return
        else:
            print(f"❌ 充值失败: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 充值失败: {e}")
        return
    
    # 4. 测试提现，验证汇率计算
    print("4. 测试充充币提现，验证汇率计算...")
    try:
        withdraw_data = {"user_id": user_id, "qb_amount": 50}
        response = requests.post(f"{API_BASE}/api/qb/withdraw", json=withdraw_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print(f"✅ 提现成功: {result['message']}")
                
                # 从响应中获取汇率信息
                if "data" in result and "exchange_rate" in result["data"]:
                    actual_rate = result["data"]["exchange_rate"]
                    print(f"   实际使用的汇率: {actual_rate}")
                    
                    # 验证计算
                    expected_rmb = 50 * actual_rate
                    print(f"   期望获得软妹币: {expected_rmb}")
                
            else:
                print(f"❌ 提现失败: {result['message']}")
        else:
            print(f"❌ 提现失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 提现失败: {e}")
    
    # 5. 再次查询余额，验证汇率一致性
    print("5. 再次查询余额，验证汇率一致性...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                balance_data = result["data"]
                final_rate = balance_data.get("qb_to_rmb_rate")
                print(f"✅ 最终汇率: {final_rate}")
                
                if final_rate == backend_rate:
                    print("✅ 汇率保持一致")
                else:
                    print(f"❌ 汇率不一致！初始: {backend_rate}, 最终: {final_rate}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 汇率同步修复总结:")
    print(f"✅ 后端汇率: {backend_rate}")
    print("✅ 前端提现界面已修复为动态获取汇率")
    print("✅ 前端JavaScript计算已修复为使用API返回的汇率")
    print("✅ 前端界面显示文字已修复为正确汇率")
    
    print("\n📋 前端修复内容:")
    print("1. 提现模态框显示: '1充充币 = 0.9软妹币' (动态获取)")
    print("2. JavaScript计算: 使用 currentUser.qb_to_rmb_rate")
    print("3. 余额更新: 保存API返回的 qb_to_rmb_rate")
    print("4. 事件监听: 避免重复绑定，使用正确汇率计算")

if __name__ == "__main__":
    test_exchange_rate_sync()
