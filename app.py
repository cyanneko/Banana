from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import random
import hashlib
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 模拟数据库 - 在实际项目中应该使用真实数据库
# 用户
users = [
    {"id": 1, "name": "fhc", "account": "fhc", "password": "114514", "coins": 500000, "qb" : 5000},
]

# 充充币转换为软妹币的比例
qb_to_rmb_rate = 0.9

# 卡池管理员
draw_admin = [
    {"id": 1, "name": "fhc", "account": "fhc", "password": "114514"},
]

# 超级管理员
super_admin = [
    {"id": 1, "name": "fhc", "account": "fhc", "password": "114514"},
    {"id": 2, "name": "test", "account": "test", "password": "123456"},
]

# 用户拥有的物品
user_own_item = [
]

# 物品数据 - weight字段表示稀有度，数值越低越稀有
items = [
    {"id": 1, "name": "能量剑", "description": "传说中能够创造世界的神器", "weight": 0.1, "rarity": "神话", "type": "武器"},
    {"id": 2, "name": "雾切之回光", "description": "神里流·霜灭", "weight": 2, "rarity": "传说", "type": "武器"},
    {"id": 3, "name": "中二手套", "description": "fhc专武", "weight": 10, "rarity": "史诗", "type": "护甲"},
    {"id": 4, "name": "护身符", "description": "这次rks一定能涨", "weight": 20, "rarity": "稀有", "type": "饰品"},
    {"id": 5, "name": "剑", "description": "常见的普通武器", "weight": 40, "rarity": "普通", "type": "武器"},
    {"id": 6, "name": "盾牌", "description": "基础的防御装备", "weight": 40, "rarity": "普通", "type": "护甲"},
    {"id": 7, "name": "治疗药水", "description": "恢复生命值的药水", "weight": 40, "rarity": "普通", "type": "消耗品"},
    {"id": 8, "name": "派蒙", "description": "应急食品！", "weight": 0.1, "rarity": "神话", "type": "同伴"},
    {"id": 9, "name": "迷迷", "description": "兄弟你好香", "weight": 0.1, "rarity": "神话", "type": "同伴"},
    {"id": 10, "name": "魔力药水", "description": "恢复魔力的药水", "weight": 40, "rarity": "普通", "type": "消耗品"},
    {"id": 11, "name": "护摩之杖", "description": "吃饱喝饱，一路走好！", "weight": 2, "rarity": "传说", "type": "武器"},
    {"id": 12, "name": "舞萌手套", "description": "awmc", "weight": 10, "rarity": "史诗", "type": "护甲"},
    {"id": 13, "name": "AK47", "description": "大人，时代变了", "weight": 20, "rarity": "稀有", "type": "武器"},
    {"id": 14, "name": "BB枪", "description": "勉强能用", "weight": 40, "rarity": "普通", "type": "武器"},
    {"id": 15, "name": "罗小黑", "description": "喵！", "weight": 0.1, "rarity": "神话", "type": "同伴"},

]

# 卡池数据
card_pools = [
    {
        "id": 1,
        "name": "标准卡池",
        "description": "包含所有基础物品的标准卡池",
        "is_active": True,
        "created_by": 1,
        "created_at": datetime.now().isoformat(),
        "single_cost": 160,  # 单抽价格
        "ten_cost": 1600    # 十连抽价格
    },
    {
        "id": 2,
        "name": "神话限定池",
        "description": "神话物品概率提升的限定卡池",
        "is_active": True,
        "created_by": 1,
        "created_at": datetime.now().isoformat(),
        "single_cost": 2000,  # 单抽价格更高
        "ten_cost": 18000     # 十连抽价格更高
    }
]

# 卡池物品关系（卡池ID -> 物品ID -> 权重）
pool_items = [
    # 标准卡池包含所有物品，使用默认权重
    {"pool_id": 1, "item_id": 1, "weight": 0.1},  # 能量剑
    {"pool_id": 1, "item_id": 2, "weight": 2},    # 雾切之回光
    {"pool_id": 1, "item_id": 3, "weight": 10},   # 中二手套
    {"pool_id": 1, "item_id": 4, "weight": 20},   # 护身符
    {"pool_id": 1, "item_id": 5, "weight": 40},   # 剑
    {"pool_id": 1, "item_id": 6, "weight": 40},   # 盾牌
    {"pool_id": 1, "item_id": 7, "weight": 40},   # 治疗药水
    {"pool_id": 1, "item_id": 8, "weight": 0.1},  # 派蒙
    {"pool_id": 1, "item_id": 9, "weight": 0.1},  # 迷迷
    {"pool_id": 1, "item_id": 10, "weight": 40},  # 魔力药水
    {"pool_id": 1, "item_id": 11, "weight": 2},   # 护摩之杖
    {"pool_id": 1, "item_id": 12, "weight": 10},  # 舞萌手套
    {"pool_id": 1, "item_id": 13, "weight": 20},  # AK47
    {"pool_id": 1, "item_id": 14, "weight": 40},  # BB枪
    {"pool_id": 1, "item_id": 15, "weight": 0.1}, # 罗小黑
    
    # 神话限定池只包含神话和传说物品，权重调整
    {"pool_id": 2, "item_id": 1, "weight": 1},    # 能量剑（权重提升）
    {"pool_id": 2, "item_id": 2, "weight": 5},    # 雾切之回光（权重提升）
    {"pool_id": 2, "item_id": 8, "weight": 1},    # 派蒙（权重提升）
    {"pool_id": 2, "item_id": 9, "weight": 1},    # 迷迷（权重提升）
    {"pool_id": 2, "item_id": 11, "weight": 5},   # 护摩之杖（权重提升）
    {"pool_id": 2, "item_id": 15, "weight": 1},   # 罗小黑（权重提升）
    {"pool_id": 2, "item_id": 3, "weight": 15},   # 中二手套（填充物品）
    {"pool_id": 2, "item_id": 12, "weight": 15},  # 舞萌手套（填充物品）
]

# 抽卡记录
draw_history = []

# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "后端服务运行正常"
    })

# 首页
@app.route('/', methods=['GET'])
def home():
    """首页端点"""
    return jsonify({
        "message": "欢迎使用抽卡系统API",
        "version": "2.0.0",
        "description": "多货币体系抽卡系统：抽抽币(coins)用于抽卡，充充币(qb)用于兑换抽抽币",
        "currencies": {
            "coins": "抽抽币 - 用于抽卡消耗",
            "qb": "充充币 - 用于兑换抽抽币",
            "rmb": "软妹币 - 虚拟的真实货币，用于充值充充币"
        },
        "endpoints": {
            "auth": "/api/auth",
            "users": "/api/users", 
            "items": "/api/items",
            "draw": "/api/draw",
            "inventory": "/api/inventory",
            "recharge": "/api/recharge (qb兑换coins)",
            "qb_recharge": "/api/qb/recharge (rmb充值qb)",
            "qb_withdraw": "/api/qb/withdraw (qb提现rmb)",
            "qb_balance": "/api/qb/balance/<user_id>",
            "health": "/health"
        }
    })

