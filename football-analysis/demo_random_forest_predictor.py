#!/usr/bin/env python3
"""
随机森林足球预测系统演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from random_forest_football_predictor import FootballRandomForestPredictor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    """主演示函数"""
    print("="*70)
    print("专业随机森林足球预测系统演示")
    print("="*70)
    
    # 1. 创建分类预测器（预测胜平负）
    print("\n1. 创建分类预测器（预测胜平负）")
    print("-"*50)
    
    classifier = FootballRandomForestPredictor(model_type='classifier', random_state=42)
    
    # 2. 准备数据
    print("\n2. 准备训练数据")
    print("-"*50)
    X, y = classifier.prepare_synthetic_data(n_samples=5000)
    
    # 查看数据分布
    print(f"\n数据分布:")
    print(f"  总样本数: {len(X)}")
    print(f"  特征数量: {X.shape[1]}")
    
    if classifier.model_type == 'classifier':
        unique, counts = np.unique(y, return_counts=True)
        result_map = {0: '客队胜', 1: '平局', 2: '主队胜'}
        for res, count in zip(unique, counts):
            print(f"  {result_map[res]}: {count} ({count/len(y)*100:.1f}%)")
    
    # 3. 训练模型
    print("\n3. 训练随机森林模型")
    print("-"*50)
    evaluation = classifier.train_model(X, y, test_size=0.2, optimize_params=True)
    
    # 4. 评估模型
    print("\n4. 模型性能评估")
    print("-"*50)
    classifier.evaluate_model(evaluation)
    
    # 5. 预测示例比赛
    print("\n5. 预测示例比赛")
    print("-"*50)
    
    # 示例1：强队 vs 弱队
    print("\n示例1: 强队(主) vs 弱队(客)")
    strong_vs_weak = {
        'home_team_strength': 0.85,
        'away_team_strength': 0.45,
        'strength_difference': 0.4,
        'home_recent_form': 0.9,
        'away_recent_form': 0.4,
        'form_difference': 0.5,
        'home_attack_power': 0.8,
        'away_attack_power': 0.4,
        'home_defense_strength': 0.7,
        'away_defense_strength': 0.5,
        'home_advantage': 0.25,
        'home_injury_impact': 0.1,
        'away_injury_impact': 0.2,
        'head_to_head_record': 0.7,
        'match_importance': 0.8,
        'weather_impact': 0.05,
        'fatigue_factor': 0.1,
        'attack_defense_ratio': 0.8 / 0.5,
        'defense_attack_ratio': 0.7 / 0.4
    }
    
    prediction1 = classifier.predict_match(strong_vs_weak)
    if prediction1:
        result, probabilities = prediction1
        result_map = {0: '客队胜', 1: '平局', 2: '主队胜'}
        print(f"  预测结果: {result_map[result]}")
        print(f"  概率分布: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 示例2：实力相当
    print("\n示例2: 实力相当的对决")
    even_match = {
        'home_team_strength': 0.65,
        'away_team_strength': 0.63,
        'strength_difference': 0.02,
        'home_recent_form': 0.6,
        'away_recent_form': 0.62,
        'form_difference': -0.02,
        'home_attack_power': 0.6,
        'away_attack_power': 0.58,
        'home_defense_strength': 0.55,
        'away_defense_strength': 0.57,
        'home_advantage': 0.2,
        'home_injury_impact': 0.15,
        'away_injury_impact': 0.1,
        'head_to_head_record': 0.52,
        'match_importance': 0.7,
        'weather_impact': -0.1,
        'fatigue_factor': 0.2,
        'attack_defense_ratio': 0.6 / 0.57,
        'defense_attack_ratio': 0.55 / 0.58
    }
    
    prediction2 = classifier.predict_match(even_match)
    if prediction2:
        result, probabilities = prediction2
        print(f"  预测结果: {result_map[result]}")
        print(f"  概率分布: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 示例3：弱队 vs 强队（冷门可能）
    print("\n示例3: 弱队(主) vs 强队(客) - 潜在冷门")
    weak_vs_strong = {
        'home_team_strength': 0.45,
        'away_team_strength': 0.85,
        'strength_difference': -0.4,
        'home_recent_form': 0.7,  # 主队近期状态不错
        'away_recent_form': 0.6,  # 客队状态一般
        'form_difference': 0.1,
        'home_attack_power': 0.5,
        'away_attack_power': 0.8,
        'home_defense_strength': 0.6,  # 主队防守不错
        'away_defense_strength': 0.5,  # 客队防守有漏洞
        'home_advantage': 0.25,
        'home_injury_impact': 0.05,
        'away_injury_impact': 0.3,  # 客队伤病严重
        'head_to_head_record': 0.3,
        'match_importance': 0.9,  # 重要比赛
        'weather_impact': 0.15,  # 天气对客队不利
        'fatigue_factor': 0.3,  # 客队疲劳
        'attack_defense_ratio': 0.5 / 0.5,
        'defense_attack_ratio': 0.6 / 0.8
    }
    
    prediction3 = classifier.predict_match(weak_vs_strong)
    if prediction3:
        result, probabilities = prediction3
        print(f"  预测结果: {result_map[result]}")
        print(f"  概率分布: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 6. 创建回归预测器（预测比分差）
    print("\n" + "="*70)
    print("6. 创建回归预测器（预测比分差）")
    print("="*70)
    
    regressor = FootballRandomForestPredictor(model_type='regressor', random_state=42)
    
    # 准备回归数据
    print("\n准备回归训练数据...")
    X_reg, y_reg = regressor.prepare_synthetic_data(n_samples=3000)
    
    print(f"\n回归目标变量统计:")
    print(f"  均值: {y_reg.mean():.3f}")
    print(f"  标准差: {y_reg.std():.3f}")
    print(f"  最小值: {y_reg.min():.3f}")
    print(f"  最大值: {y_reg.max():.3f}")
    
    # 训练回归模型
    print("\n训练回归模型...")
    evaluation_reg = regressor.train_model(X_reg, y_reg, test_size=0.2, optimize_params=True)
    
    # 评估回归模型
    print("\n回归模型评估:")
    regressor.evaluate_model(evaluation_reg)
    
    # 7. 批量预测示例
    print("\n" + "="*70)
    print("7. 批量预测示例")
    print("="*70)
    
    # 创建批量预测数据
    batch_matches = []
    for i in range(5):
        match = {
            'home_team_strength': np.random.uniform(0.5, 0.9),
            'away_team_strength': np.random.uniform(0.4, 0.8),
            'strength_difference': 0,
            'home_recent_form': np.random.uniform(0.4, 0.9),
            'away_recent_form': np.random.uniform(0.3, 0.8),
            'form_difference': 0,
            'home_attack_power': np.random.uniform(0.4, 0.8),
            'away_attack_power': np.random.uniform(0.3, 0.7),
            'home_defense_strength': np.random.uniform(0.4, 0.8),
            'away_defense_strength': np.random.uniform(0.3, 0.7),
            'home_advantage': np.random.uniform(0.1, 0.25),
            'home_injury_impact': np.random.uniform(0, 0.3),
            'away_injury_impact': np.random.uniform(0, 0.3),
            'head_to_head_record': np.random.uniform(0.3, 0.7),
            'match_importance': np.random.uniform(0.5, 0.9),
            'weather_impact': np.random.uniform(-0.1, 0.1),
            'fatigue_factor': np.random.uniform(0, 0.2),
            'attack_defense_ratio': 0,
            'defense_attack_ratio': 0
        }
        
        # 计算衍生特征
        match['strength_difference'] = match['home_team_strength'] - match['away_team_strength']
        match['form_difference'] = match['home_recent_form'] - match['away_recent_form']
        match['attack_defense_ratio'] = match['home_attack_power'] / (match['away_defense_strength'] + 0.001)
        match['defense_attack_ratio'] = match['home_defense_strength'] / (match['away_attack_power'] + 0.001)
        
        batch_matches.append(match)
    
    print(f"\n批量预测 {len(batch_matches)} 场比赛:")
    print("-"*50)
    
    for i, match in enumerate(batch_matches, 1):
        prediction = classifier.predict_match(match)
        if prediction:
            result, probabilities = prediction
            print(f"\n比赛 {i}:")
            print(f"  主队实力: {match['home_team_strength']:.3f} vs 客队实力: {match['away_team_strength']:.3f}")
            print(f"  实力差: {match['strength_difference']:.3f}")
            print(f"  预测结果: {result_map[result]}")
            print(f"  概率: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 8. 模型保存和加载演示
    print("\n" + "="*70)
    print("8. 模型保存和加载")
    print("="*70)
    
    # 保存模型
    save_path = "football_random_forest_model.pkl"
    classifier.save_model(save_path)
    print(f"模型已保存到: {save_path}")
    
    # 加载模型
    loaded_classifier = FootballRandomForestPredictor.load_model(save_path)
    print(f"模型已从 {save_path} 加载")
    
    # 使用加载的模型进行预测
    test_match = strong_vs_weak
    loaded_prediction = loaded_classifier.predict_match(test_match)
    if loaded_prediction:
        result, probabilities = loaded_prediction
        print(f"\n使用加载的模型预测:")
        print(f"  预测结果: {result_map[result]}")
        print(f"  概率分布: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 9. 性能总结
    print("\n" + "="*70)
    print("性能总结")
    print("="*70)
    
    print("\n分类模型:")
    print(f"  测试准确率: {evaluation['test_score']:.4f}")
    print(f"  训练准确率: {evaluation['train_score']:.4f}")
    
    if 'regressor' in locals():
        print("\n回归模型:")
        print(f"  测试R²得分: {evaluation_reg['test_score']:.4f}")
        print(f"  训练R²得分: {evaluation_reg['train_score']:.4f}")
    
    print("\n" + "="*70)
    print("演示完成!")
    print("="*70)
    
    # 显示生成的可视化文件
    print("\n生成的可视化文件:")
    viz_files = ['confusion_matrix.png', 'feature_importance.png', 'regression_results.png']
    for file in viz_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (未生成)")

if __name__ == "__main__":
    main()