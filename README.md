# 🎲 抽卡系统 (Gacha System)

一个功能完整(?)的基于Web的抽卡游戏系统，包含多重权限管理、双货币系统、多卡池管理、虚拟充值和完整的后台管理功能。

## ✨ 功能特性

### 🎯 核心游戏功能

- ✅ **多卡池抽卡系统**: 支持单次抽卡 & 十连抽卡，多个独立卡池
- ✅ **保底机制**: 十连抽第10个保底稀有物品
- ✅ **稀有度系统**: 神话(红)、传说(金)、史诗(紫)、稀有(蓝)、普通(灰)
- ✅ **权重概率**: 基于物品权重的随机抽取算法，支持卡池独立权重配置
- ✅ **抽卡动画**: 不同稀有度的专属动画效果（视频播放）
- ✅ **背包系统**: 查看拥有的所有物品，支持物品统计
- ✅ **抽卡记录**: 完整的历史记录追踪

### 💰 双货币经济系统

- ✅ **抽抽币系统**: 游戏内主要货币，用于抽卡消费
- ✅ **充充币系统**: 中间货币，可兑换抽抽币或提现
- ✅ **灵活定价**: 不同卡池支持自定义单抽/十连价格
- ✅ **虚拟充值**: 6种充值套餐，包含赠送奖励
- ✅ **汇率系统**: 充充币与软妹币的动态汇率转换
- ✅ **余额管理**: 实时双货币余额显示和扣费

### 👤 多权限用户系统

- ✅ **用户注册/登录**: 完整的账号密码认证系统
- ✅ **三级权限**: 普通用户、管理员、超级管理员
- ✅ **用户数据**: ID、用户名、双货币余额、物品库存
- ✅ **统计系统**: 个人和全局的抽卡统计分析

### 🎨 现代化前端界面

- ✅ **响应式设计**: 完美适配桌面和移动设备
- ✅ **现代UI**: 渐变背景、毛玻璃效果、流畅动画
- ✅ **抽卡特效**: 不同稀有度的发光特效和动画
- ✅ **多页面系统**: 背包、历史、概率、物品图鉴、管理面板

## 📁 项目结构

```
Banana-main/
├── app.py                    # 🎯 后端API服务器 (Flask)
├── frontend_server.py        # 🌐 前端静态文件服务器
├── start_server.py          # 🚀 服务器启动脚本
├── gacha.html               # 🎲 抽卡系统主界面
├── register.html            # 📝 用户注册页面
├── admin.html               # 🛠️ 卡池管理界面
├── super_admin.html         # 👑 超级管理员控制台
├── requirements.txt         # 📦 Python依赖包
├── media/                   # 🎬 抽卡动画视频文件
│   ├── 神话.mp4
│   ├── 传说.mp4
│   ├── 史诗.mp4
│   ├── 稀有.mp4
│   └── 普通.mp4
└── README.md               # 📖 项目说明文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

### 2. 安装依赖

使用启动脚本自动安装：
```bash
python start_server.py
```

或手动安装：
```bash
pip install -r requirements.txt
```

### 3. 启动系统

#### 方式一：使用启动脚本
```bash
python start_server.py
```

#### 方式二：手动启动
```bash
# 启动后端服务器
python app.py

