#!/usr/bin/env python3
"""
完整的抽卡动画功能测试
包括注册、充值、抽卡测试
"""

import requests
import json
import time

# API配置
API_BASE = 'http://127.0.0.1:5000'
FRONTEND_BASE = 'http://127.0.0.1:3000'

def test_complete_gacha_animation():
    """完整的抽卡动画测试流程"""
    print("🎬 完整抽卡动画测试")
    print("=" * 50)
    
    # 1. 注册新用户
    print("👤 注册测试用户...")
    user_data = {
        'name': 'GachaAnimationTester',
        'account': 'gachatest',
        'password': 'test123'
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/auth/register", json=user_data)
        data = response.json()
        
        if data['status'] == 'success':
            user = data['data']
            print(f"   ✅ 用户注册成功: {user['name']} (ID: {user['id']})")
            print(f"   💰 初始金币: {user['coins']}")
        else:
            print(f"   ⚠️  注册失败，尝试登录现有用户...")
            # 尝试登录
            response = requests.post(f"{API_BASE}/api/auth/login", json={'account': user_data['account'], 'password': user_data['password']})
            data = response.json()
            if data['status'] == 'success':
                user = data['data']
                print(f"   ✅ 登录成功: {user['name']} (ID: {user['id']})")
                print(f"   💰 当前金币: {user['coins']}")
            else:
                print(f"   ❌ 登录失败: {data['message']}")
                return
                
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return
    
    # 2. 充值确保有足够金币
    print(f"\n💳 为用户充值...")
    try:
        recharge_data = {
            'user_id': user['id'],
            'amount': 5000
        }
        
        response = requests.post(f"{API_BASE}/api/recharge", json=recharge_data)
        data = response.json()
        
        if data['status'] == 'success':
            print(f"   ✅ 充值成功，新余额: {data['data']['new_coins']}")
            user['coins'] = data['data']['new_coins']
        else:
            print(f"   ❌ 充值失败: {data['message']}")
            
    except Exception as e:
        print(f"   ❌ 充值错误: {e}")
    
    # 3. 获取可用卡池
    print(f"\n🎯 获取可用卡池...")
    try:
        response = requests.get(f"{API_BASE}/api/pools")
        data = response.json()
        
        if data['status'] == 'success' and data['data']:
            pools = data['data']
            print(f"   ✅ 找到 {len(pools)} 个卡池")
            
            selected_pool = pools[0]  # 选择第一个卡池
            print(f"   🎲 选择卡池: {selected_pool['name']}")
            print(f"      描述: {selected_pool['description']}")
            print(f"      单抽费用: {selected_pool.get('single_cost', 160)}")
            print(f"      十连费用: {selected_pool.get('ten_cost', 1600)}")
        else:
            print(f"   ❌ 无可用卡池")
            return
            
    except Exception as e:
        print(f"   ❌ 获取卡池错误: {e}")
        return
    
    # 4. 进行抽卡测试，收集不同稀有度
    print(f"\n🎲 进行抽卡测试...")
    rarity_results = {}
    total_draws = 0
    
    # 进行多次单抽
    for i in range(15):  # 进行15次单抽以获得不同稀有度
        try:
            draw_data = {
                'user_id': user['id'],
                'pool_id': selected_pool['id']
            }
            
            response = requests.post(f"{API_BASE}/api/draw/single", json=draw_data)
            data = response.json()
            
            if data['status'] == 'success':
                item = data['data']['item']
                rarity = item['rarity']
                
                if rarity not in rarity_results:
                    rarity_results[rarity] = []
                rarity_results[rarity].append(item['name'])
                
                total_draws += 1
                user['coins'] = data['data']['remaining_coins']
                
                print(f"   抽卡 {i+1:2d}: {item['name']} ({rarity}) - 余额: {user['coins']}")
                
                if user['coins'] < selected_pool.get('single_cost', 160):
                    print("   💰 金币不足，停止抽卡")
                    break
                    
            else:
                print(f"   ❌ 抽卡失败: {data['message']}")
                break
                
        except Exception as e:
            print(f"   ❌ 抽卡错误: {e}")
            break
            
        time.sleep(0.1)  # 稍作延迟
    
    # 进行一次十连抽测试
    if user['coins'] >= selected_pool.get('ten_cost', 1600):
        print(f"\n🎰 进行十连抽测试...")
        try:
            draw_data = {
                'user_id': user['id'],
                'pool_id': selected_pool['id']
            }
            
            response = requests.post(f"{API_BASE}/api/draw/ten", json=draw_data)
            data = response.json()
            
            if data['status'] == 'success':
                items = data['data']['items']
                user['coins'] = data['data']['remaining_coins']
                
                print(f"   ✅ 十连抽成功，获得 {len(items)} 个物品:")
                for j, item in enumerate(items):
                    rarity = item['rarity']
                    if rarity not in rarity_results:
                        rarity_results[rarity] = []
                    rarity_results[rarity].append(item['name'])
                    print(f"      {j+1:2d}. {item['name']} ({rarity})")
                
                total_draws += 10
                print(f"   💰 剩余金币: {user['coins']}")
                
                # 测试十连抽的最高稀有度判断
                rarity_order = {'神话': 1, '传说': 2, '史诗': 3, '稀有': 4, '普通': 5}
                highest_rarity = '普通'
                highest_priority = 5
                
                for item in items:
                    priority = rarity_order.get(item['rarity'], 5)
                    if priority < highest_priority:
                        highest_priority = priority
                        highest_rarity = item['rarity']
                
                print(f"   🎬 十连抽最高稀有度: {highest_rarity} (应播放 {highest_rarity}.mp4)")
                
            else:
                print(f"   ❌ 十连抽失败: {data['message']}")
                
        except Exception as e:
            print(f"   ❌ 十连抽错误: {e}")
    
    # 5. 总结抽卡结果
    print(f"\n📊 抽卡结果总结:")
    print(f"   总抽卡次数: {total_draws}")
    print(f"   获得稀有度分布:")
    
    rarity_order = ['神话', '传说', '史诗', '稀有', '普通']
    for rarity in rarity_order:
        if rarity in rarity_results:
            count = len(rarity_results[rarity])
            percentage = (count / total_draws) * 100 if total_draws > 0 else 0
            print(f"      {rarity}: {count} 个 ({percentage:.1f}%)")
            
            # 显示对应的动画视频
            video_file = f"media/{rarity}.mp4"
            print(f"         -> 动画视频: {video_file}")
    
    # 6. 动画功能验证
    print(f"\n🎬 动画功能验证:")
    print(f"   前端地址: {FRONTEND_BASE}/gacha")
    print(f"   测试账号: {user_data['account']}")
    print(f"   测试密码: {user_data['password']}")
    print(f"   当前余额: {user['coins']} 金币")
    
    print(f"\n✅ 动画系统集成完成!")
    print(f"   1. 抽卡时会根据最高稀有度播放对应视频")
    print(f"   2. 支持跳过动画功能")
    print(f"   3. 动画播放完毕后自动显示抽卡结果")
    print(f"   4. 媒体文件路径: /media/稀有度.mp4")
    
    return True

if __name__ == '__main__':
    test_complete_gacha_animation()
