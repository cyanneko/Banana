"""
抽卡系统API测试脚本
用于测试新的抽卡系统后端API
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """测试健康检查端点"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_auth():
    """测试用户认证"""
    print("🔐 测试用户认证...")
    
    # 测试登录
    print("登录测试:")
    login_data = {
        "account": "fhc",
        "password": "114514"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 测试注册
    print("注册测试:")
    register_data = {
        "name": "新用户",
        "account": f"newuser_{int(time.time())}",
        "password": "123456"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
        return response.json().get('data', {}).get('id')
    except Exception as e:
        print(f"错误: {e}")
        print()
        return None

def test_items():
    """测试物品相关API"""
    print("📦 测试物品API...")
    
    # 获取所有物品
    print("获取所有物品:")
    try:
        response = requests.get(f"{BASE_URL}/api/items")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_draw_rates():
    """测试抽卡概率"""
    print("🎲 测试抽卡概率...")
    try:
        response = requests.get(f"{BASE_URL}/api/draw/rates")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_single_draw(user_id):
    """测试单次抽卡"""
    print("🎯 测试单次抽卡...")
    draw_data = {
        "user_id": user_id
    }
    try:
        response = requests.post(f"{BASE_URL}/api/draw/single", json=draw_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_ten_draw(user_id):
    """测试十连抽卡"""
    print("🎰 测试十连抽卡...")
    draw_data = {
        "user_id": user_id
    }
    try:
        response = requests.post(f"{BASE_URL}/api/draw/ten", json=draw_data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        if result.get('status') == 'success':
            print(f"消息: {result.get('message')}")
            data = result.get('data', {})
            items = data.get('items', [])
            statistics = data.get('statistics', {})
            
            print("抽到的物品:")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item['name']} ({item['rarity']})")
            
            print(f"统计: {json.dumps(statistics, ensure_ascii=False, indent=2)}")
        else:
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_inventory(user_id):
    """测试背包查看"""
    print("🎒 测试背包查看...")
    try:
        response = requests.get(f"{BASE_URL}/api/inventory/{user_id}")
        print(f"状态码: {response.status_code}")
        result = response.json()
        if result.get('status') == 'success':
            data = result.get('data', {})
            print(f"用户: {data.get('user_name')}")
            print(f"物品总数: {data.get('total_items')}")
            print("背包物品:")
            for item_info in data.get('items', []):
                item = item_info['item']
                number = item_info['number']
                print(f"  - {item['name']} x{number} ({item['rarity']})")
        else:
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_draw_history(user_id):
    """测试抽卡历史"""
    print("📊 测试抽卡历史...")
    try:
        response = requests.get(f"{BASE_URL}/api/draw/history/{user_id}")
        print(f"状态码: {response.status_code}")
        result = response.json()
        if result.get('status') == 'success':
            data = result.get('data', {})
            history = data.get('history', [])
            pagination = data.get('pagination', {})
            
            print(f"历史记录数: {pagination.get('total', 0)}")
            print("最近的抽卡记录:")
            for record in history[:5]:  # 显示最近5条
                item = record['item']
                print(f"  - {record['timestamp'][:19]}: {item['name']} ({item['rarity']})")
        else:
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def test_stats(user_id):
    """测试统计数据"""
    print("📈 测试统计数据...")
    
    # 系统概览统计
    print("系统概览统计:")
    try:
        response = requests.get(f"{BASE_URL}/api/stats/overview")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 用户统计
    print("用户统计:")
    try:
        response = requests.get(f"{BASE_URL}/api/stats/user/{user_id}")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

def main():
    """主测试函数"""
    print("🎲 开始抽卡系统API测试...")
    print("=" * 60)
    
    # 基础测试
    test_health()
    
    # 认证测试
    new_user_id = test_auth()
    
    # 物品测试
    test_items()
    
    # 抽卡概率测试
    test_draw_rates()
    
    # 使用现有用户进行抽卡测试
    test_user_id = 1  # 使用默认用户
    
    # 单次抽卡测试
    test_single_draw(test_user_id)
    
    # 十连抽卡测试
    test_ten_draw(test_user_id)
    
    # 背包查看测试
    test_inventory(test_user_id)
    
    # 抽卡历史测试
    test_draw_history(test_user_id)
    
    # 统计数据测试
    test_stats(test_user_id)
    
    print("✅ 测试完成！")

if __name__ == "__main__":
    main()
