#!/usr/bin/env python3
"""
测试抽卡概率API，验证排序功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

def test_rates_api():
    """测试概率API的排序功能"""
    print("🧪 测试抽卡概率API排序功能...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/draw/rates")
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success":
                rates_data = data["data"]
                
                print("✅ 概率API调用成功")
                print(f"📊 总权重: {rates_data.get('total_weight', 'N/A')}")
                print(f"🎯 稀有度排序: {rates_data.get('rarity_order', 'N/A')}")
                
                # 测试稀有度概率分布排序
                print("\n📈 稀有度概率分布 (按稀有度降序):")
                print(f"{'稀有度':<8} {'概率':<10} {'物品数':<8} {'期望抽数':<10}")
                print("-" * 40)
                
                rarity_rates = rates_data.get("rarity_rates", {})
                rarity_order = rates_data.get("rarity_order", ["神话", "传说", "史诗", "稀有", "普通"])
                
                for rarity in rarity_order:
                    if rarity in rarity_rates:
                        info = rarity_rates[rarity]
                        probability = info.get("probability", 0)
                        item_count = len(info.get("items", []))
                        expected_draws = int(100 / probability) if probability > 0 else float('inf')
                        expected_str = f"{expected_draws}抽" if expected_draws != float('inf') else "∞"
                        
                        print(f"{rarity:<8} {probability:<10.4f}% {item_count:<8} {expected_str:<10}")
                
                # 测试单个物品概率排序
                print("\n🎮 单个物品概率 (按稀有度降序):")
                print(f"{'物品名称':<15} {'稀有度':<8} {'概率':<12} {'期望抽数':<10}")
                print("-" * 50)
                
                individual_rates = rates_data.get("individual_rates", [])
                
                for rate in individual_rates[:10]:  # 只显示前10个
                    item = rate.get("item", {})
                    probability = rate.get("probability", 0)
                    expected_draws = int(100 / probability) if probability > 0 else float('inf')
                    expected_str = f"{expected_draws}抽" if expected_draws != float('inf') else "∞"
                    
                    print(f"{item.get('name', 'N/A'):<15} {item.get('rarity', 'N/A'):<8} {probability:<12.4f}% {expected_str:<10}")
                
                if len(individual_rates) > 10:
                    print(f"... 还有 {len(individual_rates) - 10} 个物品")
                
                # 验证排序是否正确
                print("\n🔍 排序验证:")
                current_rarity_index = -1
                is_sorted = True
                
                for rate in individual_rates:
                    item = rate.get("item", {})
                    rarity = item.get("rarity", "")
                    rarity_index = rarity_order.index(rarity) if rarity in rarity_order else 999
                    
                    if rarity_index < current_rarity_index:
                        is_sorted = False
                        break
                    current_rarity_index = rarity_index
                
                if is_sorted:
                    print("✅ 物品概率排序正确 (按稀有度降序)")
                else:
                    print("❌ 物品概率排序错误")
                
                # 验证稀有度分布排序
                rarity_list = list(rarity_rates.keys())
                expected_order = [r for r in rarity_order if r in rarity_rates]
                
                print(f"🎯 稀有度分布顺序: {rarity_list}")
                print(f"🎯 期望排序顺序: {expected_order}")
                
                if rarity_list == expected_order:
                    print("✅ 稀有度分布排序正确")
                else:
                    print("❌ 稀有度分布排序可能需要前端处理")
                
            else:
                print(f"❌ API返回错误: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ API调用失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
            test_rates_api()
        else:
            print("❌ 后端服务器无响应，请先启动服务器")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://127.0.0.1:5000 运行")
    except Exception as e:
        print(f"❌ 测试异常: {e}")
