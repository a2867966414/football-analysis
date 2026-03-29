#!/usr/bin/env python3
"""
增强版Web应用 - 对标市场最火足球分析系统
集成实时数据、AI预测、价值检测等高级功能
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import asyncio
import threading
import json
from datetime import datetime
import time
from typing import Dict, List
import logging

# 导入我们的实时引擎
from real_time_engine import RealTimeEngine, AIValueDetector, LiveMatch

# 配置
app = Flask(__name__, 
           template_folder='web_app/templates',
           static_folder='web_app/static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局实例
real_time_engine = None
value_detector = None
update_thread = None

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_system():
    """初始化系统"""
    global real_time_engine, value_detector
    
    logger.info("初始化增强版足球分析系统...")
    
    # 创建实时引擎
    real_time_engine = RealTimeEngine()
    
    # 创建价值检测器
    value_detector = AIValueDetector()
    
    logger.info("系统初始化完成")

def start_background_updates():
    """启动后台更新线程"""
    def update_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_updates():
            await real_time_engine.update_live_data()
        
        loop.run_until_complete(run_updates())
    
    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()
    return thread

# 路由定义
@app.route('/')
def index():
    """增强版主页"""
    return render_template('enhanced_index.html')

@app.route('/dashboard')
def dashboard():
    """专业仪表板"""
    return render_template('dashboard.html')

@app.route('/live')
def live_matches_page():
    """实时比赛页面"""
    return render_template('live_matches.html')

@app.route('/predictions')
def predictions_page():
    """AI预测页面"""
    return render_template('predictions.html')

@app.route('/value')
def value_detection_page():
    """价值检测页面"""
    return render_template('value_detection.html')

# API端点
@app.route('/api/v2/status')
def api_status_v2():
    """增强版API状态"""
    return jsonify({
        'status': 'online',
        'version': '2.0.0',
        'features': [
            'real_time_data',
            'ai_predictions', 
            'value_detection',
            'live_updates',
            'multi_competition'
        ],
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time() - app_start_time
    })

@app.route('/api/v2/live/matches')
def get_live_matches():
    """获取实时比赛"""
    if not real_time_engine:
        return jsonify({'error': '系统未初始化'}), 500
    
    matches = real_time_engine.get_live_matches()
    
    # 转换为JSON可序列化格式
    serialized_matches = []
    for match in matches:
        serialized_matches.append({
            'id': match.match_id,
            'competition': match.competition,
            'home_team': match.home_team,
            'away_team': match.away_team,
            'score': match.score,
            'minute': match.minute,
            'status': match.status,
            'events_count': len(match.events),
            'last_update': match.last_update.isoformat(),
            'statistics': match.statistics
        })
    
    return jsonify({
        'count': len(serialized_matches),
        'matches': serialized_matches,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v2/live/match/<match_id>')
def get_live_match(match_id):
    """获取特定实时比赛"""
    if not real_time_engine:
        return jsonify({'error': '系统未初始化'}), 500
    
    match = real_time_engine.get_match_by_id(match_id)
    if not match:
        return jsonify({'error': '比赛未找到'}), 404
    
    # 转换事件为可序列化格式
    events = []
    for event in match.events:
        events.append({
            'type': event.event_type,
            'minute': event.minute,
            'team': event.team,
            'player': event.player,
            'details': event.details,
            'timestamp': event.timestamp.isoformat()
        })
    
    return jsonify({
        'id': match.match_id,
        'competition': match.competition,
        'home_team': match.home_team,
        'away_team': match.away_team,
        'score': match.score,
        'minute': match.minute,
        'status': match.status,
        'events': events,
        'statistics': match.statistics,
        'last_update': match.last_update.isoformat()
    })

@app.route('/api/v2/value/opportunities')
def get_value_opportunities():
    """获取价值机会"""
    if not real_time_engine or not value_detector:
        return jsonify({'error': '系统未初始化'}), 500
    
    matches = real_time_engine.get_live_matches()
    all_opportunities = []
    
    for match in matches:
        opportunities = value_detector.detect_value_opportunities(match)
        if opportunities['opportunities']:
            all_opportunities.append(opportunities)
    
    return jsonify({
        'count': len(all_opportunities),
        'opportunities': all_opportunities,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v2/predict/match', methods=['POST'])
def predict_match():
    """AI比赛预测"""
    data = request.json
    
    if not data or 'home_team' not in data or 'away_team' not in data:
        return jsonify({'error': '需要home_team和away_team参数'}), 400
    
    # 模拟AI预测
    home_team = data['home_team']
    away_team = data['away_team']
    venue = data.get('venue', 'neutral')
    
    # 简化的预测逻辑
    # 实际应该使用机器学习模型
    import random
    
    if venue == 'home':
        home_win_prob = 0.45
        draw_prob = 0.30
        away_win_prob = 0.25
    elif venue == 'away':
        home_win_prob = 0.35
        draw_prob = 0.30
        away_win_prob = 0.35
    else:
        home_win_prob = 0.40
        draw_prob = 0.30
        away_win_prob = 0.30
    
    # 添加一些随机性
    home_win_prob += random.uniform(-0.05, 0.05)
    draw_prob += random.uniform(-0.05, 0.05)
    away_win_prob += random.uniform(-0.05, 0.05)
    
    # 归一化
    total = home_win_prob + draw_prob + away_win_prob
    home_win_prob /= total
    draw_prob /= total
    away_win_prob /= total
    
    prediction = {
        'home_team': home_team,
        'away_team': away_team,
        'venue': venue,
        'predictions': {
            'home_win': round(home_win_prob * 100, 1),
            'draw': round(draw_prob * 100, 1),
            'away_win': round(away_win_prob * 100, 1)
        },
        'recommended_bet': 'home_win' if home_win_prob > 0.4 else 'draw' if draw_prob > 0.35 else 'away_win',
        'confidence': round(max(home_win_prob, draw_prob, away_win_prob) * 100, 1),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(prediction)

@app.route('/api/v2/competitions')
def get_competitions():
    """获取支持的联赛"""
    competitions = [
        {'id': 'PL', 'name': 'Premier League', 'country': 'England'},
        {'id': 'PD', 'name': 'La Liga', 'country': 'Spain'},
        {'id': 'SA', 'name': 'Serie A', 'country': 'Italy'},
        {'id': 'BL1', 'name': 'Bundesliga', 'country': 'Germany'},
        {'id': 'FL1', 'name': 'Ligue 1', 'country': 'France'},
        {'id': 'CL', 'name': 'Champions League', 'country': 'Europe'},
        {'id': 'EL', 'name': 'Europa League', 'country': 'Europe'},
        {'id': 'WC', 'name': 'World Cup', 'country': 'International'}
    ]
    
    return jsonify({
        'count': len(competitions),
        'competitions': competitions
    })

# WebSocket事件
@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端连接: {request.sid}")
    emit('connected', {'message': '连接成功', 'timestamp': datetime.now().isoformat()})

@socketio.on('subscribe_live')
def handle_subscribe_live(data):
    """订阅实时更新"""
    match_id = data.get('match_id')
    
    if match_id:
        logger.info(f"客户端订阅比赛: {match_id}")
        emit('subscription_confirmed', {
            'match_id': match_id,
            'message': '订阅成功',
            'timestamp': datetime.now().isoformat()
        })
    else:
        emit('subscription_error', {
            'error': '需要match_id参数',
            'timestamp': datetime.now().isoformat()
        })

@socketio.on('request_prediction')
def handle_prediction_request(data):
    """处理预测请求"""
    home_team = data.get('home_team')
    away_team = data.get('away_team')
    
    if home_team and away_team:
        # 这里可以调用AI预测模型
        emit('prediction_result', {
            'home_team': home_team,
            'away_team': away_team,
            'prediction': '模拟预测结果',
            'confidence': 75.5,
            'timestamp': datetime.now().isoformat()
        })

# 后台任务：定期推送更新
def background_updates():
    """后台更新任务"""
    while True:
        time.sleep(10)  # 每10秒更新一次
        
        if real_time_engine:
            # 获取实时比赛
            matches = real_time_engine.get_live_matches()
            
            if matches:
                # 推送更新给所有连接的客户端
                socketio.emit('live_update', {
                    'match_count': len(matches),
                    'timestamp': datetime.now().isoformat()
                })
                
                # 如果有价值机会，也推送
                if value_detector:
                    for match in matches[:3]:  # 只检查前3场
                        opportunities = value_detector.detect_value_opportunities(match)
                        if opportunities['opportunities']:
                            socketio.emit('value_opportunity', opportunities)

# 启动函数
def start_enhanced_system():
    """启动增强版系统"""
    global app_start_time, update_thread
    
    app_start_time = time.time()
    
    # 初始化系统
    init_system()
    
    # 启动后台更新线程
    update_thread = threading.Thread(target=background_updates, daemon=True)
    update_thread.start()
    
    logger.info("增强版足球分析系统启动完成")
    logger.info("访问 http://localhost:5001 使用增强功能")
    
    # 启动Flask应用
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    start_enhanced_system()