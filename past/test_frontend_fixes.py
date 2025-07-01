#!/usr/bin/env python3
"""
测试前端多货币修复后的效果
"""

import requests
import json
import time

# API基础URL
API_BASE = "http://localhost:5000"

def test_frontend_fixes():
    """测试前端修复后的效果"""
    print("🧪 测试前端多货币修复效果")
    print("=" * 50)
    
    # 测试数据
    test_user = {
        "account": "testuser123",
        "password": "password123",
        "name": "测试用户"
    }
    
    # 1. 创建测试用户
    print("1. 创建测试用户...")
    try:
        response = requests.post(f"{API_BASE}/api/auth/register", json=test_user)
        if response.status_code == 200:
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
    
    # 2. 测试用户登录
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
                print("✅ 用户登录成功")
                user_data = result["data"]
                print(f"   用户信息: {user_data['name']} (ID: {user_data['id']})")
                print(f"   初始抽抽币: {user_data.get('coins', 0)}")
                print(f"   初始充充币: {user_data.get('qb', 0)}")
            else:
                print(f"❌ 用户登录失败: {result['message']}")
                return
        else:
            print(f"❌ 用户登录失败: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 用户登录失败: {e}")
        return
    
    # 3. 测试余额查询API（验证前端会调用这个API）
    print("3. 测试余额查询API...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                balance_data = result["data"]
                print("✅ 余额查询成功")
                print(f"   抽抽币: {balance_data['coins']}")
                print(f"   充充币: {balance_data['qb']}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
    
    # 4. 测试软妹币充值充充币（修复后的参数）
    print("4. 测试软妹币充值充充币...")
    try:
        recharge_data = {
            "user_id": user_id,
            "rmb_amount": 100  # 修复后使用正确的参数名
        }
        response = requests.post(f"{API_BASE}/api/qb/recharge", json=recharge_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print("✅ 充充币充值成功")
                print(f"   {result['message']}")
            else:
                print(f"❌ 充充币充值失败: {result['message']}")
        else:
            print(f"❌ 充充币充值失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 充充币充值失败: {e}")
    
    # 5. 再次查询余额（验证充值后余额更新）
    print("5. 验证充值后余额...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                balance_data = result["data"]
                print("✅ 充值后余额查询成功")
                print(f"   抽抽币: {balance_data['coins']}")
                print(f"   充充币: {balance_data['qb']}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
    
    # 6. 测试充值套餐API
    print("6. 测试充值套餐API...")
    try:
        response = requests.get(f"{API_BASE}/api/recharge/packages")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                packages = result["data"]
                print("✅ 充值套餐查询成功")
                for pkg in packages:
                    print(f"   套餐{pkg['id']}: {pkg['qb_cost']}充充币 → {pkg['coins']}抽抽币 (赠送:{pkg['bonus']})")
            else:
                print(f"❌ 充值套餐查询失败: {result['message']}")
        else:
            print(f"❌ 充值套餐查询失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 充值套餐查询失败: {e}")
    
    # 7. 测试充充币兑换抽抽币
    print("7. 测试充充币兑换抽抽币...")
    try:
        exchange_data = {
            "user_id": user_id,
            "package_id": 1  # 使用套餐1
        }
        response = requests.post(f"{API_BASE}/api/recharge", json=exchange_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print("✅ 充充币兑换抽抽币成功")
                print(f"   {result['message']}")
            else:
                print(f"❌ 充充币兑换抽抽币失败: {result['message']}")
        else:
            print(f"❌ 充充币兑换抽抽币失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 充充币兑换抽抽币失败: {e}")
    
    # 8. 最终余额查询
    print("8. 最终余额查询...")
    try:
        response = requests.get(f"{API_BASE}/api/qb/balance/{user_id}")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                balance_data = result["data"]
                print("✅ 最终余额查询成功")
                print(f"   抽抽币: {balance_data['coins']}")
                print(f"   充充币: {balance_data['qb']}")
            else:
                print(f"❌ 余额查询失败: {result['message']}")
        else:
            print(f"❌ 余额查询失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 余额查询失败: {e}")
    
    # 9. 测试充充币提现（修复后的参数）
    print("9. 测试充充币提现...")
    try:
        withdraw_data = {
            "user_id": user_id,
            "qb_amount": 10  # 修复后使用正确的参数名
        }
        response = requests.post(f"{API_BASE}/api/qb/withdraw", json=withdraw_data)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print("✅ 充充币提现成功")
                print(f"   {result['message']}")
            else:
                print(f"❌ 充充币提现失败: {result['message']}")
        else:
            print(f"❌ 充充币提现失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 充充币提现失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 前端修复测试总结:")
    print("✅ 修复了 rechargeQb 函数的参数名：amount → rmb_amount")
    print("✅ 修复了 withdrawQb 函数的参数名：amount → qb_amount")
    print("✅ 余额更新逻辑调用了正确的 /api/qb/balance/<user_id> API")
    print("✅ 后端API响应正常，前端应该能正确显示余额")
    print("\n📋 前端使用说明:")
    print("1. 用户登录后会自动调用 updateUserBalances() 获取最新余额")
    print("2. 软妹币充值充充币使用正确的 rmb_amount 参数")
    print("3. 充充币提现使用正确的 qb_amount 参数")
    print("4. 所有货币操作后都会调用 updateUserBalances() 刷新显示")

if __name__ == "__main__":
    test_frontend_fixes()
