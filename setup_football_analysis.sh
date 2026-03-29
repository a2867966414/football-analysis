#!/bin/bash
echo "安装个人足球分析系统..."
echo "=========================="

# 创建项目目录
mkdir -p ~/football-analysis
cd ~/football-analysis

echo "1. 安装Python依赖..."
pip install --upgrade pip
pip install pandas numpy scikit-learn matplotlib seaborn requests jupyter notebook

echo "2. 克隆开源分析工具..."
# 克隆预测模型
git clone https://github.com/amanthedorkknight/football-predictions.git predictions

echo "3. 创建配置文件..."
cat > config.py << 'EOF'
# 足球分析系统配置
API_CONFIG = {
    'football_data': {
        'api_key': 'YOUR_API_KEY_HERE',  # 从football-data.org获取
        'base_url': 'https://api.football-data.org/v4'
    }
}

# 分析设置
ANALYSIS_CONFIG = {
    'leagues': ['PL', 'PD', 'SA', 'BL1', 'FL1'],  # 关注的联赛
    'update_interval': 3600,  # 数据更新间隔(秒)
    'prediction_model': 'logistic_regression'  # 使用的预测模型
}
EOF

echo "4. 创建数据目录结构..."
mkdir -p data/raw data/processed data/models
mkdir -p reports/visualizations reports/predictions

echo "5. 创建每日分析脚本..."
cat > daily_analysis.py << 'EOF'
#!/usr/bin/env python3
"""
每日自动分析脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pandas as pd
from football_analysis_starter import FootballAnalyzer

def main():
    print(f"开始每日分析 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 初始化分析器
    analyzer = FootballAnalyzer()
    
    # 这里可以添加您的分析逻辑
    # 例如：获取今日比赛、更新数据、生成预测等
    
    print("分析完成！")
    
    # 保存分析结果
    with open(f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.txt", 'w') as f:
        f.write(f"每日分析报告 - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("="*50 + "\n")
        f.write("分析完成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("\n提示：请配置API密钥以获取真实数据\n")

if __name__ == "__main__":
    main()
EOF

chmod +x daily_analysis.py

echo "6. 创建快速启动脚本..."
cat > start_analysis.sh << 'EOF'
#!/bin/bash
cd ~/football-analysis
echo "启动足球分析系统..."
echo "1. 运行基础分析: python football_analysis_starter.py"
echo "2. 启动Jupyter Notebook: jupyter notebook"
echo "3. 运行每日分析: python daily_analysis.py"
echo ""
echo "请先配置API密钥："
echo "  - 编辑 config.py 中的 YOUR_API_KEY_HERE"
echo "  - 或编辑 football_analysis_starter.py"
EOF

chmod +x start_analysis.sh

echo "安装完成！"
echo "=========================="
echo "下一步操作："
echo "1. 获取API密钥: https://www.football-data.org/"
echo "2. 配置密钥: 编辑 config.py 或 football_analysis_starter.py"
echo "3. 启动分析: ./start_analysis.sh"
echo "4. 查看预测模型: cd predictions"
echo ""
echo "系统已准备就绪，立即开始分析！"