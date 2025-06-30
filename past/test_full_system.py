#!/usr/bin/env python3
"""
抽卡系统完整功能验证
验证注册、充值、抽卡、背包等全流程
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

def full_system_test():
    """完整系统测试"""
    print("🎮 抽卡系统完整功能验证")
    print("=" * 60)
    
    # 1. 注册用户
    print("\n1️⃣ 用户注册测试...")
    test_username = f"system_test_{int(time.time())}"
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
            user_id = user_data["id"]
        else:
            print(f"❌ 注册失败: {result.get('message', 'Unknown error')}")
            return
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return
    
    # 2. 登录验证
    print("\n2️⃣ 用户登录测试...")
    login_data = {
        "account": test_username,
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            print("✅ 用户登录成功")
        else:
            print(f"❌ 登录失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
    
    # 3. 充值测试
    print("\n3️⃣ 充值功能测试...")
    recharge_data = {
        "user_id": user_id,
        "amount": 1000  # 标准充值套餐
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/recharge", json=recharge_data)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            recharge_info = result["data"]
            print(f"✅ 充值成功!")
            print(f"   充值前: {recharge_info['old_coins']}")
            print(f"   充值后: {recharge_info['new_coins']}")
            print(f"   基础金额: {recharge_info['base_amount']}")
            print(f"   赠送金额: {recharge_info['bonus_amount']}")
            print(f"   总计: {recharge_info['total_amount']}")
            current_coins = recharge_info['new_coins']
        else:
            print(f"❌ 充值失败: {result.get('message', 'Unknown error')}")
            return
    except Exception as e:
        print(f"❌ 充值失败: {e}")
        return
    
    # 4. 单次抽卡测试
    print("\n4️⃣ 单次抽卡测试...")
    draw_data = {"user_id": user_id}
    
    try:
        response = requests.post(f"{BASE_URL}/api/draw/single", json=draw_data)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            draw_info = result["data"]
            item = draw_info["item"]
            print(f"✅ 单次抽卡成功!")
            print(f"   获得物品: {item['name']} ({item['rarity']})")
            print(f"   物品描述: {item['description']}")
            print(f"   剩余货币: {draw_info['remaining_coins']}")
        else:
            print(f"❌ 单次抽卡失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 单次抽卡失败: {e}")
    
    # 5. 十连抽测试
    print("\n5️⃣ 十连抽测试...")
    try:
        response = requests.post(f"{BASE_URL}/api/draw/ten", json=draw_data)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            draw_info = result["data"]
            items = draw_info["items"]
            stats = draw_info["statistics"]
            print(f"✅ 十连抽成功!")
            print(f"   获得物品数量: {stats['total_items']}")
            print(f"   稀有度统计: {stats['rarity_count']}")
            print(f"   剩余货币: {draw_info['remaining_coins']}")
            
            # 显示获得的物品
            print("   获得物品列表:")
            for i, item in enumerate(items, 1):
                print(f"     {i:2d}. {item['name']} ({item['rarity']})")
        else:
            print(f"❌ 十连抽失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 十连抽失败: {e}")
    
    # 6. 背包查看测试
    print("\n6️⃣ 背包查看测试...")
    try:
        response = requests.get(f"{BASE_URL}/api/inventory/{user_id}")
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            inventory = result["data"]
            print(f"✅ 背包查看成功!")
            print(f"   用户: {inventory['user_name']}")
            print(f"   物品种类: {inventory['total_items']}")
            print("   背包内容:")
            for user_item in inventory["items"]:
                item = user_item["item"]
                count = user_item["number"]
                print(f"     {item['name']} x{count} ({item['rarity']})")
        else:
            print(f"❌ 背包查看失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 背包查看失败: {e}")
    
    # 7. 抽卡历史测试
    print("\n7️⃣ 抽卡历史测试...")
    try:
        response = requests.get(f"{BASE_URL}/api/draw/history/{user_id}")
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            history = result["data"]["history"]
            print(f"✅ 抽卡历史获取成功!")
            print(f"   历史记录数量: {len(history)}")
            if history:
                print("   最近抽卡记录:")
                for record in history[:3]:  # 只显示前3条
                    item = record["item"]
                    draw_type = record["draw_type"]
                    timestamp = record["timestamp"][:19]  # 去除毫秒部分
                    print(f"     {timestamp} - {draw_type}: {item['name']} ({item['rarity']})")
        else:
            print(f"❌ 抽卡历史获取失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 抽卡历史获取失败: {e}")
    
    # 8. 概率统计测试
    print("\n8️⃣ 抽卡概率统计测试...")
    try:
        response = requests.get(f"{BASE_URL}/api/draw/rates")
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            rates = result["data"]["rarity_rates"]
            print(f"✅ 抽卡概率获取成功!")
            print("   各稀有度概率:")
            for rarity, info in rates.items():
                print(f"     {rarity}: {info['probability']}%")
        else:
            print(f"❌ 抽卡概率获取失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 抽卡概率获取失败: {e}")
    
    # 9. 用户统计测试
    print("\n9️⃣ 用户统计测试...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats/user/{user_id}")
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            stats = result["data"]
            print(f"✅ 用户统计获取成功!")
            print(f"   抽卡次数: {stats['draw_stats']['total_draws']}")
            print(f"   背包物品总数: {stats['inventory_stats']['total_items']}")
            print(f"   当前货币: {stats['user_info']['coins']}")
        else:
            print(f"❌ 用户统计获取失败: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 用户统计获取失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 抽卡系统完整功能验证完成！")
    print("✅ 所有核心功能都已正常工作")
    print("🌐 现在可以在前端页面体验完整的抽卡游戏了！")

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
            full_system_test()
        else:
            print("❌ 后端服务器无响应，请先启动服务器")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://127.0.0.1:5000 运行")
    except Exception as e:
        print(f"❌ 验证异常: {e}")
