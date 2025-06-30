#!/usr/bin/env python3
"""
测试抽卡动画功能
验证抽卡动画系统是否正常工作
"""

import requests
import json
import time

# API配置
API_BASE = 'http://127.0.0.1:5000'
FRONTEND_BASE = 'http://127.0.0.1:3000'

def test_media_files():
    """测试媒体文件是否可以正常访问"""
    print("🎬 测试媒体文件访问...")
    
    video_files = ['神话.mp4', '传说.mp4', '史诗.mp4', '稀有.mp4', '普通.mp4']
    
    for video in video_files:
        try:
            response = requests.head(f"{FRONTEND_BASE}/media/{video}")
            if response.status_code == 200:
                print(f"   ✅ {video} - 可访问")
            else:
                print(f"   ❌ {video} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {video} - 错误: {e}")

def test_user_creation_and_recharge():
    """测试用户创建和充值"""
    print("\n👤 测试用户创建和充值...")
    
    # 创建测试用户
    user_data = {
        'name': 'test_animation_user',
        'account': 'test_anim',
        'password': 'test123'
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/users/add", json=user_data)
        data = response.json()
        
        if data['status'] == 'success':
            user_id = data['data']['user']['id']
            print(f"   ✅ 用户创建成功，ID: {user_id}")
            
            # 充值
            recharge_data = {
                'user_id': user_id,
                'amount': 5000
            }
            
            response = requests.post(f"{API_BASE}/api/recharge", json=recharge_data)
            data = response.json()
            
            if data['status'] == 'success':
                print(f"   ✅ 充值成功，余额: {data['data']['new_coins']}")
                return user_id
            else:
                print(f"   ❌ 充值失败: {data['message']}")
        else:
            print(f"   ❌ 用户创建失败: {data['message']}")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    return None

def test_gacha_draws(user_id):
    """测试抽卡功能，验证不同稀有度"""
    print(f"\n🎲 测试抽卡功能 (用户ID: {user_id})...")
    
    # 获取可用卡池
    try:
        response = requests.get(f"{API_BASE}/api/pools/all")
        data = response.json()
        
        if data['status'] == 'success' and data['data']['pools']:
            pool = data['data']['pools'][0]  # 使用第一个卡池
            pool_id = pool['id']
            print(f"   使用卡池: {pool['name']}")
            
            # 进行多次抽卡以获得不同稀有度
            results = []
            for i in range(10):  # 抽10次
                try:
                    draw_data = {
                        'user_id': user_id,
                        'pool_id': pool_id
                    }
                    
                    response = requests.post(f"{API_BASE}/api/draw/single", json=draw_data)
                    data = response.json()
                    
                    if data['status'] == 'success':
                        item = data['data']['item']
                        results.append(item)
                        print(f"   抽卡 {i+1}: {item['name']} ({item['rarity']})")
                    else:
                        print(f"   ❌ 抽卡失败: {data['message']}")
                        break
                        
                except Exception as e:
                    print(f"   ❌ 抽卡错误: {e}")
                    break
                    
                time.sleep(0.1)  # 稍作延迟
            
            # 统计抽卡结果
            if results:
                print(f"\n📊 抽卡结果统计:")
                rarity_count = {}
                for item in results:
                    rarity = item['rarity']
                    rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
                
                for rarity, count in rarity_count.items():
                    print(f"   {rarity}: {count}个")
                
                return results
        else:
            print("   ❌ 无可用卡池")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    return []

def test_animation_logic():
    """测试抽卡动画逻辑"""
    print(f"\n🎥 测试抽卡动画逻辑...")
    
    # 模拟不同稀有度的抽卡结果
    test_cases = [
        [{'name': '基础道具', 'rarity': '普通'}],
        [{'name': '蓝色装备', 'rarity': '稀有'}],
        [{'name': '紫色武器', 'rarity': '史诗'}],
        [{'name': '金色神器', 'rarity': '传说'}],
        [{'name': '红色至宝', 'rarity': '神话'}],
        [
            {'name': '基础道具', 'rarity': '普通'},
            {'name': '金色神器', 'rarity': '传说'},
            {'name': '蓝色装备', 'rarity': '稀有'}
        ]  # 混合稀有度，应该选择最高的"传说"
    ]
    
    rarity_order = {
        '神话': 1,
        '传说': 2,
        '史诗': 3,
        '稀有': 4,
        '普通': 5
    }
    
    video_map = {
        '神话': 'media/神话.mp4',
        '传说': 'media/传说.mp4',
        '史诗': 'media/史诗.mp4',
        '稀有': 'media/稀有.mp4',
        '普通': 'media/普通.mp4'
    }
    
    for i, items in enumerate(test_cases):
        # 计算最高稀有度
        highest_rarity = '普通'
        highest_priority = 5
        
        for item in items:
            rarity = item['rarity']
            priority = rarity_order.get(rarity, 5)
            if priority < highest_priority:
                highest_priority = priority
                highest_rarity = rarity
        
        expected_video = video_map[highest_rarity]
        item_names = [item['name'] for item in items]
        
        print(f"   测试 {i+1}: {item_names}")
        print(f"      最高稀有度: {highest_rarity}")
        print(f"      应播放视频: {expected_video}")

def main():
    """主测试函数"""
    print("🎬 抽卡动画功能测试")
    print("=" * 50)
    
    # 测试媒体文件访问
    test_media_files()
    
    # 测试用户创建和充值
    user_id = test_user_creation_and_recharge()
    
    if user_id:
        # 测试抽卡功能
        results = test_gacha_draws(user_id)
        
        if results:
            print(f"\n✅ 抽卡功能正常，共获得 {len(results)} 个物品")
    
    # 测试动画逻辑
    test_animation_logic()
    
    print("\n" + "=" * 50)
    print("🎯 测试总结:")
    print("1. 媒体文件访问 - 检查上面的结果")
    print("2. 用户创建和充值 - 检查上面的结果")
    print("3. 抽卡功能 - 检查上面的结果")
    print("4. 动画逻辑 - 检查上面的结果")
    print("\n📱 前端测试:")
    print(f"   访问 {FRONTEND_BASE}/gacha 进行实际测试")
    print("   登录后进行抽卡，查看动画是否正常播放")

if __name__ == '__main__':
    main()
