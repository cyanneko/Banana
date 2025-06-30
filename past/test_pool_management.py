#!/usr/bin/env python3
"""
测试卡池管理系统
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

def test_pool_management():
    """测试卡池管理功能"""
    print("🧪 测试卡池管理系统...")
    
    # 管理员ID (fhc)
    admin_id = 1
    
    # 1. 获取所有卡池
    print("\n📋 获取所有卡池...")
    try:
        response = requests.get(f"{BASE_URL}/api/pools")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                pools = data["data"]
                print("✅ 卡池列表获取成功:")
                for pool in pools:
                    print(f"   - ID: {pool['id']}, 名称: {pool['name']}, 描述: {pool['description']}")
            else:
                print(f"❌ 获取失败: {data.get('message')}")
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 2. 获取卡池详情
    print("\n🔍 获取标准卡池详情...")
    try:
        response = requests.get(f"{BASE_URL}/api/pools/1")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                pool_info = data["data"]
                print(f"✅ 卡池详情: {pool_info['pool']['name']}")
                print(f"   物品数量: {pool_info['total_items']}")
                print("   包含物品:")
                for item_info in pool_info['items'][:5]:  # 只显示前5个
                    item = item_info['item']
                    weight = item_info['weight']
                    print(f"     - {item['name']} ({item['rarity']}) - 权重: {weight}")
                if pool_info['total_items'] > 5:
                    print(f"     ... 还有 {pool_info['total_items'] - 5} 个物品")
            else:
                print(f"❌ 获取失败: {data.get('message')}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 3. 创建新卡池
    print("\n🆕 创建新卡池...")
    new_pool_data = {
        "admin_id": admin_id,
        "name": "测试卡池",
        "description": "用于测试的临时卡池",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/pools", json=new_pool_data)
        if response.status_code == 201:
            data = response.json()
            if data.get("status") == "success":
                new_pool = data["data"]
                new_pool_id = new_pool["id"]
                print(f"✅ 新卡池创建成功: {new_pool['name']} (ID: {new_pool_id})")
                
                # 4. 向新卡池添加物品
                print(f"\n➕ 向卡池 {new_pool_id} 添加物品...")
                
                # 添加几个物品到新卡池
                items_to_add = [
                    {"item_id": 1, "weight": 0.5},  # 能量剑，提高权重
                    {"item_id": 2, "weight": 3},    # 雾切之回光，提高权重
                    {"item_id": 5, "weight": 50},   # 剑，作为填充
                ]
                
                for item_data in items_to_add:
                    add_data = {
                        "admin_id": admin_id,
                        "item_id": item_data["item_id"],
                        "weight": item_data["weight"]
                    }
                    
                    add_response = requests.post(f"{BASE_URL}/api/pools/{new_pool_id}/items", json=add_data)
                    if add_response.status_code == 200:
                        add_result = add_response.json()
                        if add_result.get("status") == "success":
                            print(f"   ✅ 物品添加成功: {add_result.get('message')}")
                        else:
                            print(f"   ❌ 物品添加失败: {add_result.get('message')}")
                    else:
                        print(f"   ❌ 添加物品请求失败: HTTP {add_response.status_code}")
                
                # 5. 更新物品权重
                print(f"\n🔧 更新物品权重...")
                update_data = {
                    "admin_id": admin_id,
                    "weight": 1.0  # 将能量剑权重改为1.0
                }
                
                update_response = requests.put(f"{BASE_URL}/api/pools/{new_pool_id}/items/1", json=update_data)
                if update_response.status_code == 200:
                    update_result = update_response.json()
                    if update_result.get("status") == "success":
                        print(f"   ✅ 权重更新成功: {update_result.get('message')}")
                    else:
                        print(f"   ❌ 权重更新失败: {update_result.get('message')}")
                
                # 6. 获取新卡池的概率
                print(f"\n📊 获取卡池 {new_pool_id} 的抽卡概率...")
                rates_response = requests.get(f"{BASE_URL}/api/pools/{new_pool_id}/rates")
                if rates_response.status_code == 200:
                    rates_data = rates_response.json()
                    if rates_data.get("status") == "success":
                        rates_info = rates_data["data"]
                        print(f"   ✅ 概率计算成功")
                        print(f"   总权重: {rates_info['total_weight']}")
                        print("   稀有度概率:")
                        for rarity, info in rates_info['rarity_rates'].items():
                            print(f"     {rarity}: {info['probability']}%")
                        print("   物品概率:")
                        for rate in rates_info['individual_rates']:
                            item = rate['item']
                            print(f"     {item['name']}: {rate['probability']}% (权重: {rate['weight']})")
                
                # 7. 测试从新卡池抽卡
                print(f"\n🎲 测试从卡池 {new_pool_id} 抽卡...")
                draw_data = {
                    "user_id": admin_id,
                    "pool_id": new_pool_id
                }
                
                draw_response = requests.post(f"{BASE_URL}/api/draw/single", json=draw_data)
                if draw_response.status_code == 200:
                    draw_result = draw_response.json()
                    if draw_result.get("status") == "success":
                        item = draw_result["data"]["item"]
                        pool = draw_result["data"]["pool"]
                        print(f"   ✅ 抽卡成功! 从 {pool['name']} 获得: {item['name']} ({item['rarity']})")
                    else:
                        print(f"   ❌ 抽卡失败: {draw_result.get('message')}")
                
                # 8. 清理：删除测试卡池
                print(f"\n🗑️ 清理测试卡池...")
                delete_data = {"admin_id": admin_id}
                delete_response = requests.delete(f"{BASE_URL}/api/pools/{new_pool_id}", json=delete_data)
                if delete_response.status_code == 200:
                    delete_result = delete_response.json()
                    if delete_result.get("status") == "success":
                        print(f"   ✅ 测试卡池删除成功")
                    else:
                        print(f"   ❌ 删除失败: {delete_result.get('message')}")
                
            else:
                print(f"❌ 创建失败: {data.get('message')}")
        else:
            print(f"❌ 创建请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    print("\n🎉 卡池管理系统测试完成!")

def test_pool_selection():
    """测试卡池选择抽卡功能"""
    print("\n🎯 测试卡池选择抽卡...")
    
    # 测试从不同卡池抽卡
    test_cases = [
        {"pool_id": 1, "pool_name": "标准卡池"},
        {"pool_id": 2, "pool_name": "神话限定池"}
    ]
    
    for case in test_cases:
        print(f"\n🎲 测试 {case['pool_name']} (ID: {case['pool_id']})...")
        
        # 获取卡池概率
        try:
            rates_response = requests.get(f"{BASE_URL}/api/pools/{case['pool_id']}/rates")
            if rates_response.status_code == 200:
                rates_data = rates_response.json()
                if rates_data.get("status") == "success":
                    rates_info = rates_data["data"]
                    print(f"   📊 {case['pool_name']} 概率分布:")
                    for rarity, info in rates_info['rarity_rates'].items():
                        print(f"     {rarity}: {info['probability']}% ({len(info['items'])}个物品)")
                else:
                    print(f"   ❌ 获取概率失败: {rates_data.get('message')}")
            
            # 模拟抽卡（不实际扣费，只是展示功能）
            print(f"   💡 可以使用 pool_id={case['pool_id']} 参数进行抽卡")
            
        except Exception as e:
            print(f"   ❌ 异常: {e}")

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
            test_pool_management()
            test_pool_selection()
        else:
            print("❌ 后端服务器无响应，请先启动服务器")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://127.0.0.1:5000 运行")
    except Exception as e:
        print(f"❌ 测试异常: {e}")
