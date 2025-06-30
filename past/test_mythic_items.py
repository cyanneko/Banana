"""
神话品级测试脚本
测试新添加的神话品级功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_mythic_items():
    """测试神话品级物品"""
    print("🔥 测试神话品级功能")
    print("=" * 50)
    
    # 1. 测试物品列表
    print("📦 获取物品列表...")
    response = requests.get(f"{BASE_URL}/api/items")
    data = response.json()
    
    if data['status'] == 'success':
        items = data['data']
        print("物品列表:")
        for item in items:
            rarity_emoji = {
                '神话': '🔥',
                '传说': '🏆', 
                '史诗': '💜',
                '稀有': '💙',
                '普通': '⚪'
            }
            emoji = rarity_emoji.get(item['rarity'], '❓')
            print(f"  {emoji} {item['name']} - {item['rarity']} (权重: {item['weight']})")
    
    # 2. 测试抽卡概率
    print(f"\n📊 获取抽卡概率...")
    response = requests.get(f"{BASE_URL}/api/draw/rates")
    data = response.json()
    
    if data['status'] == 'success':
        rates = data['data']
        print("稀有度概率:")
        for rarity, info in rates['rarity_rates'].items():
            rarity_emoji = {
                '神话': '🔥',
                '传说': '🏆', 
                '史诗': '💜',
                '稀有': '💙',
                '普通': '⚪'
            }
            emoji = rarity_emoji.get(rarity, '❓')
            print(f"  {emoji} {rarity}: {info['probability']}% (权重: {info['weight']})")
    
    # 3. 测试用户登录
    print(f"\n🔐 用户登录...")
    login_data = {
        "account": "fhc",
        "password": "114514"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    data = response.json()
    
    if data['status'] == 'success':
        user = data['data']
        user_id = user['id']
        print(f"✅ 登录成功，用户ID: {user_id}，当前货币: {user.get('coins', 0)}")
        
        # 4. 进行多次抽卡测试，看看能否抽到神话
        print(f"\n🎲 进行抽卡测试...")
        mythic_count = 0
        total_draws = 0
        
        for i in range(10):  # 进行10次十连抽测试
            response = requests.post(f"{BASE_URL}/api/draw/ten", json={"user_id": user_id})
            draw_data = response.json()
            
            if draw_data['status'] == 'success':
                items = draw_data['data']['items']
                total_draws += 10
                
                # 统计抽到的物品
                round_mythic = 0
                round_legendary = 0
                round_epic = 0
                round_rare = 0
                round_common = 0
                
                for item in items:
                    if item['rarity'] == '神话':
                        round_mythic += 1
                        mythic_count += 1
                    elif item['rarity'] == '传说':
                        round_legendary += 1
                    elif item['rarity'] == '史诗':
                        round_epic += 1
                    elif item['rarity'] == '稀有':
                        round_rare += 1
                    elif item['rarity'] == '普通':
                        round_common += 1
                
                print(f"  第{i+1}轮十连: 🔥神话x{round_mythic} 🏆传说x{round_legendary} 💜史诗x{round_epic} 💙稀有x{round_rare} ⚪普通x{round_common}")
                
                if round_mythic > 0:
                    print("  🎉 恭喜！抽到神话物品！")
                    for item in items:
                        if item['rarity'] == '神话':
                            print(f"    🔥 {item['name']}: {item['description']}")
            else:
                print(f"  ❌ 第{i+1}轮抽卡失败: {draw_data.get('message', '未知错误')}")
                break
        
        print(f"\n📈 测试结果统计:")
        print(f"  总抽卡次数: {total_draws}")
        print(f"  神话物品数量: {mythic_count}")
        if total_draws > 0:
            mythic_rate = (mythic_count / total_draws) * 100
            print(f"  神话出货率: {mythic_rate:.2f}%")
        
        # 5. 查看最终背包
        print(f"\n🎒 查看背包...")
        response = requests.get(f"{BASE_URL}/api/inventory/{user_id}")
        data = response.json()
        
        if data['status'] == 'success':
            items = data['data']['items']
            print("背包内容:")
            for user_item in items:
                item = user_item['item']
                count = user_item['number']
                rarity_emoji = {
                    '神话': '🔥',
                    '传说': '🏆', 
                    '史诗': '💜',
                    '稀有': '💙',
                    '普通': '⚪'
                }
                emoji = rarity_emoji.get(item['rarity'], '❓')
                print(f"  {emoji} {item['name']} x{count}")

if __name__ == "__main__":
    test_mythic_items()