# 辅助函数
def hash_password(password):
    """密码哈希"""
    return hashlib.md5(password.encode()).hexdigest()

def get_user_by_account(account):
    """根据账号获取用户"""
    return next((u for u in users if u["account"] == account), None)

def get_item_by_id(item_id):
    """根据ID获取物品"""
    return next((i for i in items if i["id"] == item_id), None)

def get_user_items(user_id):
    """获取用户拥有的物品"""
    user_items = []
    for own_item in user_own_item:
        if own_item["userid"] == user_id:
            item = get_item_by_id(own_item["itemid"])
            if item:
                user_items.append({
                    "item": item,
                    "number": own_item["number"]
                })
    return user_items

def add_item_to_user(user_id, item_id, number=1):
    """给用户添加物品"""
    # 检查用户是否已经拥有该物品
    for own_item in user_own_item:
        if own_item["userid"] == user_id and own_item["itemid"] == item_id:
            own_item["number"] += number
            return
    
    # 如果没有，则新增记录
    user_own_item.append({
        "userid": user_id,
        "itemid": item_id,
        "number": number
    })

def weighted_random_choice(items_list):
    """基于权重的随机选择"""
    total_weight = sum(item["weight"] for item in items_list)
    random_num = random.uniform(0, total_weight)
    
    current_weight = 0
    for item in items_list:
        current_weight += item["weight"]
        if random_num <= current_weight:
            return item
    
    # 如果没有选中任何物品，返回最后一个
    return items_list[-1]

def get_user_by_id(user_id):
    """根据ID获取用户"""
    return next((u for u in users if u["id"] == user_id), None)

def update_user_coins(user_id, amount):
    """更新用户货币（amount可以是正数或负数）"""
    user = get_user_by_id(user_id)
    if user:
        user["coins"] += amount
        return True
    return False

def check_user_coins(user_id, required_amount):
    """检查用户货币是否足够"""
    user = get_user_by_id(user_id)
    return user and user["coins"] >= required_amount

def update_user_qb(user_id, amount):
    """更新用户充充币（amount可以是正数或负数）"""
    user = get_user_by_id(user_id)
    if user:
        user["qb"] += amount
        return True
    return False

def check_user_qb(user_id, required_amount):
    """检查用户充充币是否足够"""
    user = get_user_by_id(user_id)
    return user and user["qb"] >= required_amount

def get_pool_by_id(pool_id):
    """根据ID获取卡池"""
    return next((p for p in card_pools if p["id"] == pool_id), None)

def get_pool_items(pool_id):
    """获取卡池中的所有物品及其权重"""
    pool_item_list = []
    for pool_item in pool_items:
        if pool_item["pool_id"] == pool_id:
            item = get_item_by_id(pool_item["item_id"])
            if item:
                pool_item_list.append({
                    "item": item,
                    "weight": pool_item["weight"]
                })
    return pool_item_list

def weighted_random_choice_from_pool(pool_id):
    """从指定卡池进行基于权重的随机选择"""
    pool_item_list = get_pool_items(pool_id)
    if not pool_item_list:
        return None
    
    total_weight = sum(item["weight"] for item in pool_item_list)
    random_num = random.uniform(0, total_weight)
    
    current_weight = 0
    for pool_item in pool_item_list:
        current_weight += pool_item["weight"]
        if random_num <= current_weight:
            return pool_item["item"]
    
    # 如果没有选中任何物品，返回最后一个
    return pool_item_list[-1]["item"]

def is_admin(user_id):
    """检查用户是否为管理员"""
    return any(admin["id"] == user_id for admin in draw_admin)

def is_super_admin(user_id):
    """检查用户是否为超级管理员"""
    return any(admin["id"] == user_id for admin in super_admin)

def get_admin_by_id(admin_id):
    """根据ID获取管理员"""
    return next((a for a in draw_admin if a["id"] == admin_id), None)

def get_super_admin_by_id(admin_id):
    """根据ID获取超级管理员"""
    return next((a for a in super_admin if a["id"] == admin_id), None)

def get_admin_by_account(account):
    """根据账号获取管理员"""
    return next((a for a in draw_admin if a["account"] == account), None)

def get_super_admin_by_account(account):
    """根据账号获取超级管理员"""
    return next((a for a in super_admin if a["account"] == account), None)

def add_item_to_pool(pool_id, item_id, weight=None):
    """向卡池添加物品"""
    # 检查物品是否已在卡池中
    for pool_item in pool_items:
        if pool_item["pool_id"] == pool_id and pool_item["item_id"] == item_id:
            return False  # 物品已存在
    
    # 如果未指定权重，使用物品默认权重
    if weight is None:
        item = get_item_by_id(item_id)
        weight = item["weight"] if item else 1
    
    pool_items.append({
        "pool_id": pool_id,
        "item_id": item_id,
        "weight": weight
    })
    return True

def remove_item_from_pool(pool_id, item_id):
    """从卡池移除物品"""
    global pool_items
    pool_items = [pi for pi in pool_items if not (pi["pool_id"] == pool_id and pi["item_id"] == item_id)]
    return True

def update_pool_item_weight(pool_id, item_id, new_weight):
    """更新卡池中物品的权重"""
    for pool_item in pool_items:
        if pool_item["pool_id"] == pool_id and pool_item["item_id"] == item_id:
            pool_item["weight"] = new_weight
            return True
    return False

# 用户认证相关端点
@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or 'account' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少账号或密码"
        }), 400
    
    account = data['account']
    password = data['password']
    
    # 首先检查超级管理员
    super_admin_user = get_super_admin_by_account(account)
    if super_admin_user and super_admin_user['password'] == password:
        user_info = {k: v for k, v in super_admin_user.items() if k != 'password'}
        user_info['role'] = 'super_admin'
        return jsonify({
            "status": "success",
            "message": "超级管理员登录成功",
            "data": user_info
        })
    
    # 检查管理员
    admin_user = get_admin_by_account(account)
    if admin_user and admin_user['password'] == password:
        user_info = {k: v for k, v in admin_user.items() if k != 'password'}
        user_info['role'] = 'admin'
        return jsonify({
            "status": "success",
            "message": "管理员登录成功",
            "data": user_info
        })
    
    # 检查普通用户
    user = get_user_by_account(account)
    if user and user['password'] == password:
        user_info = {k: v for k, v in user.items() if k != 'password'}
        user_info['role'] = 'user'
        return jsonify({
            "status": "success",
            "message": "用户登录成功",
            "data": user_info
        })
    
    # 账号或密码错误
    return jsonify({
        "status": "error",
        "message": "账号或密码错误"
    }, 401)

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'account' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少必要字段：name、account和password"
        }), 400
    
    # 检查账号是否已存在
    if get_user_by_account(data['account']):
        return jsonify({
            "status": "error",
            "message": "账号已存在"
        }), 400
    
    # 创建新用户
    new_id = max([u["id"] for u in users]) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data["name"],
        "account": data["account"],
        "password": data["password"],  # 实际项目中应该加密
        "coins": 2000,  # 新用户初始抽抽币
        "qb": 0      # 新用户初始充充币
    }
    
    users.append(new_user)
    
    # 给新用户一些初始物品
    add_item_to_user(new_id, 4, 1)  # 普通剑
    add_item_to_user(new_id, 6, 3)  # 治疗药水
    
    user_info = {k: v for k, v in new_user.items() if k != 'password'}
    
    return jsonify({
        "status": "success",
        "message": "注册成功",
        "data": user_info
    }), 201

