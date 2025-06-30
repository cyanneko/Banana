# 🎲 抽卡系统 (Gacha System)

一个完整的基于Web的抽卡游戏系统，包含货币系统、虚拟充值、物品管理和用户系统。

## ✨ 功能特性

### 🎯 核心游戏功能

- ✅ **抽卡系统**: 单次抽卡 & 十连抽卡
- ✅ **保底机制**: 十连抽第10个保底稀有物品
- ✅ **稀有度系统**: 神话(红)、传说(金)、史诗(紫)、稀有(蓝)、普通(灰)
- ✅ **权重概率**: 基于物品权重的随机抽取算法
- ✅ **背包系统**: 查看拥有的所有物品
- ✅ **抽卡记录**: 完整的历史记录追踪

### 💰 经济系统

- ✅ **货币系统**: 游戏内货币管理
- ✅ **消费机制**: 单抽160币，十连1600币
- ✅ **虚拟充值**: 6种充值套餐，包含赠送奖励
- ✅ **充值赠送**: 自动发放bonus金额到账户
- ✅ **余额管理**: 实时货币余额显示和扣费

### 👤 用户系统

- ✅ **用户注册/登录**: 账号密码认证
- ✅ **用户数据**: ID、用户名、货币、物品库存
- ✅ **统计系统**: 抽卡次数、稀有物品统计

### 🎨 前端界面

- ✅ **响应式设计**: 适配桌面和移动设备
- ✅ **现代UI**: 渐变背景、毛玻璃效果、动画
- ✅ **抽卡动效**: 稀有物品发光特效
- ✅ **多页面**: 背包、历史、概率、物品图鉴

## 📁 项目结构

```
banana3/
├── app.py                    # 🎯 后端API服务器 (Flask)
├── frontend_server.py        # 🌐 前端静态文件服务器
├── gacha.html               # 🎲 抽卡系统主界面
├── register.html            # 📝 用户注册页面
├── requirements.txt         # 📦 Python依赖包
├── .env                     # ⚙️ 环境变量配置
├── .gitignore              # 🚫 Git忽略文件
├── test_gacha_api.py       # 🧪 抽卡API测试脚本
├── test_currency_system.py # 💰 货币系统测试脚本
└── README.md               # 📖 项目说明文档
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cyanneko/Banana.git
cd Banana
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端服务器

```bash
python app.py
```

### 4. 启动前端服务器

```bash
python frontend_server.py
```

### 5. 访问游戏

- **🎲 抽卡系统**: http://127.0.0.1:3000/gacha
- **📝 用户注册**: http://127.0.0.1:3000/register  
- **🔐 管理员入口**: http://127.0.0.1:3000/admin-login
- **👑 超级管理员控制台**: http://127.0.0.1:3000/super-admin
- **🏠 首页导航**: http://127.0.0.1:3000/
- **🔧 后端API**: http://127.0.0.1:5000/

### 6. 管理界面说明

#### 🔐 管理员界面
- **访问方式**: http://127.0.0.1:3000/admin-login
- **默认账号**: fhc / 114514
- **主要功能**: 
  - 卡池管理 (增删改查)
  - 物品权重调整
  - 自定义价格设置
  - 系统统计查看
  - 抽卡概率计算

#### 👑 超级管理员控制台
- **访问方式**: http://127.0.0.1:3000/super-admin
- **默认账号**: fhc / 114514 (通过登录API验证超级管理员身份)
- **主要功能**:
  - 📊 系统统计总览
  - 👥 管理员管理 (创建/删除普通管理员)
  - 👑 超级管理员管理 (创建/删除超级管理员)
  - 👤 用户管理 (创建/删除用户账户)
  - 💰 用户金币修改
  - 📦 用户库存管理
  - 🎁 物品管理 (创建/编辑/删除物品)
  - 🔗 级联删除 (删除物品时自动清理相关数据)

### 7. 测试系统

```bash
# 测试多卡池管理功能
python test_pool_management.py

# 测试自定义价格功能
python test_custom_prices.py

# 测试功能更新 (编码、权限等)
python test_updates.py

# 测试超级管理员功能
python test_super_admin.py

# 测试超级管理员前端界面
python test_super_admin_frontend.py

# 测试登录和角色识别
python test_login.py

# 测试抽卡API
python test_gacha_api.py

# 测试货币系统
python test_currency_system.py

