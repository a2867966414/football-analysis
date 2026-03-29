#!/usr/bin/env python3
"""
个人足球分析系统 - 基础版本
立即可用，完全免费
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class FootballAnalyzer:
    def __init__(self, api_key=None):
        """初始化分析器"""
        self.api_key = api_key or "3d6575aa9dd54fb1aa460e194fafdef3"  # 您的API密钥
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': self.api_key}
        
    def get_competitions(self):
        """获取可用联赛"""
        url = f"{self.base_url}/competitions"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            competitions = response.json()['competitions']
            # 过滤主要联赛
            major_leagues = ['PL', 'PD', 'SA', 'BL1', 'FL1', 'CL']
            filtered = [c for c in competitions if c['code'] in major_leagues]
            return filtered
        return []
    
    def get_team_matches(self, team_id, limit=10):
        """获取球队最近比赛"""
        url = f"{self.base_url}/teams/{team_id}/matches"
        params = {'limit': limit}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()['matches']
        return []
    
    def analyze_team_form(self, matches):
        """分析球队状态"""
        if not matches:
            return {}
            
        results = []
        for match in matches:
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            score = match.get('score', {})
            
            if score.get('winner') == 'HOME_TEAM':
                results.append('W' if match['homeTeam']['id'] == team_id else 'L')
            elif score.get('winner') == 'AWAY_TEAM':
                results.append('W' if match['awayTeam']['id'] == team_id else 'L')
            else:
                results.append('D')
        
        # 计算状态
        last_5 = results[:5] if len(results) >= 5 else results
        form_stats = {
            'total_matches': len(results),
            'wins': results.count('W'),
            'draws': results.count('D'),
            'losses': results.count('L'),
            'last_5_form': ''.join(last_5),
            'win_rate': results.count('W') / len(results) * 100 if results else 0
        }
        return form_stats
    
    def predict_match(self, home_team_form, away_team_form):
        """简单预测模型"""
        # 基于状态的基础预测
        home_advantage = 0.15  # 主场优势
        
        home_strength = home_team_form.get('win_rate', 50) / 100
        away_strength = away_team_form.get('win_rate', 50) / 100
        
        # 调整主场优势
        home_strength += home_advantage
        away_strength -= home_advantage * 0.5
        
        # 归一化
        total = home_strength + away_strength
        if total > 0:
            home_prob = home_strength / total * 100
            away_prob = away_strength / total * 100
        else:
            home_prob = away_prob = 50
            
        draw_prob = 100 - home_prob - away_prob
        if draw_prob < 0:
            draw_prob = 0
            
        return {
            'home_win_prob': round(home_prob, 1),
            'draw_prob': round(draw_prob, 1),
            'away_win_prob': round(away_prob, 1),
            'prediction': '主场胜' if home_prob > away_prob and home_prob > draw_prob else 
                         '客场胜' if away_prob > home_prob and away_prob > draw_prob else '平局'
        }
    
    def visualize_form(self, team_name, form_stats):
        """可视化球队状态"""
        labels = ['胜', '平', '负']
        values = [form_stats['wins'], form_stats['draws'], form_stats['losses']]
        
        plt.figure(figsize=(10, 6))
        
        # 饼图
        plt.subplot(1, 2, 1)
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
        plt.title(f'{team_name} - 近期战绩分布')
        
        # 状态走势
        plt.subplot(1, 2, 2)
        form_sequence = form_stats['last_5_form']
        if form_sequence:
            # 转换为数值：W=3, D=1, L=0
            points = []
            for result in form_sequence:
                if result == 'W':
                    points.append(3)
                elif result == 'D':
                    points.append(1)
                else:
                    points.append(0)
            
            plt.plot(range(1, len(points)+1), points, marker='o', linewidth=2)
            plt.axhline(y=1.5, color='r', linestyle='--', alpha=0.5)
            plt.xlabel('最近比赛')
            plt.ylabel('得分 (W=3, D=1, L=0)')
            plt.title('状态走势图')
            plt.ylim(0, 3.5)
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{team_name}_form_analysis.png', dpi=100, bbox_inches='tight')
        plt.show()
        
        print(f"图表已保存为: {team_name}_form_analysis.png")

def main():
    """主函数 - 演示使用"""
    print("=" * 50)
    print("个人足球分析系统 v1.0")
    print("=" * 50)
    
    # 初始化分析器
    analyzer = FootballAnalyzer()
    
    # 演示数据（实际使用时需要真实API密钥）
    print("\n1. 获取可用联赛...")
    competitions = analyzer.get_competitions()
    if competitions:
        print(f"找到 {len(competitions)} 个主要联赛:")
        for comp in competitions[:5]:  # 显示前5个
            print(f"  - {comp['name']} ({comp['code']})")
    else:
        print("⚠️  无法获取联赛数据，请检查API密钥")
        print("💡 提示：访问 https://www.football-data.org/ 获取免费API密钥")
    
    print("\n2. 模拟球队状态分析...")
    # 模拟数据
    mock_matches = [
        {'homeTeam': {'id': 1, 'name': 'Team A'}, 'awayTeam': {'id': 2, 'name': 'Team B'}, 
         'score': {'winner': 'HOME_TEAM'}},
        {'homeTeam': {'id': 2, 'name': 'Team B'}, 'awayTeam': {'id': 3, 'name': 'Team C'}, 
         'score': {'winner': 'DRAW'}},
        {'homeTeam': {'id': 1, 'name': 'Team A'}, 'awayTeam': {'id': 3, 'name': 'Team C'}, 
         'score': {'winner': 'AWAY_TEAM'}},
    ]
    
    team_id = 1  # Team A
    form_stats = analyzer.analyze_team_form(mock_matches)
    
    print(f"球队状态分析:")
    print(f"  总比赛: {form_stats['total_matches']}")
    print(f"  胜/平/负: {form_stats['wins']}/{form_stats['draws']}/{form_stats['losses']}")
    print(f"  胜率: {form_stats['win_rate']:.1f}%")
    print(f"  最近5场: {form_stats['last_5_form']}")
    
    print("\n3. 比赛预测演示...")
    home_form = {'win_rate': 60}
    away_form = {'win_rate': 40}
    prediction = analyzer.predict_match(home_form, away_form)
    
    print(f"预测结果:")
    print(f"  主场胜概率: {prediction['home_win_prob']}%")
    print(f"  平局概率: {prediction['draw_prob']}%")
    print(f"  客场胜概率: {prediction['away_win_prob']}%")
    print(f"  预测: {prediction['prediction']}")
    
    print("\n4. 下一步操作:")
    print("  a) 获取免费API密钥: https://www.football-data.org/")
    print("  b) 替换脚本中的 YOUR_API_KEY_HERE")
    print("  c) 运行完整分析: python football_analysis_starter.py")
    print("  d) 查看开源项目获取更多功能")
    
    print("\n" + "=" * 50)
    print("立即开始分析！祝您好运！")
    print("=" * 50)

if __name__ == "__main__":
    main()