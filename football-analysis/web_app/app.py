#!/usr/bin/env python3
"""
足球分析系统Web应用 - 简化版本
"""

from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# API配置
API_KEY = "3d6575aa9dd54fb1aa460e194fafdef3"
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {'X-Auth-Token': API_KEY}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API状态检查"""
    try:
        response = requests.get(f"{BASE_URL}/competitions", headers=HEADERS)
        if response.status_code == 200:
            return jsonify({
                'status': 'online',
                'message': 'API连接正常',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'API返回错误: {response.status_code}',
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'连接失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/standings/<competition_code>')
def get_standings(competition_code):
    """获取联赛积分榜"""
    try:
        url = f"{BASE_URL}/competitions/{competition_code}/standings"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({
                'error': f'获取数据失败: {response.status_code}',
                'competition': competition_code
            })
    except Exception as e:
        return jsonify({
            'error': f'请求失败: {str(e)}',
            'competition': competition_code
        })

@app.route('/api/matches/today')
def get_today_matches():
    """获取今日比赛"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"{BASE_URL}/matches"
        params = {'dateFrom': today, 'dateTo': today}
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({
                'error': f'获取数据失败: {response.status_code}',
                'date': today
            })
    except Exception as e:
        return jsonify({
            'error': f'请求失败: {str(e)}',
            'date': today
        })

@app.route('/api/world_cup/analysis')
def world_cup_analysis():
    """世界杯分析（模拟数据）"""
    analysis = {
        'tournament': '2026 FIFA World Cup',
        'analysis_date': datetime.now().isoformat(),
        'groups': {
            'Group A': {
                'teams': ['Brazil', 'Argentina', 'Germany', 'Japan'],
                'predicted_winner': 'Brazil',
                'win_probability': 65
            },
            'Group B': {
                'teams': ['France', 'England', 'Spain', 'Portugal'],
                'predicted_winner': 'France',
                'win_probability': 60
            },
            'Group C': {
                'teams': ['Italy', 'Netherlands', 'Belgium', 'Croatia'],
                'predicted_winner': 'Italy',
                'win_probability': 55
            },
            'Group D': {
                'teams': ['Uruguay', 'Mexico', 'Senegal', 'South Korea'],
                'predicted_winner': 'Uruguay',
                'win_probability': 50
            }
        },
        'champion_prediction': {
            'top_contenders': [
                {'team': 'Brazil', 'probability': 25},
                {'team': 'France', 'probability': 20},
                {'team': 'Argentina', 'probability': 18},
                {'team': 'England', 'probability': 15},
                {'team': 'Germany', 'probability': 12},
                {'team': 'Italy', 'probability': 10}
            ]
        },
        'dark_horses': [
            {'team': 'Japan', 'reason': '技术流足球，团队配合出色'},
            {'team': 'Senegal', 'reason': '身体素质出色，防守稳固'},
            {'team': 'Croatia', 'reason': '大赛经验丰富，中场控制力强'}
        ]
    }
    return jsonify(analysis)

if __name__ == '__main__':
    print("=" * 60)
    print("足球分析系统Web应用")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("访问地址: http://localhost:5000")
    print("API状态: http://localhost:5000/api/status")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)