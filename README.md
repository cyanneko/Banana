# 🎲 抽卡系统 (Gacha System)

一个完整的基于Web的抽卡游戏系统，包含货币系统、虚拟充值、物品管理和用户系统。

## ✨ 功能特性

### 🎯 核心游戏功能
- ✅ **抽卡系统**: 单次抽卡 & 十连抽卡
- ✅ **保底机制**: 十连抽第10个保底稀有物品
- ✅ **稀有度系统**: 传说(金)、史诗(紫)、稀有(蓝)、普通(灰)
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
- **🏠 首页导航**: http://127.0.0.1:3000/
- **🔧 后端API**: http://127.0.0.1:5000/

### 6. 测试系统

```bash
# 测试抽卡API
python test_gacha_api.py

# 测试货币系统
python test_currency_system.py
```

## 🎮 游戏玩法

### 登录/注册
1. 打开抽卡系统界面
2. 使用现有账号登录或注册新账号
3. 新用户自动获得2000初始货币

### 抽卡系统
- **单次抽卡**: 花费160货币，获得1个随机物品
- **十连抽卡**: 花费1600货币，获得10个物品 + 第10个保底稀有
- **稀有度概率**:
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

- GitHub: [@cyanneko](https://github.com/cyanneko)
- 项目仓库: [Banana](https://github.com/cyanneko/Banana)

---

**🎊 享受抽卡的乐趣吧！** 🎊