# 用户相关端点
@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户（管理员功能）"""
    # 返回用户信息时不包含密码
    safe_users = [{k: v for k, v in user.items() if k != 'password'} for user in users]
    return jsonify({
        "status": "success",
        "data": safe_users,
        "count": len(safe_users)
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """根据ID获取单个用户"""
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user_info = {k: v for k, v in user.items() if k != 'password'}
        return jsonify({
            "status": "success",
            "data": user_info
        })
    else:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404

@app.route('/api/users/<int:user_id>/balance', methods=['GET'])
def get_user_balance(user_id):
    """获取用户余额（支持双货币）"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "coins_balance": user.get("coins", 0),
            "qb_balance": user.get("qb", 0),
            "qb_to_rmb_rate": qb_to_rmb_rate
        }
    })

# 物品相关端点
@app.route('/api/items', methods=['GET'])
def get_items():
    """获取所有物品"""
    return jsonify({
        "status": "success",
        "data": items,
        "count": len(items)
    })

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """根据ID获取单个物品"""
    item = get_item_by_id(item_id)
    if item:
        return jsonify({
            "status": "success",
            "data": item
        })
    else:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404

# 背包相关端点
@app.route('/api/inventory/<int:user_id>', methods=['GET'])
def get_user_inventory(user_id):
    """获取用户背包"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    user_items = get_user_items(user_id)
    
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "user_name": user["name"],
            "items": user_items,
            "total_items": len(user_items)
        }
    })

# 抽卡系统端点
@app.route('/api/draw/single', methods=['POST'])
def single_draw():
    """单次抽卡"""
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID"
        }), 400
    
    user_id = data['user_id']
    pool_id = data.get('pool_id', 1)  # 默认使用标准卡池
    
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    pool = get_pool_by_id(pool_id)
    if not pool or not pool.get('is_active', True):
        return jsonify({
            "status": "error",
            "message": "卡池不存在或已停用"
        }), 404
    
    # 检查货币是否足够
    single_draw_cost = pool.get('single_cost', 160)  # 使用卡池自定义价格，默认160
    if not check_user_coins(user_id, single_draw_cost):
        return jsonify({
            "status": "error",
            "message": f"货币不足，从{pool['name']}单次抽卡需要{single_draw_cost}货币"
        }), 400
    
    # 扣除货币
    update_user_coins(user_id, -single_draw_cost)
    
    # 从指定卡池执行抽卡
    drawn_item = weighted_random_choice_from_pool(pool_id)
    if not drawn_item:
        return jsonify({
            "status": "error",
            "message": "卡池中没有可抽取的物品"
        }), 400
    
    # 添加到用户背包
    add_item_to_user(user_id, drawn_item['id'], 1)
    
    # 记录抽卡历史
    draw_record = {
        "id": len(draw_history) + 1,
        "user_id": user_id,
        "user_name": user["name"],
        "pool_id": pool_id,
        "pool_name": pool["name"],
        "item": drawn_item,
        "draw_type": "single",
        "cost": single_draw_cost,
        "timestamp": datetime.now().isoformat()
    }
    draw_history.append(draw_record)
    
    return jsonify({
        "status": "success",
        "message": f"恭喜获得 {drawn_item['name']}！",
        "data": {
            "item": drawn_item,
            "pool": pool,
            "draw_record": draw_record,
            "remaining_coins": user["coins"]
        }
    })

@app.route('/api/draw/ten', methods=['POST'])
def ten_draw():
    """十连抽卡"""
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID"
        }), 400
    
    user_id = data['user_id']
    pool_id = data.get('pool_id', 1)  # 默认使用标准卡池
    
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    pool = get_pool_by_id(pool_id)
    if not pool or not pool.get('is_active', True):
        return jsonify({
            "status": "error",
            "message": "卡池不存在或已停用"
        }), 404
    
    # 检查货币是否足够
    ten_draw_cost = pool.get('ten_cost', 1600)  # 使用卡池自定义价格，默认1600
    if not check_user_coins(user_id, ten_draw_cost):
        return jsonify({
            "status": "error",
            "message": f"货币不足，从{pool['name']}十连抽需要{ten_draw_cost}货币"
        }), 400
    
    # 扣除货币
    update_user_coins(user_id, -ten_draw_cost)
    
    drawn_items = []
    draw_records = []
    
    # 获取卡池中的稀有物品用于保底
    pool_item_list = get_pool_items(pool_id)
    rare_pool_items = [pi for pi in pool_item_list if pi["item"]["weight"] <= 20]  # 稀有及以上
    
    # 执行10次抽卡
    for i in range(10):
        # 第10次抽卡保底机制：如果前9次都没有稀有及以上物品，第10次必出稀有
        if i == 9:
            has_rare = any(item["weight"] <= 20 for item in drawn_items)
            if not has_rare and rare_pool_items:
                # 从稀有物品中随机选择
                total_rare_weight = sum(pi["weight"] for pi in rare_pool_items)
                random_num = random.uniform(0, total_rare_weight)
                current_weight = 0
                for pool_item in rare_pool_items:
                    current_weight += pool_item["weight"]
                    if random_num <= current_weight:
                        drawn_item = pool_item["item"]
                        break
                else:
                    drawn_item = rare_pool_items[-1]["item"]
            else:
                drawn_item = weighted_random_choice_from_pool(pool_id)
        else:
            drawn_item = weighted_random_choice_from_pool(pool_id)
        
        if not drawn_item:
            return jsonify({
                "status": "error",
                "message": "卡池中没有可抽取的物品"
            }), 400
        
        drawn_items.append(drawn_item)
        
        # 添加到用户背包
        add_item_to_user(user_id, drawn_item['id'], 1)
        
        # 记录抽卡历史
        draw_record = {
            "id": len(draw_history) + 1,
            "user_id": user_id,
            "user_name": user["name"],
            "pool_id": pool_id,
            "pool_name": pool["name"],
            "item": drawn_item,
            "draw_type": "ten_draw",
            "draw_index": i + 1,
            "cost": ten_draw_cost // 10,  # 平均每次的花费
            "timestamp": datetime.now().isoformat()
        }
        draw_history.append(draw_record)
        draw_records.append(draw_record)
    
    # 统计结果
    rarity_count = {}
    for item in drawn_items:
        rarity = item["rarity"]
        rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
    
    return jsonify({
        "status": "success",
        "message": "十连抽卡完成！",
        "data": {
            "items": drawn_items,
            "pool": pool,
            "draw_records": draw_records,
            "statistics": {
                "total_items": len(drawn_items),
                "rarity_count": rarity_count
            },
            "remaining_coins": user["coins"]
        }
    })

@app.route('/api/draw/history/<int:user_id>', methods=['GET'])
def get_draw_history(user_id):
    """获取用户抽卡历史"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    user_history = [record for record in draw_history if record["user_id"] == user_id]
    user_history.sort(key=lambda x: x["timestamp"], reverse=True)  # 按时间倒序
    
    # 分页支持
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_history = user_history[start:end]
    
    return jsonify({
        "status": "success",
        "data": {
            "history": paginated_history,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(user_history),
                "has_next": end < len(user_history),
                "has_prev": page > 1
            }
        }
    })

