"""
测试管理员集成功能
验证前端服务器与后端API的管理员权限交互
"""

import requests
import json

def test_admin_login_and_pool_creation():
    """测试管理员登录并创建卡池"""
    
    # 测试后端API服务是否可用
    try:
        health_check = requests.get('http://127.0.0.1:5000/health')
        print(f"✅ 后端API健康检查: {health_check.status_code}")
    except Exception as e:
        print(f"❌ 后端API不可用: {e}")
        return
    
    # 测试前端服务器是否可用
    try:
        frontend_check = requests.get('http://127.0.0.1:3000/')
        print(f"✅ 前端服务器检查: {frontend_check.status_code}")
    except Exception as e:
        print(f"❌ 前端服务器不可用: {e}")
        return
    
    # 测试管理员登录API
    try:
        login_data = {
            'account': 'fhc',
            'password': '114514'
        }
        login_response = requests.post('http://127.0.0.1:5000/api/auth/login', json=login_data)
        print(f"✅ 管理员登录测试: {login_response.status_code}")
        
        if login_response.status_code == 200:
            user_data = login_response.json()
            print(f"   用户信息: {user_data}")
            user_id = user_data.get('data', {}).get('id')
            print(f"   用户ID: {user_id}")
        else:
            print(f"   登录失败: {login_response.text}")
            return
            
    except Exception as e:
        print(f"❌ 管理员登录失败: {e}")
        return
    
    # 测试创建卡池API
    try:
        pool_data = {
            'name': '测试卡池',
            'description': '这是一个测试卡池',
            'single_cost': 180,
            'ten_cost': 1700,
            'is_active': True,
            'admin_id': user_id  # 使用正确的数字ID
        }
        
        create_pool_response = requests.post('http://127.0.0.1:5000/api/pools', json=pool_data)
        print(f"✅ 创建卡池测试: {create_pool_response.status_code}")
        
        if create_pool_response.status_code == 201:
            pool_result = create_pool_response.json()
            print(f"   创建成功: {pool_result.get('message')}")
            pool_id = pool_result.get('data', {}).get('id')
            print(f"   新卡池ID: {pool_id}")
            
            # 清理测试数据 - 删除创建的测试卡池
            if pool_id:
                delete_response = requests.delete(f'http://127.0.0.1:5000/api/pools/{pool_id}', 
                                                json={'admin_id': user_id})
                print(f"   清理测试卡池: {delete_response.status_code}")
                
        else:
            error_data = create_pool_response.json()
            print(f"   创建失败: {error_data.get('message')}")
            
    except Exception as e:
        print(f"❌ 创建卡池失败: {e}")
        return
    
    print("\n🎉 管理员集成测试完成！")

if __name__ == '__main__':
    print("🔧 开始管理员集成测试...")
    test_admin_login_and_pool_creation()
