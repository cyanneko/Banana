#!/usr/bin/env python3
"""
卡池自定义价格测试
测试每个卡池是否正确使用了自定义的抽卡价格
"""

import requests
import json

# 后端API地址
BASE_URL = "http://localhost:5000"

def test_health():
    """测试后端服务器健康状态"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
            return True
        else:
            print("❌ 后端服务器响应异常")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到后端服务器: {e}")
        return False

def test_custom_prices():
    """测试卡池自定义价格功能"""
    print("🧪 测试卡池自定义价格系统...")
    
    # 1. 获取所有卡池
    print("📋 获取所有卡池...")
    response = requests.get(f"{BASE_URL}/api/pools")
    if response.status_code != 200:
        print("❌ 获取卡池失败")
        return False
    
    pools_data = response.json()
    pools = pools_data.get('data', [])
    print(f"✅ 获取到 {len(pools)} 个卡池")
    
    # 2. 显示每个卡池的价格信息
    for pool in pools:
        pool_id = pool['id']
        pool_name = pool['name']
        single_cost = pool.get('single_cost', 160)
        ten_cost = pool.get('ten_cost', 1600)
        print(f"   📦 {pool_name} (ID: {pool_id})")
        print(f"      💰 单抽: {single_cost} 货币")
        print(f"      💰 十连: {ten_cost} 货币")
    
    # 3. 测试不同卡池的抽卡价格
    print("\n🎲 测试不同卡池的抽卡价格...")
    
    test_user_id = 1
    
    for pool in pools:
        pool_id = pool['id']
        pool_name = pool['name']
        single_cost = pool.get('single_cost', 160)
        
        print(f"\n🎯 测试卡池: {pool_name}")
        
        # 获取用户当前货币数量
        response = requests.get(f"{BASE_URL}/api/users/{test_user_id}")
        if response.status_code != 200:
            print("❌ 无法获取用户信息")
            continue
        
        user_data = response.json()
        old_coins = user_data['data']['coins']
        print(f"   💰 抽卡前货币: {old_coins}")
        
        # 执行单抽
        draw_data = {
            "user_id": test_user_id,
            "pool_id": pool_id
        }
        
        response = requests.post(f"{BASE_URL}/api/draw/single", json=draw_data)
        if response.status_code != 200:
            print(f"❌ 抽卡失败: {response.text}")
            continue
        
        result = response.json()
        actual_cost = result['data']['draw_record']['cost']
        new_coins = result['data']['remaining_coins']
        item_name = result['data']['item']['name']
        
        print(f"   🎁 获得物品: {item_name}")
        print(f"   💸 实际花费: {actual_cost} 货币")
        print(f"   💰 剩余货币: {new_coins}")
        
        # 验证价格是否正确
        expected_cost_difference = old_coins - new_coins
        if actual_cost == single_cost and expected_cost_difference == single_cost:
            print(f"   ✅ 价格正确: 预期 {single_cost}，实际 {actual_cost}")
        else:
            print(f"   ❌ 价格错误: 预期 {single_cost}，实际 {actual_cost}")
            print(f"      货币变化: {expected_cost_difference}")
    
    print("\n🎉 卡池自定义价格测试完成!")

def main():
    """主函数"""
    print("🎲 卡池自定义价格测试")
    print("=" * 50)
    
    # 测试后端健康状态
    if not test_health():
        return
    
    # 测试自定义价格功能
    test_custom_prices()

if __name__ == "__main__":
    main()
