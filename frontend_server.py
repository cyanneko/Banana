"""
静态文件服务器
用于提供前端HTML文件服务
"""

from flask import Flask, send_from_directory, render_template_string
import os

# 创建Flask应用
static_app = Flask(__name__)

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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
    
    static_app.run(host='127.0.0.1', port=3000, debug=True)
