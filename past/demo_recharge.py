#!/usr/bin/env python3
"""
充值系统功能演示
展示不同充值套餐和赠送金额
"""

import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

def demonstrate_recharge_system():
    """演示充值系统功能"""
    print("🎮 抽卡系统充值功能演示")
    print("=" * 50)
    
    # 获取充值套餐
    print("\n📦 可用充值套餐:")
    try:
        response = requests.get(f"{BASE_URL}/api/recharge/packages")
        if response.status_code == 200:
            packages = response.json()["data"]
            
            print(f"{'套餐名称':<12} {'基础货币':<8} {'赠送货币':<8} {'总计':<8} {'价格':<6}")
            print("-" * 50)
            
            for pkg in packages:
                total = pkg['coins'] + pkg['bonus']
                bonus_display = f"+{pkg['bonus']}" if pkg['bonus'] > 0 else "无"
                print(f"{pkg['name']:<12} {pkg['coins']:<8} {bonus_display:<8} {total:<8} {pkg['price']:<6}")
        else:
            print("❌ 获取套餐失败")
            return
    except Exception as e:
        print(f"❌ 获取套餐失败: {e}")
        return
    
    print("\n💡 充值说明:")
    print("• 新用户注册即可获得2000初始货币")
    print("• 单次抽卡消耗160货币")
    print("• 十连抽卡消耗1600货币（保底稀有以上）")
    print("• 充值套餐包含不同额度的赠送货币")
    print("• 赠送货币会自动添加到您的账户余额")
    
    print("\n🎯 性价比分析:")
    try:
        response = requests.get(f"{BASE_URL}/api/recharge/packages")
        if response.status_code == 200:
            packages = response.json()["data"]
            
            print(f"{'套餐名称':<12} {'可抽单次':<8} {'可抽十连':<8} {'赠送比例':<10}")
            print("-" * 50)
            
            for pkg in packages:
                total_coins = pkg['coins'] + pkg['bonus']
                single_draws = total_coins // 160
                ten_draws = total_coins // 1600
                bonus_rate = f"{(pkg['bonus'] / pkg['coins'] * 100):.1f}%" if pkg['coins'] > 0 else "0%"
                
                print(f"{pkg['name']:<12} {single_draws:<8} {ten_draws:<8} {bonus_rate:<10}")
    except Exception as e:
        print(f"❌ 分析失败: {e}")
    
    print("\n🚀 快速开始:")
    print("1. 在前端页面注册账号")
    print("2. 点击货币旁边的充值按钮")
    print("3. 选择合适的充值套餐")
    print("4. 确认充值，赠送货币将自动到账")
    print("5. 开始您的抽卡之旅！")
    
    print("\n🎁 特别提醒:")
    print("• 豪华充值以上套餐享有更高的赠送比例")
    print("• 充值金额越大，赠送比例越优惠")
    print("• 所有赠送货币都会立即到账，无需等待")
    
    print("\n" + "=" * 50)
    print("充值系统功能演示完成！")

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            demonstrate_recharge_system()
        else:
            print("❌ 后端服务器无响应，请先启动服务器")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://127.0.0.1:5000 运行")
    except Exception as e:
        print(f"❌ 演示异常: {e}")