# 新开终端，启动前端服务器
python frontend_server.py
```

### 4. 访问系统

- **🏠 首页导航**: http://127.0.0.1:3000/
- **🎲 抽卡系统**: http://127.0.0.1:3000/gacha
- **📝 用户注册**: http://127.0.0.1:3000/register  
- **�️ 管理员界面**: http://127.0.0.1:3000/admin-login
- **👑 超级管理员控制台**: http://127.0.0.1:3000/super-admin
- **🔧 后端API**: http://127.0.0.1:5000/

### 5. 管理界面说明

#### �️ 管理员界面
- **访问方式**: http://127.0.0.1:3000/admin-login
- **默认账号**: fhc / 114514
- **主要功能**: 
  - 卡池管理 (增删改查)
  - 物品权重调整
  - 自定义价格设置
  - 系统统计查看

#### 👑 超级管理员控制台
- **访问方式**: http://127.0.0.1:3000/super-admin
- **默认账号**: fhc / 114514
- **主要功能**:
  - 📊 系统统计总览
  - 👥 管理员管理 (增删)
  - 👑 超级管理员管理 (增删)  
  - 👤 用户管理 (增删改)
  - 💰 用户货币管理 (抽抽币/充充币)
  - 🎁 物品管理 (增删改)
  - 📦 用户库存管理

## 👤 默认账号配置

**超级管理员账号:**
- 🔑 账号: `fhc`
- 🔐 密码: `114514`
- 💰 初始货币: 500000抽抽币 + 5000充充币
- 🎖️ 权限: 超级管理员（具有所有权限）

**权限说明:**
- **超级管理员**: 可以管理管理员、用户、物品，修改用户数据
- **管理员**: 可以管理卡池、物品权重、查看统计
- **普通用户**: 可以抽卡、充值、查看背包

## 🎮 游戏玩法

### 登录/注册

1. 打开抽卡系统界面  
2. 使用现有账号登录或注册新账号
3. 新用户自动获得初始货币

### 多卡池抽卡系统

- **标准卡池**: 单抽160币，十连1600币，包含所有基础物品
- **神话限定池**: 单抽2000币，十连18000币，神话物品概率提升
- **十连保底**: 第10个物品保底稀有或以上
- **抽卡动画**: 不同稀有度播放专属视频动画

### 稀有度系统

- 💘 **神话** (红色): 极低概率，最珍贵物品
- 🟡 **传说** (金色): 低概率，非常稀有
- 🟣 **史诗** (紫色): 中等概率
- 🔵 **稀有** (蓝色): 较高概率  
- ⚪ **普通** (灰色): 高概率

### 双货币系统

- **抽抽币**: 用于抽卡的主要货币
- **充充币**: 中间货币，可兑换抽抽币(1:1)或提现软妹币(0.9:1)
- **汇率转换**: 充充币→软妹币 按0.9汇率转换

### 充值系统

6种充值套餐可选：

- 💰 新手礼包: 100币 (¥1)
- 💰 小额充值: 500币+50赠送 (¥5)
- 💰 标准充值: 1000币+100赠送 (¥10)
- 💰 豪华充值: 2000币+300赠送 (¥20) **推荐**
- 💰 至尊充值: 5000币+1000赠送 (¥50)
- 💰 王者充值: 10000币+2500赠送 (¥100)
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
- `GET /api/users/<user_id>/balance` - 获取用户双货币余额

### 🎁 物品系统

- `GET /api/items` - 获取所有物品
- `GET /api/items/<item_id>` - 获取指定物品
- `GET /api/inventory/<user_id>` - 获取用户背包

### 🎲 抽卡系统

- `POST /api/draw/single` - 单次抽卡 (需要pool_id参数)
- `POST /api/draw/ten` - 十连抽卡 (需要pool_id参数)
- `GET /api/draw/history/<user_id>` - 抽卡历史
- `GET /api/draw/rates` - 抽卡概率
- `GET /api/pools` - 获取所有卡池
- `GET /api/pools/<pool_id>` - 获取指定卡池详情

### 💰 双货币系统

- `POST /api/recharge` - 虚拟充值 (充充币→抽抽币)
- `GET /api/recharge/packages` - 获取充值套餐
- `POST /api/qb-recharge` - 软妹币充值充充币
- `POST /api/qb-withdraw` - 充充币提现软妹币

### 📊 统计数据

- `GET /api/stats/overview` - 系统统计概览
- `GET /api/stats/user/<user_id>` - 用户统计数据
- `GET /health` - 健康检查

### 🛠️ 管理员 API

- `POST /api/admin/login` - 管理员登录
- `GET /api/admin/pools` - 获取卡池列表
- `POST /api/admin/pools` - 创建新卡池
- `PUT /api/admin/pools/<pool_id>` - 更新卡池
- `DELETE /api/admin/pools/<pool_id>` - 删除卡池
- `POST /api/admin/pools/<pool_id>/items` - 添加物品到卡池
- `DELETE /api/admin/pools/<pool_id>/items/<item_id>` - 从卡池移除物品
- `PUT /api/admin/pools/<pool_id>/items/<item_id>/weight` - 更新物品权重

### 👑 超级管理员 API

#### 管理员管理
- `GET /api/super-admin/admins` - 获取所有管理员
- `POST /api/super-admin/admins` - 创建新管理员
- `DELETE /api/super-admin/admins/<admin_id>` - 删除管理员

#### 超级管理员管理
- `GET /api/super-admin/super-admins` - 获取所有超级管理员
- `POST /api/super-admin/super-admins` - 创建新超级管理员
- `DELETE /api/super-admin/super-admins/<admin_id>` - 删除超级管理员

#### 用户管理
- `POST /api/super-admin/users` - 创建新用户
- `DELETE /api/super-admin/users/<user_id>` - 删除用户
- `PUT /api/super-admin/users/<user_id>/coins` - 修改用户双货币
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

### 多卡池抽卡

#### 标准卡池单抽
```bash
curl -X POST http://127.0.0.1:5000/api/draw/single \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "pool_id": 1
  }'