@app.route('/api/draw/rates', methods=['GET'])
def get_draw_rates():
    """获取抽卡概率"""
    total_weight = sum(item["weight"] for item in items)
    
    # 定义稀有度排序顺序（从高稀有度到低稀有度）
    rarity_order = ["神话", "传说", "史诗", "稀有", "普通"]
    
    # 计算单个物品概率
    rates = []
    for item in items:
        probability = (item["weight"] / total_weight) * 100
        rates.append({
            "item": item,
            "probability": round(probability, 4)  # 增加精度到4位小数
        })
    
    # 按稀有度排序单个物品概率
    rates.sort(key=lambda x: (
        rarity_order.index(x["item"]["rarity"]) if x["item"]["rarity"] in rarity_order else 999,
        x["item"]["name"]  # 同稀有度内按名称排序
    ))
    
    # 按稀有度分组
    rarity_rates = {}
    for item in items:
        rarity = item["rarity"]
        if rarity not in rarity_rates:
            rarity_rates[rarity] = {"weight": 0, "items": []}
        rarity_rates[rarity]["weight"] += item["weight"]
        rarity_rates[rarity]["items"].append(item)
    
    # 计算稀有度概率并排序
    sorted_rarity_rates = {}
    for rarity in rarity_order:
        if rarity in rarity_rates:
            probability = (rarity_rates[rarity]["weight"] / total_weight) * 100
            sorted_rarity_rates[rarity] = {
                "weight": rarity_rates[rarity]["weight"],
                "items": rarity_rates[rarity]["items"],
                "probability": round(probability, 4)  # 增加精度到4位小数
            }
    
    return jsonify({
        "status": "success",
        "data": {
            "individual_rates": rates,
            "rarity_rates": sorted_rarity_rates,
            "total_weight": total_weight,
            "rarity_order": rarity_order
        }
    })

# 统计相关端点
@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """获取系统统计概览"""
    # 计算各种统计数据
    total_users = len(users)
    total_items = len(items)
    total_draws = len(draw_history)
    
    # 统计各稀有度物品数量
    rarity_stats = {}
    for item in items:
        rarity = item["rarity"]
        rarity_stats[rarity] = rarity_stats.get(rarity, 0) + 1
    
    # 统计抽卡情况
    draw_stats = {}
    for record in draw_history:
        rarity = record["item"]["rarity"]
        draw_stats[rarity] = draw_stats.get(rarity, 0) + 1
    
    return jsonify({
        "status": "success",
        "data": {
            "users": {
                "total": total_users
            },
            "items": {
                "total": total_items,
                "by_rarity": rarity_stats
            },
            "draws": {
                "total": total_draws,
                "by_rarity": draw_stats
            }
        }
    })