# 测试完整系统
python test_full_system.py
```

## 👤 默认账号配置

**超级管理员账号:**
- 🔑 账号: `fhc`
- 🔐 密码: `114514`
- 💰 初始货币: 500000
- 🎖️ 权限: 超级管理员（具有所有权限）

**权限说明:**
- **超级管理员**: 可以管理管理员、用户、物品，修改用户数据
- **管理员**: 可以管理卡池、物品权重、查看统计
- **普通用户**: 可以抽卡、充值、查看背包

**首次使用建议:**
1. 使用默认超级管理员账号登录（返回role: "super_admin"）
2. 创建新的管理员和普通用户账户进行测试
3. 访问管理员界面创建新卡池和管理物品
4. 体验完整的多权限系统功能

## 🎮 游戏玩法

### 登录/注册

1. 打开抽卡系统界面
2. 使用现有账号登录或注册新账号
3. 新用户自动获得2000初始货币

### 抽卡系统

- **单次抽卡**: 花费160货币，获得1个随机物品
- **十连抽卡**: 花费1600货币，获得10个物品 + 第10个保底稀有
- **稀有度概率**:
  - 💘 神话 (红色): 最低概率
  - 🏆 传说 (金色): 极低概率
  - 💜 史诗 (紫色): 低概率
  - 💙 稀有 (蓝色): 中等概率
  - ⚪ 普通 (灰色): 高概率

### 充值系统

6种充值套餐可选：

- 💰 新手礼包: 100币 (¥1)
- 💰 小额充值: 500币+50赠送 (¥5)
- 💰 标准充值: 1000币+100赠送 (¥10)
- 💰 豪华充值: 2000币+300赠送 (¥20) **推荐**
- 💰 至尊充值: 5000币+1000赠送 (¥50)
- 💰 王者充值: 10000币+2500赠送 (¥100)

## 📡 API 端点

### 🔐 用户认证

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

### 👤 用户管理

- `GET /api/users` - 获取所有用户
- `GET /api/users/<id>` - 获取指定用户

### 🎁 物品系统

- `GET /api/items` - 获取所有物品
- `GET /api/inventory/<user_id>` - 获取用户背包

### 🎲 抽卡系统

- `POST /api/draw/single` - 单次抽卡
- `POST /api/draw/ten` - 十连抽卡
- `GET /api/draw/history/<user_id>` - 抽卡历史
- `GET /api/draw/rates` - 抽卡概率

### 💰 充值系统

- `POST /api/recharge` - 虚拟充值
- `GET /api/recharge/packages` - 获取充值套餐

### 📊 统计数据

- `GET /api/stats/overview` - 系统统计概览
- `GET /api/stats/user/<user_id>` - 用户统计数据
- `GET /health` - 健康检查

### 🎖️ 超级管理员 API

#### 管理员管理
- `GET /api/super-admin/admins` - 获取所有管理员 (需要super_admin_id参数)
- `POST /api/super-admin/admins` - 创建新管理员
- `DELETE /api/super-admin/admins/<admin_id>` - 删除管理员

#### 超级管理员管理
- `GET /api/super-admin/super-admins` - 获取所有超级管理员 (需要super_admin_id参数)
- `POST /api/super-admin/super-admins` - 创建新超级管理员
- `DELETE /api/super-admin/super-admins/<admin_id>` - 删除超级管理员

#### 用户管理
- `POST /api/super-admin/users` - 创建新用户
- `DELETE /api/super-admin/users/<user_id>` - 删除用户
- `PUT /api/super-admin/users/<user_id>/coins` - 修改用户货币
- `PUT /api/super-admin/users/<user_id>/inventory` - 修改用户库存

#### 物品系统管理
- `POST /api/super-admin/items` - 创建新物品
- `PUT /api/super-admin/items/<item_id>` - 修改物品信息
- `DELETE /api/super-admin/items/<item_id>` - 删除物品

## 🎯 API 使用示例

### 用户登录

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "account": "fhc",
    "password": "114514"
  }'
```

### 单次抽卡

```bash
curl -X POST http://127.0.0.1:5000/api/draw/single \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

### 虚拟充值

```bash
curl -X POST http://127.0.0.1:5000/api/recharge \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 1000
  }'
```

### 查看背包

```bash
curl http://127.0.0.1:5000/api/inventory/1
```

### 超级管理员功能示例

#### 创建新管理员
```bash
curl -X POST http://127.0.0.1:5000/api/super-admin/admins \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "name": "新管理员",
    "account": "admin_user",
    "password": "admin123"
  }'
```

#### 创建新用户
```bash
curl -X POST http://127.0.0.1:5000/api/super-admin/users \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "name": "新用户",
    "account": "new_user",
    "password": "user123",
    "coins": 5000
  }'
```

#### 修改用户货币
```bash
curl -X PUT http://127.0.0.1:5000/api/super-admin/users/2/coins \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "coins": 10000
  }'
```

#### 修改用户库存
```bash
curl -X PUT http://127.0.0.1:5000/api/super-admin/users/2/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "item_id": 1,
    "quantity": 10
  }'
```

#### 创建新物品
```bash
curl -X POST http://127.0.0.1:5000/api/super-admin/items \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "name": "新物品",
    "description": "超级管理员创建的物品",
    "weight": 20,
    "rarity": "稀有",
    "type": "特殊"
  }'
