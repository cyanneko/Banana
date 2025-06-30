# Python 基本后端 API

这是一个使用 Flask 框架构建的基本 Python 后端 API 服务。

## 功能特性

### 后端特性
- ✅ RESTful API 设计
- ✅ 用户管理 (CRUD操作)
- ✅ 待办事项管理 (CRUD操作)
- ✅ 跨域支持 (CORS)
- ✅ 错误处理
- ✅ 健康检查端点
- ✅ 环境变量配置

### 前端特性
- ✅ 现代化响应式设计
- ✅ 桌面版完整功能界面
- ✅ 移动端优化界面
- ✅ 实时数据同步
- ✅ 直观的用户交互
- ✅ API状态监控
- ✅ 统计数据可视化

## 项目结构

```
banana3/
├── app.py              # 后端API服务器
├── frontend_server.py  # 前端静态文件服务器
├── requirements.txt    # Python依赖包
├── .env               # 环境变量配置
├── start_server.py    # 服务器启动脚本
├── test_api.py        # API测试脚本
├── frontend.html       # 桌面版前端界面
├── mobile.html         # 移动版前端界面
├── demo.html          # API演示页面
└── README.md          # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务器

**方法一：直接运行**
```bash
python app.py
```

**方法二：使用启动脚本**
```bash
python start_server.py
```

### 3. 启动前端服务器

```bash
python frontend_server.py
```

### 4. 访问应用

- **前端首页**: http://127.0.0.1:3000/
- **桌面版界面**: http://127.0.0.1:3000/desktop
- **移动版界面**: http://127.0.0.1:3000/mobile
- **API演示**: http://127.0.0.1:3000/demo
- **后端API**: http://127.0.0.1:5000/

### 5. 测试API

```bash
python test_api.py
```

## API 端点

### 基础端点

- `GET /` - 首页，显示API信息
- `GET /health` - 健康检查

### 用户管理

- `GET /api/users` - 获取所有用户
- `GET /api/users/<id>` - 获取指定用户
- `POST /api/users` - 创建新用户
- `PUT /api/users/<id>` - 更新用户信息
- `DELETE /api/users/<id>` - 删除用户

### 待办事项管理

- `GET /api/todos` - 获取所有待办事项
- `GET /api/todos?user_id=<id>` - 获取指定用户的待办事项
- `POST /api/todos` - 创建新待办事项
- `PUT /api/todos/<id>` - 更新待办事项
- `DELETE /api/todos/<id>` - 删除待办事项

## API 使用示例

### 创建用户

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25
  }'
```

### 获取所有用户

```bash
curl http://127.0.0.1:5000/api/users
```

### 创建待办事项

```bash
curl -X POST http://127.0.0.1:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "学习Python",
    "user_id": 1,
    "completed": false
  }'
```

### 获取待办事项

```bash
curl http://127.0.0.1:5000/api/todos
```

## 配置

在 `.env` 文件中可以配置以下参数：

- `HOST` - 服务器地址 (默认: 127.0.0.1)
- `PORT` - 服务器端口 (默认: 5000)
- `DEBUG` - 调试模式 (默认: True)

## 数据格式

### 用户数据结构

```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

### 待办事项数据结构

```json
{
  "id": 1,
  "title": "学习Python",
  "completed": false,
  "user_id": 1
}
```

### 响应格式

```json
{
  "status": "success",
  "message": "操作成功",
  "data": { ... },
  "count": 1
}
```

## 扩展建议

1. **数据库集成**: 替换内存存储，使用 SQLite、MySQL 或 PostgreSQL
2. **身份验证**: 添加 JWT 或 Session 认证
3. **数据验证**: 使用 marshmallow 或 pydantic 进行数据验证
4. **日志记录**: 添加详细的日志记录
5. **API文档**: 使用 Flask-RESTX 或 Swagger 生成 API 文档
6. **测试**: 添加单元测试和集成测试
7. **部署**: 使用 gunicorn + nginx 部署到生产环境

## 故障排除

1. **端口被占用**: 修改 `.env` 文件中的 `PORT` 值
2. **依赖安装失败**: 确保 Python 版本 >= 3.7
3. **CORS 错误**: 检查 Flask-CORS 是否正确安装

## 许可证

MIT License
