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
users = [
    {"id": 1, "name": "fhc", "account": "fhc", "password": "114514", "coins": 500000},
]

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
        "endpoints": {
            "auth": "/api/auth",
            "users": "/api/users",
            "items": "/api/items",
            "draw": "/api/draw",
            "inventory": "/api/inventory",
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
    
    user = get_user_by_account(data['account'])
    if not user or user['password'] != data['password']:
        return jsonify({
            "status": "error",
            "message": "账号或密码错误"
        }), 401
    
    # 返回用户信息（不包含密码）
    user_info = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        "status": "success",
        "message": "登录成功",
        "data": user_info
    })

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
        "coins": 2000  # 新用户初始货币
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
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 检查货币是否足够
    single_draw_cost = 160
    if not check_user_coins(user_id, single_draw_cost):
        return jsonify({
            "status": "error",
            "message": f"货币不足，单次抽卡需要{single_draw_cost}货币"
        }), 400
    
    # 扣除货币
    update_user_coins(user_id, -single_draw_cost)
    
    # 执行抽卡
    drawn_item = weighted_random_choice(items)
    
    # 添加到用户背包
    add_item_to_user(user_id, drawn_item['id'], 1)
    
    # 记录抽卡历史
    draw_record = {
        "id": len(draw_history) + 1,
        "user_id": user_id,
        "user_name": user["name"],
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
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 检查货币是否足够
    ten_draw_cost = 1600
    if not check_user_coins(user_id, ten_draw_cost):
        return jsonify({
            "status": "error",
            "message": f"货币不足，十连抽需要{ten_draw_cost}货币"
        }), 400
    
    # 扣除货币
    update_user_coins(user_id, -ten_draw_cost)
    
    drawn_items = []
    draw_records = []
    
    # 执行10次抽卡
    for i in range(10):
        # 第10次抽卡保底机制：如果前9次都没有稀有及以上物品，第10次必出稀有
        if i == 9:
            rare_items = [item for item in items if item["weight"] <= 20]  # 稀有及以上 (包含神话、传说、史诗、稀有)
            has_rare = any(item["weight"] <= 20 for item in drawn_items)
            if not has_rare and rare_items:
                drawn_item = weighted_random_choice(rare_items)
            else:
                drawn_item = weighted_random_choice(items)
        else:
            drawn_item = weighted_random_choice(items)
        
        drawn_items.append(drawn_item)
        
        # 添加到用户背包
        add_item_to_user(user_id, drawn_item['id'], 1)
        
        # 记录抽卡历史
        draw_record = {
            "id": len(draw_history) + 1,
            "user_id": user_id,
            "user_name": user["name"],
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

# 充值系统端点
@app.route('/api/recharge', methods=['POST'])
def recharge():
    """虚拟充值"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'amount' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少用户ID或充值金额"
        }), 400
    
    user_id = data['user_id']
    amount = data['amount']
    
    # 获取充值套餐信息
    packages = [
        {"id": 1, "name": "新手礼包", "coins": 100, "price": "¥1", "bonus": 0},
        {"id": 2, "name": "小额充值", "coins": 500, "price": "¥5", "bonus": 50},
        {"id": 3, "name": "标准充值", "coins": 1000, "price": "¥10", "bonus": 100},
        {"id": 4, "name": "豪华充值", "coins": 2000, "price": "¥20", "bonus": 300},
        {"id": 5, "name": "至尊充值", "coins": 5000, "price": "¥50", "bonus": 1000},
        {"id": 6, "name": "王者充值", "coins": 10000, "price": "¥100", "bonus": 2500}
    ]
    
    # 查找对应的充值套餐
    package = None
    for pkg in packages:
        if pkg["coins"] == amount:
            package = pkg
            break
    
    if not package:
        return jsonify({
            "status": "error",
            "message": f"无效的充值金额，请选择有效的充值套餐"
        }), 400
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "用户不存在"
        }), 404
    
    # 计算实际到账金额（基础金额 + 赠送金额）
    actual_amount = amount + package["bonus"]
    old_coins = user["coins"]
    
    # 更新用户货币
    update_user_coins(user_id, actual_amount)
    
    # 记录充值历史（在实际项目中应该保存到数据库）
    recharge_record = {
        "id": len(draw_history) + 1,  # 简单的ID生成
        "user_id": user_id,
        "user_name": user["name"],
        "package_name": package["name"],
        "base_amount": amount,
        "bonus_amount": package["bonus"],
        "total_amount": actual_amount,
        "timestamp": datetime.now().isoformat(),
        "type": "recharge"
    }
    
    bonus_text = f"+{package['bonus']}赠送" if package["bonus"] > 0 else ""
    
    return jsonify({
        "status": "success",
        "message": f"充值成功！获得{amount}货币{bonus_text}，共计{actual_amount}货币",
        "data": {
            "old_coins": old_coins,
            "new_coins": user["coins"],
            "package": package,
            "base_amount": amount,
            "bonus_amount": package["bonus"],
            "total_amount": actual_amount,
            "recharge_record": recharge_record
        }
    })

@app.route('/api/recharge/packages', methods=['GET'])
def get_recharge_packages():
    """获取充值套餐"""
    packages = [
        {"id": 1, "name": "新手礼包", "coins": 100, "price": "¥1", "bonus": 0},
        {"id": 2, "name": "小额充值", "coins": 500, "price": "¥5", "bonus": 50},
        {"id": 3, "name": "标准充值", "coins": 1000, "price": "¥10", "bonus": 100},
        {"id": 4, "name": "豪华充值", "coins": 2000, "price": "¥20", "bonus": 300},
        {"id": 5, "name": "至尊充值", "coins": 5000, "price": "¥50", "bonus": 1000},
        {"id": 6, "name": "王者充值", "coins": 10000, "price": "¥100", "bonus": 2500}
    ]
    
    return jsonify({
        "status": "success",
        "data": packages
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
    print(f"   - 背包查看: GET /api/inventory/<user_id>")
    print(f"   - 单次抽卡: POST /api/draw/single")
    print(f"   - 十连抽卡: POST /api/draw/ten")
    print(f"   - 抽卡历史: GET /api/draw/history/<user_id>")
    print(f"   - 抽卡概率: GET /api/draw/rates")
    print(f"   - 统计数据: GET /api/stats/overview, /api/stats/user/<user_id>")
    print(f"   - 充值相关: POST /api/recharge, GET /api/recharge/packages")
    
    app.run(host=host, port=port, debug=debug)
