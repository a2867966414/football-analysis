@echo off
echo ========================================
echo 企业级足球分析系统启动脚本
echo 一体化专业商务型平台
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
pip install flask flask-socketio

echo.
echo 3. 创建必要目录...
mkdir web_app\templates 2>nul
mkdir web_app\static 2>nul

echo.
echo 4. 启动企业级系统...
echo 访问: http://localhost:9000
echo 公司: Football Intelligence Inc.
echo 版本: 3.0.0-enterprise
echo.
echo 登录信息:
echo   • 管理员: admin / enterprise123
echo   • 分析师: analyst / enterprise123  
echo   • 查看者: viewer / enterprise123
echo.
echo 系统特点:
echo   • 一体化专业商务平台
echo   • 企业级数据安全
echo   • 实时团队协作
echo   • 投资组合管理
echo   • 专业分析报告
echo.

python enterprise_football_system_complete.py

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
    exit /b 1
)

pause