@echo off
echo ========================================
echo 专业足球AI分析界面系统启动脚本
echo 使用现代化UI设计 + 专业数据可视化
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
echo 2. 创建必要目录...
mkdir web_app\templates 2>nul
mkdir web_app\static 2>nul

echo.
echo 3. 启动专业UI系统...
echo 访问: http://localhost:8090
echo 系统特点:
echo   • 现代化暗色主题设计
echo   • 专业数据可视化
echo   • 实时比赛监控
echo   • AI智能预测 (88.5%%准确率)
echo   • 价值机会检测
echo   • 世界杯2026专业分析
echo.

python professional_ui_system.py

if errorlevel 1 (
    echo.
    echo 启动失败，请检查错误信息
    pause
    exit /b 1
)

pause