@app.route('/api/stats/user/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    """获取用户统计数据"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 统计用户抽卡次数
    user_draws = [record for record in draw_history if record["user_id"] == user_id]
    total_draws = len(user_draws)
    
    # 统计用户获得的物品稀有度
    draw_rarity_stats = {}
    for record in user_draws:
        rarity = record["item"]["rarity"]
        draw_rarity_stats[rarity] = draw_rarity_stats.get(rarity, 0) + 1
    
    # 统计用户背包物品
    user_items = get_user_items(user_id)
    inventory_stats = {}
    total_item_count = 0
    for user_item in user_items:
        rarity = user_item["item"]["rarity"]
        count = user_item["number"]
        inventory_stats[rarity] = inventory_stats.get(rarity, 0) + count
        total_item_count += count
    
    return jsonify({
        "status": "success",
        "data": {
            "user_info": {k: v for k, v in user.items() if k != 'password'},
            "draw_stats": {
                "total_draws": total_draws,
                "by_rarity": draw_rarity_stats
            },
            "inventory_stats": {
                "total_items": total_item_count,
                "unique_items": len(user_items),
                "by_rarity": inventory_stats
            }
        }
    })

# 充值系统端点（消耗充充币兑换抽抽币）
@app.route('/api/recharge', methods=['POST'])
def recharge():
    """使用充充币兑换抽抽币"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'package_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID或套餐ID"
        }), 400
    
    user_id = data['user_id']
    package_id = data['package_id']
    
    # 获取充值套餐信息（现在表示消耗qb获得coins）
    packages = [
        {"id": 1, "name": "基础兑换", "coins": 100, "qb_cost": 100, "bonus": 0},
        {"id": 2, "name": "小额兑换", "coins": 500, "qb_cost": 500, "bonus": 50},
        {"id": 3, "name": "标准兑换", "coins": 1000, "qb_cost": 1000, "bonus": 100},
        {"id": 4, "name": "豪华兑换", "coins": 2000, "qb_cost": 2000, "bonus": 300},
        {"id": 5, "name": "至尊兑换", "coins": 5000, "qb_cost": 5000, "bonus": 1000},
        {"id": 6, "name": "王者兑换", "coins": 10000, "qb_cost": 10000, "bonus": 2500}
    ]
    
    # 查找对应的充值套餐
    package = None
    for pkg in packages:
        if pkg["id"] == package_id:
            package = pkg
            break
    
    if not package:
        return jsonify({
            "status": "error",
            "message": f"无效的套餐ID"
        }), 400
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 检查用户充充币是否足够
    if not check_user_qb(user_id, package["qb_cost"]):
        return jsonify({
            "status": "error",
            "message": f"充充币不足，需要{package['qb_cost']}充充币，当前仅有{user['qb']}充充币"
        }), 400
    
    # 计算实际到账金额（基础金额 + 赠送金额）
    actual_coins = package["coins"] + package["bonus"]
    old_coins = user["coins"]
    old_qb = user["qb"]
    
    # 扣除充充币，增加抽抽币
    update_user_qb(user_id, -package["qb_cost"])
    update_user_coins(user_id, actual_coins)
    
    # 记录兑换历史
    recharge_record = {
        "id": len(draw_history) + 1,  # 简单的ID生成
        "user_id": user_id,
        "user_name": user["name"],
        "package_name": package["name"],
        "qb_cost": package["qb_cost"],
        "base_coins": package["coins"],
        "bonus_coins": package["bonus"],
        "total_coins": actual_coins,
        "timestamp": datetime.now().isoformat(),
        "type": "qb_to_coins_exchange"
    }
    
    bonus_text = f"+{package['bonus']}赠送" if package["bonus"] > 0 else ""
    
    return jsonify({
        "status": "success",
        "message": f"兑换成功！消耗{package['qb_cost']}充充币，获得{package['coins']}抽抽币{bonus_text}，共计{actual_coins}抽抽币",
        "data": {
            "old_coins": old_coins,
            "new_coins": user["coins"],
            "old_qb": old_qb,
            "new_qb": user["qb"],
            "package": package,
            "qb_cost": package["qb_cost"],
            "base_coins": package["coins"],
            "bonus_coins": package["bonus"],
            "total_coins": actual_coins,
            "recharge_record": recharge_record
        }
    })

@app.route('/api/recharge/packages', methods=['GET'])
def get_recharge_packages():
    """获取充充币兑换抽抽币套餐"""
    packages = [
        {"id": 1, "name": "基础兑换", "coins": 100, "qb_cost": 100, "bonus": 0, "description": "消耗100充充币，获得100抽抽币"},
        {"id": 2, "name": "小额兑换", "coins": 500, "qb_cost": 500, "bonus": 50, "description": "消耗500充充币，获得550抽抽币"},
        {"id": 3, "name": "标准兑换", "coins": 1000, "qb_cost": 1000, "bonus": 100, "description": "消耗1000充充币，获得1100抽抽币"},
        {"id": 4, "name": "豪华兑换", "coins": 2000, "qb_cost": 2000, "bonus": 300, "description": "消耗2000充充币，获得2300抽抽币"},
        {"id": 5, "name": "至尊兑换", "coins": 5000, "qb_cost": 5000, "bonus": 1000, "description": "消耗5000充充币，获得6000抽抽币"},
        {"id": 6, "name": "王者兑换", "coins": 10000, "qb_cost": 10000, "bonus": 2500, "description": "消耗10000充充币，获得12500抽抽币"}
    ]
    
    return jsonify({
        "status": "success",
        "data": packages
    })

# 卡池管理相关端点
@app.route('/api/pools', methods=['GET'])
def get_pools():
    """获取所有卡池"""
    active_pools = [pool for pool in card_pools if pool.get('is_active', True)]
    return jsonify({
        "status": "success",
        "data": active_pools,
        "count": len(active_pools)
    })

@app.route('/api/pools/<int:pool_id>', methods=['GET'])
def get_pool(pool_id):
    """根据ID获取单个卡池详情"""
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    # 获取卡池中的物品
    pool_item_list = get_pool_items(pool_id)
    
    return jsonify({
        "status": "success",
        "data": {
            "pool": pool,
            "items": pool_item_list,
            "total_items": len(pool_item_list)
        }
    })

@app.route('/api/pools', methods=['POST'])
def create_pool():
    """创建新卡池（管理员功能）"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少卡池名称"
        }), 400
    
    # 检查管理员权限（简化版本，实际应该通过token验证）
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以创建卡池"
        }), 403
    
    # 创建新卡池
    new_pool_id = max([p["id"] for p in card_pools]) + 1 if card_pools else 1
    new_pool = {
        "id": new_pool_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "is_active": data.get("is_active", True),
        "created_by": user_id,
        "created_at": datetime.now().isoformat(),
        "single_cost": data.get("single_cost", 160),  # 单抽价格，默认160
        "ten_cost": data.get("ten_cost", 1600)        # 十连抽价格，默认1600
    }
    
    card_pools.append(new_pool)
    
    return jsonify({
        "status": "success",
        "message": "卡池创建成功",
        "data": new_pool
    }), 201

