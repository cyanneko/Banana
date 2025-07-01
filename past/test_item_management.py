#!/usr/bin/env python3
"""
测试超级管理员物品管理功能
"""
import requests
import json

API_BASE_URL = 'http://127.0.0.1:5000'

def test_item_management():
    """测试物品管理功能"""
    print("=== 测试超级管理员物品管理功能 ===")
    
    try:
        # 1. 获取现有物品列表
        print("\n1. 获取物品列表...")
        response = requests.get(f"{API_BASE_URL}/api/items")
        if response.status_code == 200:
            items_data = response.json()
            if items_data['status'] == 'success' and items_data['data']:
                print(f"当前物品数量: {len(items_data['data'])}")
                for item in items_data['data'][:3]:  # 只显示前3个
                    print(f"  - ID: {item['id']}, 名称: {item['name']}, 权重: {item['weight']}")
                
                # 选择第一个物品进行测试修改
                if items_data['data']:
                    test_item_id = items_data['data'][0]['id']
                    print(f"\n准备测试修改物品ID: {test_item_id}")
                    
                    # 2. 测试没有权限的修改（应该失败）
                    print("\n2. 测试无权限修改...")
                    unauthorized_data = {
                        "super_admin_id": 999,  # 不存在的超级管理员
                        "name": "测试修改物品",
                        "description": "测试描述",
                        "weight": 50.0,
                        "rarity": "稀有",
                        "type": "测试"
                    }
                    
                    unauthorized_response = requests.put(
                        f"{API_BASE_URL}/api/super-admin/items/{test_item_id}",
                        json=unauthorized_data
                    )
                    print(f"无权限修改响应: {unauthorized_response.status_code}")
                    if unauthorized_response.status_code == 403:
                        print("✅ 权限验证正常！")
                    else:
                        print(f"❌ 权限验证异常: {unauthorized_response.text}")
                    
                    # 3. 测试创建超级管理员（用于测试有权限的操作）
                    print("\n3. 尝试创建测试超级管理员...")
                    create_admin_data = {
                        "name": "测试物品管理员",
                        "account": "test_item_admin",
                        "password": "test123456"
                    }
                    
                    admin_response = requests.post(f"{API_BASE_URL}/api/auth/register", json=create_admin_data)
                    if admin_response.status_code == 200:
                        admin_data = admin_response.json()
                        admin_id = admin_data['data']['id']
                        
                        # 设置为超级管理员
                        set_admin_response = requests.put(f"{API_BASE_URL}/api/debug/set-super-admin/{admin_id}")
                        if set_admin_response.status_code == 200:
                            print(f"✅ 测试超级管理员创建成功，ID: {admin_id}")
                            
                            # 4. 测试有权限的物品修改
                            print("\n4. 测试有权限的物品修改...")
                            authorized_data = {
                                "super_admin_id": admin_id,
                                "name": f"修改后的物品_{test_item_id}",
                                "description": "这是通过超级管理员界面修改的物品",
                                "weight": 99.5,
                                "rarity": "传说",
                                "type": "管理员测试"
                            }
                            
                            authorized_response = requests.put(
                                f"{API_BASE_URL}/api/super-admin/items/{test_item_id}",
                                json=authorized_data
                            )
                            print(f"有权限修改响应: {authorized_response.status_code}")
                            if authorized_response.status_code == 200:
                                result = authorized_response.json()
                                print(f"✅ 物品修改成功: {result}")
                                
                                # 验证修改是否生效
                                verify_response = requests.get(f"{API_BASE_URL}/api/items")
                                if verify_response.status_code == 200:
                                    verify_data = verify_response.json()
                                    modified_item = next((item for item in verify_data['data'] if item['id'] == test_item_id), None)
                                    if modified_item:
                                        print(f"✅ 验证修改结果: 名称={modified_item['name']}, 权重={modified_item['weight']}")
                                    else:
                                        print("❌ 找不到修改后的物品")
                            else:
                                print(f"❌ 有权限修改失败: {authorized_response.text}")
                        else:
                            print("❌ 设置超级管理员权限失败")
                    else:
                        print("❌ 创建测试管理员失败")
                
            else:
                print("❌ 没有找到物品数据")
        else:
            print(f"❌ 获取物品列表失败: {response.status_code}")
            
        print("\n=== 物品管理功能测试完成 ===")
        print("前端物品管理功能包括：")
        print("- 物品列表显示和刷新")
        print("- 创建新物品")
        print("- 编辑物品信息（名称、描述、权重、稀有度、类型）")
        print("- 删除物品")
        print("- 超级管理员权限验证")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_item_management()
