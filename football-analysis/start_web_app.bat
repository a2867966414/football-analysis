@echo off
echo ========================================
echo 足球分析系统Web应用启动脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo [2/3] 安装依赖包...
pip install flask requests --quiet
if errorlevel 1 (
    echo 警告: 依赖包安装失败，尝试继续运行...
)

echo [3/3] 启动Web应用...
echo.
echo 系统正在启动，请稍候...
echo 访问地址: http://localhost:5000
echo API状态: http://localhost:5000/api/status
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

cd web_app
python app.py

pause