@app.route('/api/pools/<int:pool_id>', methods=['PUT'])
def update_pool(pool_id):
    """更新卡池信息（管理员功能）"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "缺少更新数据"
        }), 400
    
    # 检查管理员权限
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以更新卡池"
        }), 403
    
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    # 更新卡池信息
    if 'name' in data:
        pool['name'] = data['name']
    if 'description' in data:
        pool['description'] = data['description']
    if 'is_active' in data:
        pool['is_active'] = data['is_active']
    if 'single_cost' in data:
        pool['single_cost'] = max(1, data['single_cost'])  # 确保价格至少为1
    if 'ten_cost' in data:
        pool['ten_cost'] = max(1, data['ten_cost'])        # 确保价格至少为1
    
    return jsonify({
        "status": "success",
        "message": "卡池更新成功",
        "data": pool
    })

@app.route('/api/pools/<int:pool_id>', methods=['DELETE'])
def delete_pool(pool_id):
    """删除卡池（管理员功能）"""
    data = request.get_json() or {}
    
    # 检查管理员权限
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以删除卡池"
        }), 403
    
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    # 删除卡池
    global card_pools, pool_items
    card_pools = [p for p in card_pools if p["id"] != pool_id]
    pool_items = [pi for pi in pool_items if pi["pool_id"] != pool_id]
    
    return jsonify({
        "status": "success",
        "message": "卡池删除成功"
    })

@app.route('/api/pools/<int:pool_id>/items', methods=['POST'])
def add_pool_item(pool_id):
    """向卡池添加物品（管理员功能）"""
    data = request.get_json()
    
    if not data or 'item_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少物品ID"
        }), 400
    
    # 检查管理员权限
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以管理卡池物品"
        }), 403
    
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    item_id = data['item_id']
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404
    
    weight = data.get('weight', item['weight'])  # 使用指定权重或物品默认权重
    
    if not add_item_to_pool(pool_id, item_id, weight):
        return jsonify({
            "status": "error",
            "message": "物品已存在于该卡池中"
        }), 400
    
    return jsonify({
        "status": "success",
        "message": f"物品 {item['name']} 已添加到卡池 {pool['name']}",
        "data": {
            "pool_id": pool_id,
            "item_id": item_id,
            "weight": weight
        }
    })

@app.route('/api/pools/<int:pool_id>/items/<int:item_id>', methods=['PUT'])
def update_pool_item(pool_id, item_id):
    """更新卡池中物品的权重（管理员功能）"""
    data = request.get_json()
    
    if not data or 'weight' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少权重参数"
        }), 400
    
    # 检查管理员权限
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以管理卡池物品"
        }), 403
    
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404
    
    new_weight = data['weight']
    if new_weight <= 0:
        return jsonify({
            "status": "error",
            "message": "权重必须大于0"
        }), 400
    
    if not update_pool_item_weight(pool_id, item_id, new_weight):
        return jsonify({
            "status": "error",
            "message": "物品不在该卡池中"
        }), 404
    
    return jsonify({
        "status": "success",
        "message": f"物品 {item['name']} 在卡池 {pool['name']} 中的权重已更新为 {new_weight}",
        "data": {
            "pool_id": pool_id,
            "item_id": item_id,
            "weight": new_weight
        }
    })

@app.route('/api/pools/<int:pool_id>/items/<int:item_id>', methods=['DELETE'])
def remove_pool_item(pool_id, item_id):
    """从卡池移除物品（管理员功能）"""
    data = request.get_json() or {}
    
    # 检查管理员权限
    user_id = data.get('admin_id')
    if not user_id or not is_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有管理员可以管理卡池物品"
        }), 403
    
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404
    
    remove_item_from_pool(pool_id, item_id)
    
    return jsonify({
        "status": "success",
        "message": f"物品 {item['name']} 已从卡池 {pool['name']} 中移除"
    })

@app.route('/api/pools/<int:pool_id>/rates', methods=['GET'])
def get_pool_rates(pool_id):
    """获取指定卡池的抽卡概率"""
    pool = get_pool_by_id(pool_id)
    if not pool:
        return jsonify({
            "status": "error",
            "message": "卡池不存在"
        }), 404
    
    pool_item_list = get_pool_items(pool_id)
    if not pool_item_list:
        return jsonify({
            "status": "error",
            "message": "卡池中没有物品"
        }), 400
    
    total_weight = sum(item["weight"] for item in pool_item_list)
    
    # 定义稀有度排序顺序
    rarity_order = ["神话", "传说", "史诗", "稀有", "普通"]
    
    # 计算单个物品概率
    rates = []
    for pool_item in pool_item_list:
        probability = (pool_item["weight"] / total_weight) * 100
        rates.append({
            "item": pool_item["item"],
            "weight": pool_item["weight"],
            "probability": round(probability, 4)
        })
    
    # 按稀有度排序
    rates.sort(key=lambda x: (
        rarity_order.index(x["item"]["rarity"]) if x["item"]["rarity"] in rarity_order else 999,
        x["item"]["name"]
    ))
    
    # 按稀有度分组统计
    rarity_rates = {}
    for pool_item in pool_item_list:
        rarity = pool_item["item"]["rarity"]
        if rarity not in rarity_rates:
            rarity_rates[rarity] = {"weight": 0, "items": []}
        rarity_rates[rarity]["weight"] += pool_item["weight"]
        rarity_rates[rarity]["items"].append(pool_item["item"])
    
    # 计算稀有度概率并排序
    sorted_rarity_rates = {}
    for rarity in rarity_order:
        if rarity in rarity_rates:
            probability = (rarity_rates[rarity]["weight"] / total_weight) * 100
            sorted_rarity_rates[rarity] = {
                "weight": rarity_rates[rarity]["weight"],
                "items": rarity_rates[rarity]["items"],
                "probability": round(probability, 4)
            }
    
    return jsonify({
        "status": "success",
        "data": {
            "pool": pool,
            "individual_rates": rates,
            "rarity_rates": sorted_rarity_rates,
            "total_weight": total_weight,
            "rarity_order": rarity_order
        }
    })

# 超级管理员相关端点
@app.route('/api/super-admin/admins', methods=['GET'])
def get_admins():
    """获取所有管理员（超级管理员功能）"""
    # 检查超级管理员权限
    user_id = request.args.get('super_admin_id', type=int)
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以查看管理员列表"
        }), 403
    
    # 返回管理员信息时不包含密码
    safe_admins = [{k: v for k, v in admin.items() if k != 'password'} for admin in draw_admin]
    
    return jsonify({
        "status": "success",
        "data": safe_admins,
        "count": len(safe_admins)
    })

@app.route('/api/super-admin/admins', methods=['POST'])
def create_admin():
    """创建新管理员（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'account' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少必要字段：name、account和password"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以创建管理员"
        }), 403
    
    # 检查账号是否已存在
    if get_admin_by_account(data['account']) or get_user_by_account(data['account']) or get_super_admin_by_account(data['account']):
        return jsonify({
            "status": "error",
            "message": "账号已存在"
        }), 400
    
    # 创建新管理员
    new_id = max([a["id"] for a in draw_admin]) + 1 if draw_admin else 1
    new_admin = {
        "id": new_id,
        "name": data["name"],
        "account": data["account"],
        "password": data["password"]
    }
    
    draw_admin.append(new_admin)
    
    admin_info = {k: v for k, v in new_admin.items() if k != 'password'}
    
    return jsonify({
        "status": "success",
        "message": "管理员创建成功",
        "data": admin_info
    }), 201

@app.route('/api/super-admin/admins/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    """删除管理员（超级管理员功能）"""
    data = request.get_json() or {}
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以删除管理员"
        }), 403
    
    admin = get_admin_by_id(admin_id)
    if not admin:
        return jsonify({
            "status": "error",
            "message": "管理员不存在"
        }), 404
    
    # 删除管理员
    global draw_admin
    draw_admin = [a for a in draw_admin if a["id"] != admin_id]
    
    return jsonify({
        "status": "success",
        "message": f"管理员 {admin['name']} 删除成功"
    })

@app.route('/api/super-admin/super-admins', methods=['GET'])
def get_super_admins():
    """获取所有超级管理员（超级管理员功能）"""
    # 检查超级管理员权限
    user_id = request.args.get('super_admin_id', type=int)
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以查看超级管理员列表"
        }), 403
    
    # 返回超级管理员信息时不包含密码
    safe_super_admins = [{k: v for k, v in admin.items() if k != 'password'} for admin in super_admin]
    
    return jsonify({
        "status": "success",
        "data": safe_super_admins,
        "count": len(safe_super_admins)
    })

