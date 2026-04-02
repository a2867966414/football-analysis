@echo off
echo ========================================
echo 统一专业足球分析系统启动脚本
echo 对标GitHub Copilot级别专业界面
echo 整合所有功能：实时数据、AI预测、价值检测、世界杯分析
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
pip install flask flask-socketio requests

echo.
echo 3. 启动统一专业系统...
echo 访问: http://localhost:5003
echo 登录信息: admin/admin123 或 user/user123
echo.

python unified_professional_system.py

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
    exit /b 1
)

pause