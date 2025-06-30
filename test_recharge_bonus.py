#!/usr/bin/env python3
"""
测试充值系统API，验证赠送金额功能
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

def test_recharge_bonus():
    """测试充值赠送功能"""
    print("🧪 开始测试充值赠送功能...")
    
    # 1. 注册测试用户
    print("\n📝 注册测试用户...")
    test_username = f"recharge_test_{int(time.time())}"
    register_data = {
        "name": test_username,
        "account": test_username,
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        result = response.json()
        
        if response.status_code in [200, 201] and result.get("status") == "success":
            user_data = result["data"]
            print(f"✅ 用户注册成功: {user_data['name']} (ID: {user_data['id']})")
            print(f"💰 初始货币: {user_data['coins']}")
        else:
            print(f"❌ 注册失败: {result.get('message', 'Unknown error')}")
            return
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return
    
    user_id = user_data["id"]
    initial_coins = user_data["coins"]
    
    # 2. 获取充值套餐
    print("\n📦 获取充值套餐...")
    try:
        response = requests.get(f"{BASE_URL}/api/recharge/packages")
        if response.status_code == 200:
            packages = response.json()["data"]
            print("✅ 充值套餐获取成功:")
            for pkg in packages:
                bonus_text = f"+{pkg['bonus']}赠送" if pkg['bonus'] > 0 else ""
                print(f"   {pkg['name']}: {pkg['coins']}货币{bonus_text} ({pkg['price']})")
        else:
            print(f"❌ 获取套餐失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 获取套餐失败: {e}")
        return
    
    # 3. 测试不同套餐的充值和赠送
    test_packages = [
        {"coins": 500, "expected_bonus": 50, "name": "小额充值"},
        {"coins": 1000, "expected_bonus": 100, "name": "标准充值"},
        {"coins": 2000, "expected_bonus": 300, "name": "豪华充值"}
    ]
    
    current_coins = initial_coins
    
    for test_pkg in test_packages:
        print(f"\n💳 测试{test_pkg['name']}充值...")
        print(f"   充值金额: {test_pkg['coins']}")
        print(f"   预期赠送: {test_pkg['expected_bonus']}")
        print(f"   预期总额: {test_pkg['coins'] + test_pkg['expected_bonus']}")
        print(f"   充值前余额: {current_coins}")
        
        recharge_data = {
            "user_id": user_id,
            "amount": test_pkg["coins"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/recharge", json=recharge_data)
            if response.status_code == 200:
                result = response.json()["data"]
                old_coins = result["old_coins"]
                new_coins = result["new_coins"]
                actual_added = new_coins - old_coins
                
                print(f"   ✅ 充值成功!")
                print(f"   充值前: {old_coins}")
                print(f"   充值后: {new_coins}")
                print(f"   实际增加: {actual_added}")
                print(f"   基础金额: {result.get('base_amount', 'N/A')}")
                print(f"   赠送金额: {result.get('bonus_amount', 'N/A')}")
                print(f"   总金额: {result.get('total_amount', 'N/A')}")
                
                # 验证充值是否正确
                expected_total = test_pkg["coins"] + test_pkg["expected_bonus"]
                if actual_added == expected_total:
                    print(f"   ✅ 赠送金额正确！实际增加{actual_added} = 基础{test_pkg['coins']} + 赠送{test_pkg['expected_bonus']}")
                else:
                    print(f"   ❌ 赠送金额错误！实际增加{actual_added}，预期{expected_total}")
                
                current_coins = new_coins
                
            else:
                print(f"   ❌ 充值失败: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 充值失败: {e}")
    
    # 4. 测试总余额
    print(f"\n📊 最终余额统计:")
    print(f"   初始余额: {initial_coins}")
    print(f"   最终余额: {current_coins}")
    print(f"   总增加: {current_coins - initial_coins}")
    
    expected_total_increase = sum(pkg["coins"] + pkg["expected_bonus"] for pkg in test_packages)
    actual_total_increase = current_coins - initial_coins
    
    if actual_total_increase == expected_total_increase:
        print(f"   ✅ 总充值金额正确！增加{actual_total_increase}，预期{expected_total_increase}")
    else:
        print(f"   ❌ 总充值金额错误！增加{actual_total_increase}，预期{expected_total_increase}")
    
    print("\n🎉 充值系统测试完成！")

def test_invalid_recharge():
    """测试无效充值请求"""
    print("\n🧪 测试无效充值请求...")
    
    # 测试无效金额
    invalid_data = {
        "user_id": 1,
        "amount": 999  # 不存在的套餐金额
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/recharge", json=invalid_data)
        if response.status_code == 400:
            print("✅ 无效金额正确被拒绝")
        else:
            print(f"❌ 无效金额处理异常: {response.text}")
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
            
            # 运行测试
            test_recharge_bonus()
            test_invalid_recharge()
            
        else:
            print("❌ 后端服务器无响应，请先启动服务器")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://127.0.0.1:5000 运行")
    except Exception as e:
        print(f"❌ 测试异常: {e}")
