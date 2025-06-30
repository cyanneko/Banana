"""
货币系统测试脚本
测试充值和抽卡扣费功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_login():
    """测试登录并获取用户初始货币"""
    print("🔐 测试用户登录...")
    login_data = {
        "account": "fhc",
        "password": "114514"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    data = response.json()
    print(f"用户信息: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return data['data'] if data['status'] == 'success' else None

def test_recharge_packages():
    """测试获取充值套餐"""
    print("\n💰 测试获取充值套餐...")
    response = requests.get(f"{BASE_URL}/api/recharge/packages")
    data = response.json()
    print(f"充值套餐: {json.dumps(data, ensure_ascii=False, indent=2)}")

def test_recharge(user_id, amount):
    """测试充值"""
    print(f"\n💳 测试充值 {amount} 货币...")
    recharge_data = {
        "user_id": user_id,
        "amount": amount
    }
    
    response = requests.post(f"{BASE_URL}/api/recharge", json=recharge_data)
    data = response.json()
    print(f"充值结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return data['data'] if data['status'] == 'success' else None

def test_single_draw_with_cost(user_id):
    """测试单次抽卡（含扣费）"""
    print(f"\n🎯 测试单次抽卡（扣费160货币）...")
    draw_data = {
        "user_id": user_id
    }
    
    response = requests.post(f"{BASE_URL}/api/draw/single", json=draw_data)
    data = response.json()
    print(f"抽卡结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return data

def test_ten_draw_with_cost(user_id):
    """测试十连抽（含扣费）"""
    print(f"\n🎰 测试十连抽（扣费1600货币）...")
    draw_data = {
        "user_id": user_id
    }
    
    response = requests.post(f"{BASE_URL}/api/draw/ten", json=draw_data)
    data = response.json()
    print(f"十连抽结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return data

def main():
    print("=" * 50)
    print("🎲 货币系统功能测试")
    print("=" * 50)
    
    # 1. 测试登录
    user = test_login()
    if not user:
        print("❌ 登录失败，终止测试")
        return
    
    user_id = user['id']
    print(f"✅ 登录成功，用户ID: {user_id}，初始货币: {user.get('coins', 0)}")
    
    # 2. 测试获取充值套餐
    test_recharge_packages()
    
    # 3. 测试充值
    recharge_result = test_recharge(user_id, 1000)
    if recharge_result:
        print(f"✅ 充值成功，新余额: {recharge_result['new_coins']}")
    
    # 4. 测试单次抽卡扣费
    single_result = test_single_draw_with_cost(user_id)
    if single_result.get('status') == 'success':
        print(f"✅ 单次抽卡成功，剩余货币: {single_result['data']['remaining_coins']}")
        print(f"   获得物品: {single_result['data']['item']['name']} ({single_result['data']['item']['rarity']})")
    else:
        print(f"❌ 单次抽卡失败: {single_result.get('message', '未知错误')}")
    
    # 5. 测试十连抽扣费
    ten_result = test_ten_draw_with_cost(user_id)
    if ten_result.get('status') == 'success':
        print(f"✅ 十连抽成功，剩余货币: {ten_result['data']['remaining_coins']}")
        print("   获得物品:")
        for i, item in enumerate(ten_result['data']['items'], 1):
            print(f"   {i}. {item['name']} ({item['rarity']})")
    else:
        print(f"❌ 十连抽失败: {ten_result.get('message', '未知错误')}")
    
    print("\n" + "=" * 50)
    print("🎯 货币系统测试完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
