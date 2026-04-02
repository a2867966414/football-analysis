@echo off
echo ========================================
echo 终极专业足球分析系统启动脚本
echo 使用FastAPI + WebSocket + 现代前端技术
echo 对标GitHub Copilot级别专业界面
echo ========================================
echo.

echo 1. 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 2. 安装必要依赖...
pip install fastapi uvicorn jinja2 pydantic requests

echo.
echo 3. 创建必要目录...
mkdir web_app\templates 2>nul
mkdir web_app\static 2>nul

echo.
echo 4. 启动终极专业系统...
echo 访问: http://localhost:8000
echo 登录信息: admin/admin123 或 user/user123
echo.

python ultimate_pro_system.py

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
    exit /b 1
)

pause