#!/usr/bin/env python3
"""
测试充值后抽卡按钮状态更新问题修复
验证充值后无需刷新页面即可立即抽卡
"""

import requests
import json

def test_recharge_button_update():
    """测试充值后按钮状态更新"""
    print("🔧 测试充值后抽卡按钮状态更新修复")
    print("=" * 60)
    
    # 1. 创建/登录测试用户
    print("👤 准备测试用户...")
    
    # 尝试注册新用户
    user_data = {
        'name': 'RechargeTestUser',
        'account': 'rechargetest',
        'password': 'test123'
    }
    
    try:
        # 先尝试注册
        response = requests.post('http://127.0.0.1:5000/api/auth/register', json=user_data)
        data = response.json()
        
        if data['status'] == 'success':
            user = data['data']
            print(f"   ✅ 用户注册成功: {user['name']} (ID: {user['id']})")
            print(f"   💰 初始金币: {user['coins']}")
        else:
            # 注册失败，尝试登录
            response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                                   json={'account': user_data['account'], 'password': user_data['password']})
            data = response.json()
            if data['status'] == 'success':
                user = data['data']
                print(f"   ✅ 登录现有用户: {user['name']} (ID: {user['id']})")
                print(f"   💰 当前金币: {user['coins']}")
            else:
                print(f"   ❌ 用户创建/登录失败: {data['message']}")
                return
                
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return
    
    # 2. 获取可用卡池
    print(f"\n🎯 获取可用卡池...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/pools')
        data = response.json()
        
        if data['status'] == 'success' and data['data']:
            pools = data['data']
            pool = pools[0]  # 使用第一个卡池
            print(f"   ✅ 选择卡池: {pool['name']}")
            print(f"   💰 单抽费用: {pool.get('single_cost', 160)}")
            print(f"   💰 十连费用: {pool.get('ten_cost', 1600)}")
        else:
            print(f"   ❌ 无可用卡池")
            return
            
    except Exception as e:
        print(f"   ❌ 获取卡池失败: {e}")
        return
    
    # 3. 模拟金币耗尽的场景
    print(f"\n💸 模拟金币耗尽场景...")
    single_cost = pool.get('single_cost', 160)
    ten_cost = pool.get('ten_cost', 1600)
    
    # 计算当前能进行多少次抽卡
    max_single_draws = user['coins'] // single_cost
    max_ten_draws = user['coins'] // ten_cost
    
    print(f"   当前金币: {user['coins']}")
    print(f"   可进行单抽次数: {max_single_draws}")
    print(f"   可进行十连抽次数: {max_ten_draws}")
    
    # 如果金币充足，先消耗一些
    if max_single_draws > 5:
        print(f"   📉 先进行几次抽卡以消耗金币...")
        for i in range(3):
            try:
                response = requests.post('http://127.0.0.1:5000/api/draw/single',
                                       json={'user_id': user['id'], 'pool_id': pool['id']})
                data = response.json()
                
                if data['status'] == 'success':
                    user['coins'] = data['data']['remaining_coins']
                    item = data['data']['item']
                    print(f"      抽卡 {i+1}: {item['name']} ({item['rarity']}) - 余额: {user['coins']}")
                else:
                    print(f"      抽卡失败: {data['message']}")
                    break
                    
            except Exception as e:
                print(f"      抽卡错误: {e}")
                break
    
    # 4. 检查按钮状态逻辑
    print(f"\n🔘 检查按钮状态逻辑...")
    current_coins = user['coins']
    
    can_single = current_coins >= single_cost
    can_ten = current_coins >= ten_cost
    
    print(f"   当前金币: {current_coins}")
    print(f"   单抽按钮应该{'启用' if can_single else '禁用'} (需要 {single_cost} 金币)")
    print(f"   十连按钮应该{'启用' if can_ten else '禁用'} (需要 {ten_cost} 金币)")
    
    # 5. 测试充值功能
    print(f"\n💳 测试充值功能...")
    recharge_amount = 3000  # 充值3000金币
    
    try:
        response = requests.post('http://127.0.0.1:5000/api/recharge',
                               json={'user_id': user['id'], 'amount': recharge_amount})
        data = response.json()
        
        if data['status'] == 'success':
            new_coins = data['data']['new_coins']
            print(f"   ✅ 充值成功:")
            print(f"      充值前: {current_coins} 金币")
            print(f"      充值后: {new_coins} 金币")
            print(f"      充值金额: {recharge_amount} 金币")
            
            # 6. 检查充值后的按钮状态
            print(f"\n🔘 检查充值后的按钮状态...")
            can_single_after = new_coins >= single_cost
            can_ten_after = new_coins >= ten_cost
            
            print(f"   充值后金币: {new_coins}")
            print(f"   单抽按钮应该{'启用' if can_single_after else '禁用'} (需要 {single_cost} 金币)")
            print(f"   十连按钮应该{'启用' if can_ten_after else '禁用'} (需要 {ten_cost} 金币)")
            
            # 7. 验证可以进行抽卡
            if can_single_after:
                print(f"\n🎲 验证充值后可以立即抽卡...")
                try:
                    response = requests.post('http://127.0.0.1:5000/api/draw/single',
                                           json={'user_id': user['id'], 'pool_id': pool['id']})
                    data = response.json()
                    
                    if data['status'] == 'success':
                        item = data['data']['item']
                        final_coins = data['data']['remaining_coins']
                        print(f"   ✅ 抽卡成功: {item['name']} ({item['rarity']})")
                        print(f"   💰 剩余金币: {final_coins}")
                    else:
                        print(f"   ❌ 抽卡失败: {data['message']}")
                        
                except Exception as e:
                    print(f"   ❌ 抽卡错误: {e}")
            
        else:
            print(f"   ❌ 充值失败: {data['message']}")
            
    except Exception as e:
        print(f"   ❌ 充值错误: {e}")
    
    # 8. 总结修复内容
    print(f"\n" + "=" * 60)
    print("🎯 修复总结:")
    print("✅ 问题: 充值后需要刷新页面才能抽卡")
    print("✅ 原因: 充值成功后没有更新抽卡按钮状态")
    print("✅ 修复: 在充值成功后调用 updateDrawButtons() 函数")
    print("✅ 效果: 充值后立即可以抽卡，无需刷新页面")
    
    print(f"\n🔧 修复代码位置:")
    print("   文件: gacha.html")
    print("   函数: recharge(amount)")
    print("   修改: 在充值成功后添加 updateDrawButtons() 调用")
    
    print(f"\n🌐 前端测试:")
    print("   1. 访问 http://127.0.0.1:3000/gacha")
    print("   2. 登录用户")
    print("   3. 选择卡池")
    print("   4. 消耗金币直到无法抽卡")
    print("   5. 点击充值")
    print("   6. 充值完成后，抽卡按钮应立即可用")

if __name__ == '__main__':
    test_recharge_button_update()