```

#### 神话限定池十连
```bash
curl -X POST http://127.0.0.1:5000/api/draw/ten \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "pool_id": 2
  }'
```

### 双货币系统

#### 充充币兑换抽抽币
```bash
curl -X POST http://127.0.0.1:5000/api/recharge \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 1000
  }'
```

#### 软妹币充值充充币
```bash
curl -X POST http://127.0.0.1:5000/api/qb-recharge \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "package_id": 3
  }'
```

#### 充充币提现软妹币
```bash
curl -X POST http://127.0.0.1:5000/api/qb-withdraw \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "qb_amount": 1000
  }'
```

### 卡池管理 (管理员)

#### 获取所有卡池
```bash
curl http://127.0.0.1:5000/api/pools
```

#### 创建新卡池
```bash
curl -X POST http://127.0.0.1:5000/api/admin/pools \
  -H "Content-Type: application/json" \
  -d '{
    "admin_id": 1,
    "name": "新卡池",
    "description": "测试卡池",
    "single_cost": 200,
    "ten_cost": 1800
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
    "coins": 5000,
    "qb": 1000
  }'
```

#### 修改用户双货币
```bash
curl -X PUT http://127.0.0.1:5000/api/super-admin/users/2/coins \
  -H "Content-Type: application/json" \
  -d '{
    "super_admin_id": 1,
    "coins": 10000,
    "qb": 2000
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

## 🎨 数据结构

### 物品信息

```json
{
  "id": 1,
  "name": "能量剑",
  "description": "传说中能够创造世界的神器",
  "weight": 0.1,
  "rarity": "神话",
  "type": "武器"
}
```

### 用户数据

```json
{
  "id": 1,
  "name": "fhc",
  "account": "fhc",
  "coins": 500000,
  "qb": 5000
}
```

### 卡池数据

```json
{
  "id": 1,
  "name": "标准卡池",
  "description": "包含所有基础物品的标准卡池",
  "is_active": true,
  "created_by": 1,
  "single_cost": 160,
  "ten_cost": 1600,
  "created_at": "2025-07-03T10:30:00.000000"
}
```

### 抽卡记录

```json
{
  "id": 1,
  "user_id": 1,
  "pool_id": 1,
  "item": {
    "id": 1,
    "name": "能量剑",
    "rarity": "神话"
  },
  "draw_type": "single",
  "cost": 160,
  "timestamp": "2025-07-03T10:30:00.000000"
}
```

