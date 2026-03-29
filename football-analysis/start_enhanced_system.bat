@echo off
echo ========================================
echo 增强版足球分析系统启动脚本
echo 对标市场最火AI足球分析平台
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
echo 2. 安装依赖包...
pip install -r requirements_enhanced.txt

echo.
echo 3. 启动增强版Web应用...
echo 访问: http://localhost:5001
echo.

python enhanced_web_app.py

if errorlevel 1 (
    echo.
    echo 启动失败，尝试备用方案...
    echo 启动基础版Web应用...
    python web_app/app.py
)

pause