#!/usr/bin/env python3
"""
测试前端余额显示修复
"""

import requests
import json

# API基础URL
API_BASE = "http://localhost:5000"

def test_balance_display():
    """测试余额显示相关功能"""
    print("🧪 测试前端余额显示修复")
    print("=" * 50)
    
    # 1. 创建一个新用户来测试
    test_user = {
        "account": f"testbalance_{int(__import__('time').time())}",
        "password": "password123",
        "name": "余额测试用户"
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
                return None
        else:
            print(f"❌ 用户创建失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 用户创建失败: {e}")
        return None
    
    # 2. 测试登录API
    print("2. 测试用户登录...")
    try:
        login_data = {
            "account": test_user["account"],
            "password": test_user["password"]
        }
        response = requests.post(f"{API_BASE}/api/auth/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                user_data = result["data"]
                print("✅ 用户登录成功")
                print(f"   登录返回的用户数据: {json.dumps(user_data, ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ 用户登录失败: {result['message']}")
                return None
        else:
            print(f"❌ 用户登录失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 用户登录失败: {e}")
        return None
    
    # 3. 测试余额查询API（这是前端会调用的关键API）
    print("3. 测试余额查询API（前端调用的关键API）...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        print(f"   请求URL: {API_BASE}/api/qb/balance/{user_id}")
        print(f"   响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result["status"] == "success":
                balance_data = result["data"]
                print("✅ 余额查询成功")
                print(f"   🪙 抽抽币 (coins_balance): {balance_data['coins_balance']}")
                print(f"   💎 充充币 (qb_balance): {balance_data['qb_balance']}")
                print(f"   前端应该显示: userCoins={balance_data['coins_balance']}, userQb={balance_data['qb_balance']}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
    
    # 4. 给用户充值一些充充币，然后再次测试余额显示
    print("4. 充值100充充币后测试余额显示...")
    try:
        recharge_data = {
            "user_id": user_id,
            "rmb_amount": 100
        }
        response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print("✅ 充充币充值成功")
                print(f"   {result['message']}")
                
                # 再次查询余额
                balance_response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
                if balance_response.status_code == 200:
                    balance_result = balance_response.json()
                    if balance_result["status"] == "success":
                        new_balance = balance_result["data"]
                        print("✅ 充值后余额查询成功")
                        print(f"   🪙 抽抽币 (coins_balance): {new_balance['coins_balance']}")
                        print(f"   💎 充充币 (qb_balance): {new_balance['qb_balance']}")
                        print(f"   前端应该显示更新后的余额: userCoins={new_balance['coins_balance']}, userQb={new_balance['qb_balance']}")
                    else:
                        print(f"❌ 充值后余额查询失败: {balance_result['message']}")
            else:
                print(f"❌ 充充币充值失败: {result['message']}")
        else:
            print(f"❌ 充充币充值失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 充充币充值失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 前端余额显示问题分析:")
    print("1. 检查浏览器控制台是否有JavaScript错误")
    print("2. 检查网络请求是否成功（F12 → Network选项卡）")
    print("3. 检查 updateUserBalances() 函数是否被正确调用")
    print("4. 检查 API_BASE 变量是否正确设置为 'http://localhost:5000'")
    print("5. 确认用户登录后 currentUser.id 是否正确设置")
    
    print("\n🛠️  前端调试建议:")
    print("1. 在浏览器中打开 gacha.html")
    print("2. 打开开发者工具（F12）")
    print("3. 在Console中输入: console.log('currentUser:', currentUser)")
    print("4. 在Console中输入: updateUserBalances().then(() => console.log('余额更新完成'))")
    print("5. 检查是否有网络请求失败或CORS错误")
    
    return user_id

if __name__ == "__main__":
    test_balance_display()
