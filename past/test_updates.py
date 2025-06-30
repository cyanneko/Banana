#!/usr/bin/env python3
"""
测试更新后的功能
1. 卡池概率根据选择的卡池动态显示
2. 管理员界面功能
3. 编码问题修复
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

def test_pools_api():
    """测试卡池API"""
    print("🧪 测试卡池API...")
    
    # 1. 获取卡池列表
    print("📋 获取卡池列表...")
    response = requests.get(f"{BASE_URL}/api/pools")
    if response.status_code != 200:
        print("❌ 获取卡池失败")
        return False
    
    pools_data = response.json()
    pools = pools_data.get('data', [])
    print(f"✅ 获取到 {len(pools)} 个卡池")
    
    # 验证每个卡池的编码是否正常
    for pool in pools:
        pool_name = pool['name']
        if '?' in pool_name or '\\u' in str(pool):
            print(f"❌ 卡池名称编码异常: {pool}")
        else:
            print(f"✅ 卡池编码正常: {pool_name}")
    
    return True

def test_pool_rates():
    """测试卡池概率API"""
    print("\n🎯 测试卡池概率API...")
    
    # 获取卡池列表
    response = requests.get(f"{BASE_URL}/api/pools")
    pools = response.json().get('data', [])
    
    for pool in pools:
        pool_id = pool['id']
        pool_name = pool['name']
        
        print(f"\n📊 测试卡池 {pool_name} (ID: {pool_id}) 的概率...")
        
        # 获取卡池特定概率
        response = requests.get(f"{BASE_URL}/api/pools/{pool_id}/rates")
        if response.status_code != 200:
            print(f"❌ 获取卡池{pool_id}概率失败")
            continue
        
        rates_data = response.json()
        if rates_data['status'] != 'success':
            print(f"❌ 概率API返回错误: {rates_data.get('message', '未知错误')}")
            continue
        
        rates = rates_data['data']
        print(f"✅ 卡池概率获取成功")
        print(f"   📦 卡池: {rates['pool']['name']}")
        print(f"   💰 单抽价格: {rates['pool'].get('single_cost', 160)}")
        print(f"   💰 十连价格: {rates['pool'].get('ten_cost', 1600)}")
        print(f"   🎲 总权重: {rates['total_weight']}")
        
        # 显示稀有度分布
        if 'rarity_rates' in rates:
            print(f"   📈 稀有度分布:")
            for rarity, info in rates['rarity_rates'].items():
                print(f"      {rarity}: {info['probability']}% ({info['items']}个物品)")

def test_admin_functionality():
    """测试管理员功能"""
    print("\n🛠️ 测试管理员功能...")
    
    # 管理员登录
    admin_data = {
        "account": "fhc",
        "password": "114514"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_data)
    if response.status_code != 200:
        print("❌ 管理员登录失败")
        return False
    
    login_result = response.json()
    if login_result['status'] != 'success':
        print(f"❌ 管理员登录失败: {login_result.get('message', '未知错误')}")
        return False
    
    print("✅ 管理员登录成功")
    admin_id = login_result['data']['id']
    
    # 测试创建卡池
    print("🆕 测试创建卡池...")
    new_pool_data = {
        "name": "测试高级卡池",
        "description": "用于测试的高级卡池，价格更高",
        "single_cost": 250,
        "ten_cost": 2200,
        "is_active": True,
        "admin_id": admin_id
    }
    
    response = requests.post(f"{BASE_URL}/api/pools", json=new_pool_data)
    if response.status_code == 201:
        create_result = response.json()
        if create_result['status'] == 'success':
            test_pool_id = create_result['data']['id']
            print(f"✅ 测试卡池创建成功 (ID: {test_pool_id})")
            
            # 测试向卡池添加物品
            print("➕ 测试添加物品到卡池...")
            add_item_data = {
                "admin_id": admin_id,
                "item_id": 1,  # 能量剑
                "weight": 0.5
            }
            
            response = requests.post(f"{BASE_URL}/api/pools/{test_pool_id}/items", json=add_item_data)
            if response.status_code == 200:
                print("✅ 物品添加成功")
            else:
                print("❌ 物品添加失败")
            
            # 清理测试卡池
            print("🗑️ 清理测试卡池...")
            delete_data = {"admin_id": admin_id}
            response = requests.delete(f"{BASE_URL}/api/pools/{test_pool_id}", json=delete_data)
            if response.status_code == 200:
                print("✅ 测试卡池清理完成")
            else:
                print("❌ 测试卡池清理失败")
        else:
            print(f"❌ 卡池创建失败: {create_result.get('message', '未知错误')}")
    else:
        print("❌ 卡池创建请求失败")

def test_encoding():
    """测试中文编码"""
    print("\n🔤 测试中文编码...")
    
    # 创建包含中文的卡池
    admin_data = {
        "name": "中文测试卡池",
        "description": "测试中文编码是否正常显示",
        "single_cost": 200,
        "ten_cost": 1800,
        "admin_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/pools", json=admin_data)
    if response.status_code == 201:
        result = response.json()
        if result['status'] == 'success':
            pool_id = result['data']['id']
            pool_name = result['data']['name']
            print(f"✅ 中文卡池创建成功: {pool_name}")
            
            # 清理
            delete_data = {"admin_id": 1}
            requests.delete(f"{BASE_URL}/api/pools/{pool_id}", json=delete_data)
            print("✅ 中文编码测试完成")
        else:
            print("❌ 中文卡池创建失败")
    else:
        print("❌ 中文编码测试失败")

def main():
    """主函数"""
    print("🧪 功能更新测试")
    print("=" * 50)
    
    # 测试后端健康状态
    if not test_health():
        return
    
    # 测试卡池API
    test_pools_api()
    
    # 测试卡池概率
    test_pool_rates()
    
    # 测试管理员功能
    test_admin_functionality()
    
    # 测试编码
    test_encoding()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    main()