### 充值套餐

```json
{
  "id": 3,
  "name": "标准充值",
  "base_amount": 1000,
  "bonus_amount": 100,
  "price": 10,
  "description": "性价比之选"
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
- **内存数据库** - 快速演示 (生产环境建议使用数据库)

### 前端

- **HTML5** - 结构
- **CSS3** - 样式 (渐变、动画、毛玻璃效果)
- **JavaScript** - 交互逻辑
- **Font Awesome** - 图标库
- **多媒体** - MP4视频动画

### 架构特点

- **前后端分离** - Flask后端 + 静态前端
- **RESTful API** - 标准API设计
- **响应式设计** - 适配各种设备
- **模块化结构** - 易于维护和扩展

## 🎯 系统特色

### 🎨 视觉效果

- 渐变背景和毛玻璃效果
- 不同稀有度的发光动画和视频特效
- 响应式设计适配各种设备
- 现代化的UI组件和交互

### 🎲 游戏机制

- 多卡池系统，每个卡池独立配置
- 基于权重的概率系统
- 十连抽保底机制
- 双货币经济系统 (抽抽币+充充币)
- 完整的汇率转换系统

### 👑 权限管理

- 三级权限体系 (用户/管理员/超级管理员)
- 管理员可管理卡池和物品权重
- 超级管理员拥有所有管理权限
- 完整的用户和数据管理功能

### 🔧 开发友好

- RESTful API设计
- 完整的错误处理机制
- 清晰的代码结构和注释
- 易于扩展的模块化设计

## 🚀 扩展建议

### 📂 数据持久化
1. **🗄️ 数据库集成**: 使用 SQLite、MySQL 或 PostgreSQL 替换内存存储
2. **� Redis缓存**: 添加缓存层提升性能
3. **📝 数据备份**: 实现自动备份和恢复机制

### 🔐 安全增强
1. **🎫 JWT认证**: 添加Token认证和会话管理
2. **🔒 密码加密**: 使用bcrypt等加密算法
3. **�️ API限流**: 防止API滥用和攻击
4. **🔍 日志审计**: 完整的操作日志记录

### 🎮 游戏功能
1. **🏆 等级系统**: 用户经验值和等级机制
2. **🎖️ 成就系统**: 各种成就和奖励
3. **👥 社交功能**: 好友系统、排行榜
4. **🎁 活动系统**: 限时活动和特殊奖励

### 📊 数据分析
1. **� 用户行为**: 详细的用户行为分析
2. **💹 收入统计**: 充值和消费分析
3. **🎯 概率分析**: 抽卡概率和稀有度统计
4. **📋 报表系统**: 自动生成各类报表

### 🌐 部署和运维
1. **🐳 Docker化**: 容器化部署
2. **☁️ 云部署**: 部署到AWS、阿里云等
3. **⚖️ 负载均衡**: 支持高并发访问
4. **� 移动端**: 开发React Native或Flutter应用

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   
   ```bash
   # 修改启动端口
   python app.py  # 后端默认5000端口
   python frontend_server.py  # 前端默认3000端口
   ```

2. **依赖安装失败**
   
   ```bash
   # 确保 Python 版本 >= 3.7
   python --version
   
   # 升级 pip
   pip install --upgrade pip
   
   # 使用启动脚本自动安装
   python start_server.py
   ```

3. **CORS 错误**
   
   ```bash
   # 检查 Flask-CORS 是否正确安装
   pip install Flask-CORS
   ```

4. **货币不足**
   
   - 使用充值功能获取更多游戏币
   - 使用超级管理员功能直接修改用户货币

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 👨‍💻 作者

- 开发: 基于抽卡游戏系统开发
- 致谢: GitHub Copilot 提供开发辅助

- GitHub: [@cyanneko](https://github.com/cyanneko)
- 项目仓库: [Banana](https://github.com/cyanneko/Banana)

---

**🎊 享受抽卡的乐趣吧！** 🎊

