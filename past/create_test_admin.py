#!/usr/bin/env python3
"""
创建测试管理员账号
"""

import requests
import json

# 服务器配置
BACKEND_BASE_URL = 'http://127.0.0.1:5000'

def create_test_admin():
    """创建测试管理员账号"""
    print("🧪 创建测试管理员账号...")
    
    # 首先以超级管理员身份登录
    super_admin_login = {
        'account': 'fhc',
        'password': '114514'
    }
    
    try:
        # 登录超级管理员
        login_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=super_admin_login)
        login_result = login_response.json()
        
        if login_result.get('status') == 'success':
            super_admin_id = login_result['data']['id']
            print(f"✅ 超级管理员登录成功，ID: {super_admin_id}")
            
            # 创建新的管理员
            new_admin_data = {
                'super_admin_id': super_admin_id,
                'name': 'test_admin',
                'account': 'test_admin',
                'password': 'admin123456'
            }
            
            create_response = requests.post(f'{BACKEND_BASE_URL}/api/super-admin/admins', json=new_admin_data)
            create_result = create_response.json()
            
            print(f"创建管理员结果: {create_result}")
            
            if create_result.get('status') == 'success':
                print("✅ 测试管理员账号创建成功")
                
                # 验证管理员可以登录
                admin_login = {
                    'account': 'test_admin',
                    'password': 'admin123456'
                }
                
                verify_response = requests.post(f'{BACKEND_BASE_URL}/api/auth/login', json=admin_login)
                verify_result = verify_response.json()
                
                print(f"管理员登录验证: {verify_result}")
                
                if verify_result.get('status') == 'success' and verify_result['data'].get('role') == 'admin':
                    print("✅ 测试管理员账号验证成功")
                    return True
                else:
                    print("❌ 管理员账号验证失败")
            else:
                print("❌ 管理员账号创建失败")
        else:
            print("❌ 超级管理员登录失败")
            
    except Exception as e:
        print(f"❌ 创建过程中出错: {e}")
    
    return False

if __name__ == '__main__':
    if create_test_admin():
        print("\n🎉 测试管理员账号创建完成！")
        print("账号: test_admin")
        print("密码: admin123456")
    else:
        print("\n❌ 测试管理员账号创建失败")
