"""
静态文件服务器
用于提供前端HTML文件服务，集成管理员登录和控制界面
"""

from flask import Flask, send_from_directory, render_template_string, request, jsonify, session, redirect, url_for
import os
import requests
import json
import json

# 创建Flask应用
static_app = Flask(__name__)
static_app.secret_key = 'admin_session_key_2025'  # 用于session管理

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# API基础URL
API_BASE_URL = 'http://127.0.0.1:5000'

@static_app.route('/')
def index():
    """首页 - 显示可用的前端页面"""
    index_html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>前端页面导航</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 100%;
            }
            
            h1 {
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            
            .page-list {
                display: grid;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .page-card {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                text-decoration: none;
                color: #333;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .page-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                border-color: #4facfe;
                text-decoration: none;
                color: #333;
            }
            
            .page-card h3 {
                margin-bottom: 10px;
                color: #4facfe;
                font-size: 1.3em;
            }
            
            .page-card p {
                color: #666;
                font-size: 0.95em;
                line-height: 1.5;
            }
            
            .api-info {
                background: #e3f2fd;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                text-align: left;
            }
            
            .api-info h4 {
                color: #1976d2;
                margin-bottom: 10px;
            }
            
            .api-info p {
                color: #424242;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            
            .status-badge {
                display: inline-flex;
                align-items: center;
                background: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 25px;
                font-size: 0.9em;
                margin-bottom: 20px;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                background: white;
                border-radius: 50%;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 前端页面导航</h1>
            
            <div class="status-badge">
                <span class="status-dot"></span>
                前端服务器运行中
            </div>
            
            <div class="page-list">
                <a href="/gacha" class="page-card" style="border: 3px solid #667eea;">
                    <h3>🎲 抽卡系统</h3>
                    <p>全新的抽卡游戏系统！登录账号，收集稀有物品，体验刺激的抽卡乐趣。支持单抽和十连抽，还有保底机制！</p>
                </a>
                
                <a href="/register" class="page-card">
                    <h3>📄 用户注册</h3>
                    <p>新用户注册页面，创建您的抽卡系统账号。填写用户名、账号和密码即可开始您的抽卡之旅！</p>
                </a>
                
                <a href="/admin-login" class="page-card" style="border: 3px solid #e74c3c;">
                    <h3>🔐 管理员入口</h3>
                    <p>管理员专用登录入口。管理卡池、物品权重、价格设置，查看系统统计信息和用户数据。</p>
                    <div style="margin-top: 10px; padding: 8px; background: rgba(231,76,60,0.1); border-radius: 5px; font-size: 0.85em; color: #e74c3c;">
                        🔑 需要管理员权限
                    </div>
                </a>
                
                <a href="/super-admin" class="page-card" style="border: 3px solid #ffd700; background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 100%); color: white;">
                    <h3>👑 超级管理员控制台</h3>
                    <p>超级管理员专用控制台。管理所有用户、管理员、超级管理员，修改用户数据，完全控制系统。</p>
                    <div style="margin-top: 10px; padding: 8px; background: rgba(255,255,255,0.2); border-radius: 5px; font-size: 0.85em;">
                        ⚠️ 仅限超级管理员访问 - 需要最高权限
                    </div>
                </a>
            </div>
            
            <div class="api-info">
                <h4>📡 API服务信息</h4>
                <p><strong>后端地址:</strong> http://127.0.0.1:5000</p>
                <p><strong>前端地址:</strong> http://127.0.0.1:3000</p>
                <p><strong>健康检查:</strong> http://127.0.0.1:5000/health</p>
            </div>
        </div>
        
        <script>
            // 检查后端API是否可用
            async function checkAPI() {
                try {
                    const response = await fetch('http://127.0.0.1:5000/health');
                    if (response.ok) {
                        console.log('✅ 后端API服务正常');
                    }
                } catch (error) {
                    console.warn('⚠️ 后端API服务不可用，请先启动后端服务器');
                }
            }
            
            checkAPI();
        </script>
    </body>
    </html>
    """
    return render_template_string(index_html)

@static_app.route('/register')
def register():
    """用户注册页面"""
    return send_from_directory(PROJECT_ROOT, 'register.html')

@static_app.route('/gacha')
def gacha():
    """抽卡系统页面"""
    return send_from_directory(PROJECT_ROOT, 'gacha.html')

@static_app.route('/super-admin')
def super_admin():
    """超级管理员控制台"""
    # 检查是否已登录且为超级管理员
    if 'user_id' not in session or 'role' not in session:
        return redirect('/super-admin-login')
    
    if session.get('role') != 'super_admin':
        # 返回权限不足页面
        error_html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>权限不足</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #ff7b7b 0%, #ff6b6b 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .error-container {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    width: 100%;
                }
                
                .error-icon {
                    font-size: 80px;
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }
                
                .error-title {
                    font-size: 28px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                
                .error-message {
                    font-size: 16px;
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }
                
                .user-info {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 30px;
                    border-left: 4px solid #ff6b6b;
                }
                
                .user-info p {
                    color: #555;
                    margin: 5px 0;
                }
                
                .button-group {
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                
                .btn {
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 500;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: inline-block;
                }
                
                .btn-primary {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                
                .btn-secondary {
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                }
                
                .btn-home {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                }
                
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">🚫</div>
                <h1 class="error-title">权限不足</h1>
                <p class="error-message">
                    只有超级管理员可以访问此页面。<br>
                    您当前的权限级别无法进入超级管理员控制台。
                </p>
                
                <div class="user-info">
                    <p><strong>当前用户:</strong> """ + session.get('username', '未知') + """</p>
                    <p><strong>权限级别:</strong> """ + session.get('role', '未知') + """</p>
                    <p><strong>需要权限:</strong> super_admin</p>
                </div>
                
                <div class="button-group">
                    <a href="/super-admin-login" class="btn btn-primary">超级管理员登录</a>
                    <a href="/admin" class="btn btn-secondary">管理员面板</a>
                    <a href="/" class="btn btn-home">返回首页</a>
                </div>
            </div>
        </body>
        </html>
        """
        return error_html
    
    # 权限验证通过，返回超级管理员页面
    return send_from_directory(PROJECT_ROOT, 'super_admin.html')

@static_app.route('/super-admin-login')
def super_admin_login():
    """超级管理员登录页面"""
    super_admin_login_html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>超级管理员登录</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .login-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
                text-align: center;
                border: 3px solid #ffd700;
            }
            
            .login-title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #ffd700, #ff6b6b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .login-subtitle {
                font-size: 16px;
                color: #666;
                margin-bottom: 30px;
            }
            
            .crown-icon {
                font-size: 60px;
                margin-bottom: 20px;
                display: block;
            }
            
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            
            .form-label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
            }
            
            .form-input {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                transition: border-color 0.3s ease;
                background: white;
            }
            
            .form-input:focus {
                outline: none;
                border-color: #ffd700;
            }
            
            .login-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #ffd700, #ff6b6b);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease;
                margin-bottom: 20px;
            }
            
            .login-btn:hover {
                transform: translateY(-2px);
            }
            
            .back-link {
                color: #666;
                text-decoration: none;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 8px;
                transition: background-color 0.2s ease;
            }
            
            .back-link:hover {
                background-color: #f5f5f5;
            }
            
            .error-message {
                color: #e74c3c;
                background: #ffebee;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 14px;
                display: none;
            }
            
            .success-message {
                color: #27ae60;
                background: #e8f5e8;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 14px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="crown-icon">👑</div>
            <h1 class="login-title">超级管理员登录</h1>
            <p class="login-subtitle">最高权限 · 系统管理</p>
            
            <div id="errorMessage" class="error-message"></div>
            <div id="successMessage" class="success-message"></div>
            
            <form id="superAdminLoginForm">
                <div class="form-group">
                    <label for="account" class="form-label">账号</label>
                    <input type="text" id="account" name="account" class="form-input" required>
                </div>
                
                <div class="form-group">
                    <label for="password" class="form-label">密码</label>
                    <input type="password" id="password" name="password" class="form-input" required>
                </div>
                
                <button type="submit" class="login-btn">登录进入控制台</button>
            </form>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
        
        <script>
            document.getElementById('superAdminLoginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const account = document.getElementById('account').value;
                const password = document.getElementById('password').value;
                const errorDiv = document.getElementById('errorMessage');
                const successDiv = document.getElementById('successMessage');
                
                // 隐藏之前的消息
                errorDiv.style.display = 'none';
                successDiv.style.display = 'none';
                
                try {
                    // 调用后端登录API
                    const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            account: account,
                            password: password
                        })
                    });
                    
                    // 检查响应状态
                    if (!response.ok) {
                        // 尝试解析错误响应
                        let errorData;
                        try {
                            errorData = await response.json();
                        } catch (parseError) {
                            throw new Error(`服务器响应错误 (${response.status}): ${response.statusText}`);
                        }
                        throw new Error(errorData.message || `登录请求失败 (${response.status})`);
                    }
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        const userRole = result.data.role;
                        
                        if (userRole === 'super_admin') {
                            // 超级管理员登录成功，调用前端登录接口设置session
                            const sessionResponse = await fetch('/api/super-admin-session', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    user_id: result.data.id,
                                    username: result.data.name,
                                    role: userRole
                                })
                            });
                            
                            if (sessionResponse.ok) {
                                successDiv.textContent = '超级管理员登录成功！正在跳转...';
                                successDiv.style.display = 'block';
                                
                                setTimeout(() => {
                                    window.location.href = '/super-admin';
                                }, 1500);
                            } else {
                                throw new Error('会话设置失败');
                            }
                        } else {
                            errorDiv.textContent = '权限不足：您不是超级管理员，当前权限: ' + userRole;
                            errorDiv.style.display = 'block';
                        }
                    } else {
                        errorDiv.textContent = result.message || '登录失败';
                        errorDiv.style.display = 'block';
                    }
                } catch (error) {
                    console.error('登录错误:', error);
                    
                    // 提供更详细的错误信息
                    let errorMessage = '登录过程中发生错误';
                    
                    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                        errorMessage = '无法连接到服务器，请检查后端服务是否正常运行';
                    } else if (error.message.includes('会话设置失败')) {
                        errorMessage = '登录成功但会话设置失败，请重试';
                    } else if (error.name === 'SyntaxError') {
                        errorMessage = '服务器响应格式错误，请稍后重试';
                    } else {
                        errorMessage = '登录过程中发生错误：' + error.message;
                    }
                    
                    errorDiv.textContent = errorMessage;
                    errorDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """
    return super_admin_login_html

@static_app.route('/api/super-admin-session', methods=['POST'])
def set_super_admin_session():
    """设置超级管理员会话"""
    data = request.get_json()
    if data and data.get('role') == 'super_admin':
        session['is_admin'] = True
        session['is_super_admin'] = True
        session['username'] = data.get('username')
        session['user_id'] = data.get('user_id')
        session['role'] = 'super_admin'
        return jsonify({"status": "success", "message": "超级管理员会话设置成功"})
    return jsonify({"status": "error", "message": "权限不足"}), 403

@static_app.route('/admin-login')
def admin_login():
    """管理员登录页面"""
    admin_login_html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>管理员登录</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .login-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                max-width: 400px;
                width: 100%;
            }
            
            .admin-icon {
                font-size: 4em;
                margin-bottom: 20px;
            }
            
            h1 {
                color: #333;
                margin-bottom: 30px;
                font-size: 2em;
            }
            
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 500;
            }
            
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            
            input[type="text"]:focus, input[type="password"]:focus {
                outline: none;
                border-color: #e74c3c;
            }
            
            .login-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease;
                margin-bottom: 20px;
            }
            
            .login-btn:hover {
                transform: translateY(-2px);
            }
            
            .back-link {
                color: #666;
                text-decoration: none;
                font-size: 14px;
            }
            
            .back-link:hover {
                color: #e74c3c;
            }
            
            .alert {
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
            }
            
            .alert-error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .alert-success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="admin-icon">🔐</div>
            <h1>管理员登录</h1>
            
            <div id="alert" class="alert"></div>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">管理员用户名</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="login-btn">登录</button>
            </form>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const alertDiv = document.getElementById('alert');
                
                try {
                    const response = await fetch('/admin-login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, password })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        alertDiv.textContent = '登录成功，正在跳转...';
                        alertDiv.className = 'alert alert-success';
                        alertDiv.style.display = 'block';
                        
                        setTimeout(() => {
                            window.location.href = '/admin';
                        }, 1500);
                    } else {
                        alertDiv.textContent = result.message || '登录失败';
                        alertDiv.className = 'alert alert-error';
                        alertDiv.style.display = 'block';
                    }
                } catch (error) {
                    alertDiv.textContent = '网络错误，请检查后端服务是否启动';
                    alertDiv.className = 'alert alert-error';
                    alertDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(admin_login_html)

@static_app.route('/admin-login', methods=['POST'])
def admin_login_post():
    """处理管理员登录请求"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # 向后端API验证管理员身份
        response = requests.post(f'{API_BASE_URL}/api/auth/login', json={
            'account': username,
            'password': password
        })
        
        if response.status_code == 200:
            user_data = response.json()
            if user_data.get('status') == 'success':
                user_info = user_data.get('data', {})
                # 检查是否为管理员 - 检查 draw_admin 列表
                # 根据app.py中的配置，管理员account为'fhc'，id为1
                if username == 'fhc' and user_info.get('id') == 1:
                    # 设置session
                    session['is_admin'] = True
                    session['username'] = username
                    session['user_id'] = user_info.get('id')
                    return jsonify({'success': True, 'message': '登录成功'})
                else:
                    return jsonify({'success': False, 'message': '该账号没有管理员权限'})
            else:
                return jsonify({'success': False, 'message': '用户名或密码错误'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'})

@static_app.route('/admin')
def admin_panel():
    """管理员控制面板"""
    # 检查是否已登录
    if 'user_id' not in session or 'role' not in session:
        return redirect(url_for('admin_login'))
    
    # 检查管理员权限 - 管理员和超级管理员都可以访问
    user_role = session.get('role')
    if user_role not in ['admin', 'super_admin']:
        # 返回权限不足页面
        error_html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>权限不足</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .error-container {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    width: 100%;
                }
                
                .error-icon {
                    font-size: 80px;
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                
                .error-title {
                    font-size: 28px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                
                .error-message {
                    font-size: 16px;
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }
                
                .user-info {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 30px;
                    border-left: 4px solid #e74c3c;
                }
                
                .user-info p {
                    color: #555;
                    margin: 5px 0;
                }
                
                .button-group {
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                
                .btn {
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 500;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: inline-block;
                }
                
                .btn-primary {
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                    color: white;
                }
                
                .btn-secondary {
                    background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 100%);
                    color: white;
                }
                
                .btn-home {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                }
                
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">🔐</div>
                <h1 class="error-title">权限不足</h1>
                <p class="error-message">
                    您需要管理员或超级管理员权限才能访问此页面。<br>
                    请使用管理员账号登录后再试。
                </p>
                
                <div class="user-info">
                    <p><strong>当前用户:</strong> """ + session.get('username', '未知') + """</p>
                    <p><strong>权限级别:</strong> """ + session.get('role', '未知') + """</p>
                    <p><strong>需要权限:</strong> admin 或 super_admin</p>
                </div>
                
                <div class="button-group">
                    <a href="/admin-login" class="btn btn-primary">管理员登录</a>
                    <a href="/super-admin-login" class="btn btn-secondary">超级管理员登录</a>
                    <a href="/" class="btn btn-home">返回首页</a>
                </div>
            </div>
        </body>
        </html>
        """
        return error_html
    
    return send_from_directory(PROJECT_ROOT, 'admin.html')

@static_app.route('/admin-logout')
def admin_logout():
    """管理员退出登录"""
    session.clear()
    return redirect(url_for('index'))

@static_app.route('/admin-check')
def admin_check():
    """检查管理员登录状态"""
    if session.get('is_admin'):
        return jsonify({
            'is_admin': True,
            'username': session.get('username'),
            'user_id': session.get('user_id')  # 添加用户ID
        })
    else:
        return jsonify({'is_admin': False})

@static_app.route('/api/check-super-admin-status')
def check_super_admin_status():
    """检查超级管理员登录状态"""
    if 'user_id' in session and session.get('role') == 'super_admin':
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'role': session.get('role')
        })
    else:
        return jsonify({
            'logged_in': False
        })

@static_app.route('/debug-session')
def debug_session():
    """调试session状态"""
    debug_info = {
        'session_keys': list(session.keys()),
        'session_data': dict(session),
        'user_id': session.get('user_id'),
        'role': session.get('role'),
        'username': session.get('username'),
        'is_admin': session.get('is_admin'),
        'is_super_admin': session.get('is_super_admin')
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Session调试</title></head>
    <body>
        <h1>Session调试信息</h1>
        <pre>{json.dumps(debug_info, indent=2, ensure_ascii=False)}</pre>
        <p><a href="/super-admin">访问超级管理员页面</a></p>
        <p><a href="/super-admin-login">超级管理员登录</a></p>
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    """

@static_app.route('/static/<path:filename>')
def static_files(filename):
    """静态文件服务"""
    return send_from_directory(PROJECT_ROOT, filename)

if __name__ == '__main__':
    print("🌐 启动前端服务器...")
    print("📡 地址: http://127.0.0.1:3000")
    print("📄 可用页面:")
    print("   - 首页导航: http://127.0.0.1:3000/")
    print("   - 抽卡系统: http://127.0.0.1:3000/gacha")
    print("   - 用户注册: http://127.0.0.1:3000/register")
    print("   - 管理员登录: http://127.0.0.1:3000/admin-login")
    print("   - 管理员面板: http://127.0.0.1:3000/admin")
    print("   - 超级管理员控制台: http://127.0.0.1:3000/super-admin")
    print("🔐 管理员功能:")
    print("   - 卡池管理 (增删改查)")
    print("   - 物品权重调整")
    print("   - 自定义价格设置")
    print("   - 系统统计查看")
    print("👑 超级管理员功能:")
    print("   - 管理员管理 (增删)")
    print("   - 超级管理员管理 (增删)")
    print("   - 用户管理 (增删改)")
    print("   - 用户金币/库存修改")
    print("   - 物品管理 (增删改)")
    print("   - 系统总览统计")
    print("⚠️  注意: 需要先启动后端服务器 (app.py)")
    
    static_app.run(host='127.0.0.1', port=3000, debug=True)