@app.route('/api/super-admin/super-admins', methods=['POST'])
def create_super_admin():
    """创建新超级管理员（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'account' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少必要字段：name、account和password"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以创建超级管理员"
        }), 403
    
    # 检查账号是否已存在
    if get_super_admin_by_account(data['account']) or get_admin_by_account(data['account']) or get_user_by_account(data['account']):
        return jsonify({
            "status": "error",
            "message": "账号已存在"
        }), 400
    
    # 创建新超级管理员
    new_id = max([a["id"] for a in super_admin]) + 1 if super_admin else 1
    new_super_admin = {
        "id": new_id,
        "name": data["name"],
        "account": data["account"],
        "password": data["password"]
    }
    
    super_admin.append(new_super_admin)
    
    admin_info = {k: v for k, v in new_super_admin.items() if k != 'password'}
    
    return jsonify({
        "status": "success",
        "message": "超级管理员创建成功",
        "data": admin_info
    }), 201

@app.route('/api/super-admin/super-admins/<int:admin_id>', methods=['DELETE'])
def delete_super_admin(admin_id):
    """删除超级管理员（超级管理员功能）"""
    global super_admin
    data = request.get_json() or {}
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以删除超级管理员"
        }), 403
    
    # 不能删除自己
    if user_id == admin_id:
        return jsonify({
            "status": "error",
            "message": "不能删除自己"
        }), 400
    
    admin = get_super_admin_by_id(admin_id)
    if not admin:
        return jsonify({
            "status": "error",
            "message": "超级管理员不存在"
        }), 404
    
    # 确保至少保留一个超级管理员
    if len(super_admin) <= 1:
        return jsonify({
            "status": "error",
            "message": "至少需要保留一个超级管理员"
        }), 400
    
    # 删除超级管理员
    super_admin = [a for a in super_admin if a["id"] != admin_id]
    
    return jsonify({
        "status": "success",
        "message": f"超级管理员 {admin['name']} 删除成功"
    })

@app.route('/api/super-admin/users', methods=['POST'])
def create_user():
    """创建新用户（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'account' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少必要字段：name、account和password"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以创建用户"
        }), 403
    
    # 检查账号是否已存在
    if get_user_by_account(data['account']) or get_admin_by_account(data['account']) or get_super_admin_by_account(data['account']):
        return jsonify({
            "status": "error",
            "message": "账号已存在"
        }), 400
    
    # 创建新用户
    new_id = max([u["id"] for u in users]) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data["name"],
        "account": data["account"],
        "password": data["password"],
        "coins": data.get("coins", 2000),  # 默认初始抽抽币
        "qb": data.get("qb", 0.0)  # 默认初始充充币
    }
    
    users.append(new_user)
    
    user_info = {k: v for k, v in new_user.items() if k != 'password'}
    
    return jsonify({
        "status": "success",
        "message": "用户创建成功",
        "data": user_info
    }), 201

@app.route('/api/super-admin/users/<int:target_user_id>', methods=['DELETE'])
def delete_user(target_user_id):
    """删除用户（超级管理员功能）"""
    data = request.get_json() or {}
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以删除用户"
        }), 403
    
    user = get_user_by_id(target_user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 删除用户及其相关数据
    global users, user_own_item, draw_history
    users = [u for u in users if u["id"] != target_user_id]
    user_own_item = [item for item in user_own_item if item["userid"] != target_user_id]
    # 保留抽卡历史记录，但标记用户已删除
    
    return jsonify({
        "status": "success",
        "message": f"用户 {user['name']} 删除成功"
    })

@app.route('/api/super-admin/users/<int:target_user_id>/coins', methods=['PUT'])
def update_user_coins_admin(target_user_id):
    """修改用户货币（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'coins' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少货币数量参数"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以修改用户货币"
        }), 403
    
    user = get_user_by_id(target_user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    new_coins = data['coins']
    if new_coins < 0:
        return jsonify({
            "status": "error",
            "message": "货币数量不能为负数"
        }), 400
    
    old_coins = user["coins"]
    user["coins"] = new_coins
    
    return jsonify({
        "status": "success",
        "message": f"用户 {user['name']} 的货币已从 {old_coins} 修改为 {new_coins}",
        "data": {
            "user_id": target_user_id,
            "old_coins": old_coins,
            "new_coins": new_coins
        }
    })

@app.route('/api/super-admin/users/<int:target_user_id>/qb', methods=['PUT'])
def update_user_qb_admin(target_user_id):
    """修改用户充充币（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'qb' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少充充币数量参数"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以修改用户充充币"
        }), 403
    
    user = get_user_by_id(target_user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    new_qb = float(data['qb'])
    if new_qb < 0:
        return jsonify({
            "status": "error",
            "message": "充充币数量不能为负数"
        }), 400
    
    old_qb = user.get("qb", 0)
    user["qb"] = new_qb
    
    return jsonify({
        "status": "success",
        "message": f"用户 {user['name']} 的充充币已从 {old_qb} 修改为 {new_qb}",
        "data": {
            "user_id": target_user_id,
            "old_qb": old_qb,
            "new_qb": new_qb
        }
    })

@app.route('/api/super-admin/items', methods=['POST'])
def create_item():
    """创建新物品（超级管理员功能）"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少物品名称"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以创建物品"
        }), 403
    
    # 检查物品名称是否已存在
    if any(item["name"] == data["name"] for item in items):
        return jsonify({
            "status": "error",
            "message": "物品名称已存在"
        }), 400
    
    # 创建新物品
    new_id = max([i["id"] for i in items]) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "weight": data.get("weight", 40),  # 默认权重
        "rarity": data.get("rarity", "普通"),  # 默认稀有度
        "type": data.get("type", "其他")  # 默认类型
    }
    
    items.append(new_item)
    
    return jsonify({
        "status": "success",
        "message": "物品创建成功",
        "data": new_item
    }), 201

@app.route('/api/super-admin/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """修改物品（超级管理员功能）"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "缺少更新数据"
        }), 400
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以修改物品"
        }), 403
    
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404
    
    # 如果要修改名称，检查是否与其他物品重名
    if 'name' in data and data['name'] != item['name']:
        if any(i["name"] == data["name"] for i in items if i["id"] != item_id):
            return jsonify({
                "status": "error",
                "message": "物品名称已存在"
            }), 400
    
    # 更新物品信息
    if 'name' in data:
        item['name'] = data['name']
    if 'description' in data:
        item['description'] = data['description']
    if 'weight' in data:
        item['weight'] = max(0.1, data['weight'])  # 确保权重至少为0.1
    if 'rarity' in data:
        item['rarity'] = data['rarity']
    if 'type' in data:
        item['type'] = data['type']
    
    return jsonify({
        "status": "success",
        "message": "物品更新成功",
        "data": item
    })