```

#### 查看所有管理员
```bash
curl "http://127.0.0.1:5000/api/super-admin/admins?super_admin_id=1"
```

## 🎨 物品数据结构

### 物品信息

```json
{
  "id": 1,
  "name": "雾切之回光",
  "description": "神里流·霜灭",
  "weight": 1,
  "rarity": "传说",
  "type": "武器"
}
```

### 用户数据

```json
{
  "id": 1,
  "name": "fhc",
  "account": "fhc",
  "coins": 5000
}
```

### 抽卡记录

```json
{
  "id": 1,
  "user_id": 1,
  "item": { ... },
  "draw_type": "single",
  "cost": 160,
  "timestamp": "2025-06-30T15:19:12.676976"
}
```

## ⚙️ 配置

在 `.env` 文件中可以配置以下参数：

- `HOST` - 服务器地址 (默认: 127.0.0.1)
- `PORT` - 服务器端口 (默认: 5000)
- `DEBUG` - 调试模式 (默认: True)

## 🛠️ 技术栈

### 后端

- **Flask** - Web框架
- **Flask-CORS** - 跨域支持
- **Python 3.7+** - 编程语言

### 前端

- **HTML5** - 结构
- **CSS3** - 样式 (渐变、动画、毛玻璃效果)
- **JavaScript** - 交互逻辑
- **Font Awesome** - 图标库

### 数据存储

- **内存存储** - 用于演示 (生产环境建议使用数据库)

## 🎯 系统特色

### 🎨 视觉效果

- 渐变背景和毛玻璃效果
- 稀有物品发光动画
- 响应式设计适配各种设备
- 现代化的UI组件

### 🎲 游戏机制

- 基于权重的概率系统
- 十连抽保底机制
- 完整的经济循环
- 详细的统计数据

### 🔧 开发友好

- RESTful API设计
- 完整的测试脚本
- 详细的错误处理
- 清晰的代码结构

## 🚀 扩展建议

1. **🗄️ 数据库集成**: 使用 SQLite、MySQL 或 PostgreSQL 替换内存存储
2. **🔐 身份验证**: 添加 JWT Token 认证和会话管理
3. **📊 数据分析**: 添加更详细的用户行为分析
4. **🎮 游戏机制**: 添加更多游戏元素（等级系统、成就系统）
5. **💼 管理后台**: 创建管理员界面管理用户和物品
6. **📱 移动应用**: 开发原生移动应用
7. **🌐 部署**: 使用 Docker + K8s 部署到云平台
8. **🔄 实时功能**: 添加 WebSocket 支持实时通知

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   
   ```bash
   # 修改 .env 文件中的 PORT 值
   PORT=5001
   ```
2. **依赖安装失败**
   
   ```bash
   # 确保 Python 版本 >= 3.7
   python --version
   
   # 升级 pip
   pip install --upgrade pip
   ```
3. **CORS 错误**
   
   ```bash
   # 检查 Flask-CORS 是否正确安装
   pip install Flask-CORS
   ```
4. **货币不足**
   
   - 使用充值功能获取更多游戏币
   - 或者修改用户初始货币数量

## 📸 截图预览

抽卡系统包含以下界面：

- 🎲 主抽卡界面
- 💰 充值套餐选择
- 🎒 背包物品展示
- 📊 抽卡历史记录
- 📈 概率统计信息
- 📖 物品图鉴

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 👨‍💻 作者

- 致谢: Github Copilot

- GitHub: [@cyanneko](https://github.com/cyanneko)
- 项目仓库: [Banana](https://github.com/cyanneko/Banana)

---

**🎊 享受抽卡的乐趣吧！** 🎊

### 🛠️ 管理员系统
- ✅ **权限验证**: 基于用户ID的管理员权限校验
- ✅ **卡池管理**: 创建、编辑、删除、激活/停用卡池
- ✅ **价格设置**: 为每个卡池设置独立的单抽/十连价格
- ✅ **物品管理**: 向卡池添加/移除物品，调整权重
- ✅ **智能权重**: 添加物品时自动填充默认权重值
- ✅ **概率查看**: 实时查看各卡池的概率分布
- ✅ **统计报告**: 查看系统运行统计数据
- ✅ **管理员界面**: 专用的web管理界面(admin.html)

### 🎖️ 超级管理员系统
- ✅ **管理员管理**: 创建、删除卡池管理员账户
- ✅ **超级管理员管理**: 创建、删除超级管理员账户（至少保留一个）
- ✅ **用户管理**: 创建、删除普通用户账户
- ✅ **用户货币管理**: 直接修改用户的货币余额
- ✅ **用户库存管理**: 直接修改用户的物品库存数量
- ✅ **物品系统管理**: 创建、修改、删除游戏物品
- ✅ **权限层级**: 超级管理员 > 管理员 > 普通用户
- ✅ **安全保护**: 防止删除自己、确保至少保留一个超级管理员

