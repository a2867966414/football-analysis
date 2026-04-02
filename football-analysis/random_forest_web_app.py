#!/usr/bin/env python3
"""
随机森林足球预测Web应用
提供Web界面进行足球比赛预测
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

# 导入我们的预测器
from random_forest_football_predictor import FootballRandomForestPredictor

app = Flask(__name__, 
            template_folder='web_app/templates',
            static_folder='web_app/static')

# 全局预测器实例
predictor = None
model_trained = False

def init_predictor():
    """初始化预测器"""
    global predictor, model_trained
    
    print("初始化随机森林足球预测器...")
    predictor = FootballRandomForestPredictor(model_type='classifier', random_state=42)
    
    # 训练模型（使用合成数据）
    print("训练模型...")
    X, y = predictor.prepare_synthetic_data(n_samples=5000)
    evaluation = predictor.train_model(X, y, test_size=0.2, optimize_params=True)
    
    model_trained = True
    print(f"模型训练完成，测试准确率: {evaluation['test_score']:.4f}")
    
    return predictor

@app.route('/')
def index():
    """主页"""
    return render_template('random_forest_index.html')

@app.route('/api/model/status')
def model_status():
    """获取模型状态"""
    global predictor, model_trained
    
    if not model_trained or predictor is None:
        return jsonify({
            'status': 'not_trained',
            'message': '模型未训练'
        })
    
    info = predictor.get_model_info()
    
    return jsonify({
        'status': 'trained',
        'model_type': info['model_type'],
        'n_features': info['n_features'],
        'n_training_samples': info['n_training_samples'],
        'accuracy': info['training_history'][-1]['test_score'] if info['training_history'] else 0,
        'feature_count': len(info['feature_names']) if info['feature_names'] else 0,
        'last_trained': info['training_history'][-1]['timestamp'] if info['training_history'] else None
    })

@app.route('/api/predict/single', methods=['POST'])
def predict_single():
    """预测单场比赛"""
    global predictor, model_trained
    
    if not model_trained or predictor is None:
        return jsonify({
            'success': False,
            'error': '模型未训练，请先训练模型'
        })
    
    try:
        data = request.json
        
        # 提取特征
        match_features = {
            'home_team_strength': float(data.get('home_strength', 0.5)),
            'away_team_strength': float(data.get('away_strength', 0.5)),
            'strength_difference': float(data.get('home_strength', 0.5)) - float(data.get('away_strength', 0.5)),
            'home_recent_form': float(data.get('home_form', 0.5)),
            'away_recent_form': float(data.get('away_form', 0.5)),
            'form_difference': float(data.get('home_form', 0.5)) - float(data.get('away_form', 0.5)),
            'home_attack_power': float(data.get('home_attack', 0.5)),
            'away_attack_power': float(data.get('away_attack', 0.5)),
            'home_defense_strength': float(data.get('home_defense', 0.5)),
            'away_defense_strength': float(data.get('away_defense', 0.5)),
            'home_advantage': float(data.get('home_advantage', 0.2)),
            'home_injury_impact': float(data.get('home_injuries', 0.1)),
            'away_injury_impact': float(data.get('away_injuries', 0.1)),
            'head_to_head_record': float(data.get('head_to_head', 0.5)),
            'match_importance': float(data.get('importance', 0.5)),
            'weather_impact': float(data.get('weather', 0.0)),
            'fatigue_factor': float(data.get('fatigue', 0.1)),
            'attack_defense_ratio': float(data.get('home_attack', 0.5)) / (float(data.get('away_defense', 0.5)) + 0.001),
            'defense_attack_ratio': float(data.get('home_defense', 0.5)) / (float(data.get('away_attack', 0.5)) + 0.001)
        }
        
        # 预测
        prediction, probabilities = predictor.predict_match(match_features)
        
        # 映射结果
        result_map = {0: '客队胜', 1: '平局', 2: '主队胜'}
        result_text = result_map[prediction]
        
        # 格式化概率
        if probabilities is not None:
            prob_dict = {
                'away_win': float(probabilities[0][0]),
                'draw': float(probabilities[0][1]),
                'home_win': float(probabilities[0][2])
            }
        else:
            prob_dict = None
        
        # 分析特征重要性
        feature_importance = {}
        if hasattr(predictor.model, 'feature_importances_'):
            importances = predictor.model.feature_importances_
            for i, feature in enumerate(predictor.feature_names):
                feature_importance[feature] = float(importances[i])
        
        # 获取关键影响因素
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'result': result_text,
            'probabilities': prob_dict,
            'match_features': match_features,
            'top_features': top_features,
            'prediction_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """批量预测"""
    global predictor, model_trained
    
    if not model_trained or predictor is None:
        return jsonify({
            'success': False,
            'error': '模型未训练'
        })
    
    try:
        data = request.json
        matches = data.get('matches', [])
        
        if not matches:
            return jsonify({
                'success': False,
                'error': '没有提供比赛数据'
            })
        
        predictions = []
        
        for match in matches:
            match_features = {
                'home_team_strength': float(match.get('home_strength', 0.5)),
                'away_team_strength': float(match.get('away_strength', 0.5)),
                'strength_difference': float(match.get('home_strength', 0.5)) - float(match.get('away_strength', 0.5)),
                'home_recent_form': float(match.get('home_form', 0.5)),
                'away_recent_form': float(match.get('away_form', 0.5)),
                'form_difference': float(match.get('home_form', 0.5)) - float(match.get('away_form', 0.5)),
                'home_attack_power': float(match.get('home_attack', 0.5)),
                'away_attack_power': float(match.get('away_attack', 0.5)),
                'home_defense_strength': float(match.get('home_defense', 0.5)),
                'away_defense_strength': float(match.get('away_defense', 0.5)),
                'home_advantage': float(match.get('home_advantage', 0.2)),
                'home_injury_impact': float(match.get('home_injuries', 0.1)),
                'away_injury_impact': float(match.get('away_injuries', 0.1)),
                'head_to_head_record': float(match.get('head_to_head', 0.5)),
                'match_importance': float(match.get('importance', 0.5)),
                'weather_impact': float(match.get('weather', 0.0)),
                'fatigue_factor': float(match.get('fatigue', 0.1)),
                'attack_defense_ratio': float(match.get('home_attack', 0.5)) / (float(match.get('away_defense', 0.5)) + 0.001),
                'defense_attack_ratio': float(match.get('home_defense', 0.5)) / (float(match.get('away_attack', 0.5)) + 0.001)
            }
            
            prediction, probabilities = predictor.predict_match(match_features)
            
            result_map = {0: '客队胜', 1: '平局', 2: '主队胜'}
            
            predictions.append({
                'match_id': match.get('id', len(predictions)),
                'home_team': match.get('home_team', '主队'),
                'away_team': match.get('away_team', '客队'),
                'prediction': int(prediction),
                'result': result_map[prediction],
                'probabilities': {
                    'away_win': float(probabilities[0][0]) if probabilities is not None else 0,
                    'draw': float(probabilities[0][1]) if probabilities is not None else 0,
                    'home_win': float(probabilities[0][2]) if probabilities is not None else 0
                } if probabilities is not None else None
            })
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'total_matches': len(predictions),
            'prediction_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/model/retrain', methods=['POST'])
def retrain_model():
    """重新训练模型"""
    global predictor, model_trained
    
    try:
        data = request.json
        n_samples = int(data.get('n_samples', 5000))
        
        print(f"重新训练模型，使用 {n_samples} 个样本...")
        
        # 重新初始化预测器
        predictor = FootballRandomForestPredictor(model_type='classifier', random_state=42)
        
        # 训练模型
        X, y = predictor.prepare_synthetic_data(n_samples=n_samples)
        evaluation = predictor.train_model(X, y, test_size=0.2, optimize_params=True)
        
        model_trained = True
        
        return jsonify({
            'success': True,
            'message': f'模型重新训练完成，使用 {n_samples} 个样本',
            'accuracy': float(evaluation['test_score']),
            'training_samples': n_samples,
            'training_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/model/info')
def model_info():
    """获取模型详细信息"""
    global predictor, model_trained
    
    if not model_trained or predictor is None:
        return jsonify({
            'success': False,
            'error': '模型未训练'
        })
    
    try:
        info = predictor.get_model_info()
        
        # 获取特征重要性
        feature_importance = []
        if hasattr(predictor.model, 'feature_importances_'):
            importances = predictor.model.feature_importances_
            for i, feature in enumerate(predictor.feature_names):
                feature_importance.append({
                    'feature': feature,
                    'importance': float(importances[i])
                })
        
        # 按重要性排序
        feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        
        return jsonify({
            'success': True,
            'model_type': info['model_type'],
            'n_features': info['n_features'],
            'n_training_samples': info['n_training_samples'],
            'training_history': info['training_history'],
            'feature_names': info['feature_names'],
            'feature_importance': feature_importance[:10],  # 只返回前10个
            'model_created': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/examples')
def get_examples():
    """获取示例比赛数据"""
    examples = [
        {
            'id': 1,
            'name': '强队 vs 弱队',
            'home_strength': 0.85,
            'away_strength': 0.45,
            'home_form': 0.9,
            'away_form': 0.4,
            'home_attack': 0.8,
            'away_attack': 0.4,
            'home_defense': 0.7,
            'away_defense': 0.5,
            'home_advantage': 0.25,
            'home_injuries': 0.1,
            'away_injuries': 0.2,
            'head_to_head': 0.7,
            'importance': 0.8,
            'weather': 0.05,
            'fatigue': 0.1
        },
        {
            'id': 2,
            'name': '实力相当',
            'home_strength': 0.65,
            'away_strength': 0.63,
            'home_form': 0.6,
            'away_form': 0.62,
            'home_attack': 0.6,
            'away_attack': 0.58,
            'home_defense': 0.55,
            'away_defense': 0.57,
            'home_advantage': 0.2,
            'home_injuries': 0.15,
            'away_injuries': 0.1,
            'head_to_head': 0.52,
            'importance': 0.7,
            'weather': -0.1,
            'fatigue': 0.2
        },
        {
            'id': 3,
            'name': '潜在冷门',
            'home_strength': 0.45,
            'away_strength': 0.85,
            'home_form': 0.7,
            'away_form': 0.6,
            'home_attack': 0.5,
            'away_attack': 0.8,
            'home_defense': 0.6,
            'away_defense': 0.5,
            'home_advantage': 0.25,
            'home_injuries': 0.05,
            'away_injuries': 0.3,
            'head_to_head': 0.3,
            'importance': 0.9,
            'weather': 0.15,
            'fatigue': 0.3
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })

@app.route('/api/visualizations/<viz_type>')
def get_visualization(viz_type):
    """获取可视化图表"""
    viz_files = {
        'confusion_matrix': 'confusion_matrix.png',
        'feature_importance': 'feature_importance.png',
        'regression_results': 'regression_results.png',
        'training_history': 'training_history.png'
    }
    
    if viz_type in viz_files and os.path.exists(viz_files[viz_type]):
        return send_file(viz_files[viz_type], mimetype='image/png')
    else:
        return jsonify({
            'success': False,
            'error': f'可视化文件 {viz_type} 不存在'
        })

if __name__ == '__main__':
    # 初始化预测器
    init_predictor()
    
    # 启动Web应用
    print("="*60)
    print("随机森林足球预测Web应用")
    print("="*60)
    print(f"访问地址: http://localhost:9200")
    print("功能:")
    print("  - 单场比赛预测")
    print("  - 批量比赛预测")
    print("  - 模型状态查看")
    print("  - 特征重要性分析")
    print("  - 可视化图表")
    print("="*60)
    
    app.run(host='0.0.0.0', port=9200, debug=True)