@app.route('/api/super-admin/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """删除物品（超级管理员功能）"""
    data = request.get_json() or {}
    
    # 检查超级管理员权限
    user_id = data.get('super_admin_id')
    if not user_id or not is_super_admin(user_id):
        return jsonify({
            "status": "error",
            "message": "权限不足，只有超级管理员可以删除物品"
        }), 403
    
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({
            "status": "error",
            "message": "物品不存在"
        }), 404
    
    # 删除物品及其相关数据
    global items, pool_items, user_own_item
    items = [i for i in items if i["id"] != item_id]
    pool_items = [pi for pi in pool_items if pi["item_id"] != item_id]
    user_own_item = [ui for ui in user_own_item if ui["itemid"] != item_id]
    
    return jsonify({
        "status": "success",
        "message": f"物品 {item['name']} 删除成功"
    })

# 充充币管理端点
@app.route('/api/qb/recharge', methods=['POST'])
def qb_recharge():
    """使用软妹币充值充充币（1:1兑换）"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'rmb_amount' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID或充值金额"
        }), 400
    
    user_id = data['user_id']
    rmb_amount = data['rmb_amount']
    
    # 验证充值金额
    if not isinstance(rmb_amount, (int, float)) or rmb_amount <= 0:
        return jsonify({
            "status": "error",
            "message": "充值金额必须为正数"
        }), 400
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 1:1兑换，软妹币换充充币（假设用户有无限rmb）
    qb_amount = rmb_amount
    old_qb = user["qb"]
    
    # 增加充充币
   
    update_user_qb(user_id, qb_amount)
    
    # 记录充值历史
    recharge_record = {
        "id": len(draw_history) + 1,
        "user_id": user_id,
        "user_name": user["name"],
               "rmb_amount": rmb_amount,
        "qb_amount": qb_amount,
        "timestamp": datetime.now().isoformat(),
        "type": "rmb_to_qb_recharge"
    }
    
    return jsonify({
        "status": "success",
        "message": f"充值成功！消耗{rmb_amount}软妹币，获得{qb_amount}充充币",
        "data": {
            "old_qb": old_qb,
            "new_qb": user["qb"],
            "rmb_amount": rmb_amount,
            "qb_amount": qb_amount,
            "recharge_record": recharge_record
        }
    })

@app.route('/api/qb/withdraw', methods=['POST'])
def qb_withdraw():
    """充充币兑换软妹币（按比例兑换）"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'qb_amount' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID或提现金额"
        }), 400
    
    user_id = data['user_id']
    qb_amount = data['qb_amount']
    
    # 验证提现金额
    if not isinstance(qb_amount, (int, float)) or qb_amount <= 0:
        return jsonify({
            "status": "error",
            "message": "提现金额必须为正数"
        }), 400
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 检查充充币是否足够
    if not check_user_qb(user_id, qb_amount):
        return jsonify({
            "status": "error",
            "message": f"充充币不足，需要{qb_amount}充充币，当前仅有{user['qb']}充充币"
        }), 400
    
    # 按比例兑换为软妹币
    rmb_amount = qb_amount * qb_to_rmb_rate
    old_qb = user["qb"]
    
    # 扣除充充币
    update_user_qb(user_id, -qb_amount)
    
    # 记录提现历史
    withdraw_record = {
        "id": len(draw_history) + 1,
        "user_id": user_id,
        "user_name": user["name"],
        "qb_amount": qb_amount,
        "rmb_amount": rmb_amount,
        "exchange_rate": qb_to_rmb_rate,
        "timestamp": datetime.now().isoformat(),
        "type": "qb_to_rmb_withdraw"
    }
    
    return jsonify({
        "status": "success",
        "message": f"提现成功！消耗{qb_amount}充充币，获得{rmb_amount:.2f}软妹币（汇率：{qb_to_rmb_rate}）",
        "data": {
            "old_qb": old_qb,
            "new_qb": user["qb"],
            "qb_amount": qb_amount,
            "rmb_amount": rmb_amount,
            "exchange_rate": qb_to_rmb_rate,
            "withdraw_record": withdraw_record
        }
    })

@app.route('/api/qb/balance/<int:user_id>', methods=['GET'])
def get_qb_balance(user_id):
    """获取用户充充币余额"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "user_name": user["name"],
            "qb_balance": user["qb"],
            "coins_balance": user["coins"],
            "qb_to_rmb_rate": qb_to_rmb_rate
        }
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        "status": "error",
        "message": "接口不存在"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        "status": "error",
        "message": "服务器内部错误"
    }), 500

if __name__ == '__main__':
    # 从环境变量获取配置，或使用默认值
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🎲 启动抽卡系统后端服务...")
    print(f"📡 地址: http://{host}:{port}")
    print(f"🔧 调试模式: {debug}")
    print(f"📚 API文档:")
    print(f"   - 健康检查: GET /health")
    print(f"   - 用户认证: POST /api/auth/login, /api/auth/register")
    print(f"   - 用户管理: GET /api/users")
    print(f"   - 物品管理: GET /api/items")
    print(f"   - 卡池管理: GET /api/pools, POST /api/pools, PUT /api/pools/<id>, DELETE /api/pools/<id>")
    print(f"   - 卡池物品: POST /api/pools/<id>/items, PUT /api/pools/<id>/items/<item_id>, DELETE /api/pools/<id>/items/<item_id>")
    print(f"   - 卡池概率: GET /api/pools/<id>/rates")
    print(f"   - 背包查看: GET /api/inventory/<user_id>")
    print(f"   - 单次抽卡: POST /api/draw/single (支持pool_id参数)")
    print(f"   - 十连抽卡: POST /api/draw/ten (支持pool_id参数)")
    print(f"   - 抽卡历史: GET /api/draw/history/<user_id>")
    print(f"   - 抽卡概率: GET /api/draw/rates (默认标准卡池)")
    print(f"   - 统计数据: GET /api/stats/overview, /api/stats/user/<user_id>")
    print(f"   - 充值相关: POST /api/recharge, GET /api/recharge/packages")
    print(f"   - 卡池管理: GET/POST/PUT/DELETE /api/pools")
    print(f"   - 卡池物品管理: POST/PUT/DELETE /api/pools/<pool_id>/items")
    print(f"   - 卡池抽卡概率: GET /api/pools/<pool_id>/rates")
    print(f"   - 超级管理员管理: GET/POST/DELETE /api/super-admin/admins")
    print(f"   - 超级管理员查看: GET /api/super-admin/super-admins")
    print(f"   - 超级管理员创建: POST /api/super-admin/super-admins")
    print(f"   - 超级管理员删除: DELETE /api/super-admin/super-admins/<admin_id>")
    print(f"   - 用户创建: POST /api/super-admin/users")
    print(f"   - 用户删除: DELETE /api/super-admin/users/<user_id>")
    print(f"   - 用户货币修改: PUT /api/super-admin/users/<user_id>/coins")
    print(f"   - 用户库存修改: PUT /api/super-admin/users/<user_id>/inventory")
    print(f"   - 物品创建: POST /api/super-admin/items")
    print(f"   - 物品修改: PUT /api/super-admin/items/<item_id>")
    print(f"   - 物品删除: DELETE /api/super-admin/items/<item_id>")
    
    app.run(host=host, port=port, debug=debug)
