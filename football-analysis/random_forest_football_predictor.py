#!/usr/bin/env python3
"""
专业随机森林足球预测系统
基于您的代码优化和扩展
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import pickle
import os

# 机器学习库
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# 可视化设置
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class FootballRandomForestPredictor:
    """专业随机森林足球预测器"""
    
    def __init__(self, model_type='classifier', random_state=42):
        """
        初始化预测器
        
        参数:
            model_type: 'classifier' 分类或 'regressor' 回归
            random_state: 随机种子
        """
        self.model_type = model_type
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.model = None
        self.feature_names = None
        self.training_history = []
        
        # 初始化模型
        if model_type == 'classifier':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1,
                verbose=0
            )
        else:
            self.model = RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1,
                verbose=0
            )
    
    def prepare_synthetic_data(self, n_samples=5000):
        """
        准备合成足球比赛数据（模拟真实场景）
        
        参数:
            n_samples: 样本数量
            
        返回:
            X: 特征数据
            y: 目标变量
        """
        print(f"生成 {n_samples} 个足球比赛样本...")
        
        np.random.seed(self.random_state)
        
        # 定义特征（基于真实足球分析）
        features = {
            # 球队实力相关
            'home_team_strength': np.random.uniform(0.4, 1.0, n_samples),  # 主队实力 (0-1)
            'away_team_strength': np.random.uniform(0.3, 0.9, n_samples),  # 客队实力 (0-1)
            'strength_difference': np.zeros(n_samples),  # 实力差
            
            # 近期状态
            'home_recent_form': np.random.uniform(0.3, 1.0, n_samples),  # 主队近期状态
            'away_recent_form': np.random.uniform(0.2, 0.9, n_samples),  # 客队近期状态
            'form_difference': np.zeros(n_samples),  # 状态差
            
            # 进攻防守能力
            'home_attack_power': np.random.uniform(0.3, 1.0, n_samples),  # 主队进攻力
            'away_attack_power': np.random.uniform(0.2, 0.9, n_samples),  # 客队进攻力
            'home_defense_strength': np.random.uniform(0.3, 1.0, n_samples),  # 主队防守力
            'away_defense_strength': np.random.uniform(0.2, 0.9, n_samples),  # 客队防守力
            
            # 特殊因素
            'home_advantage': np.random.uniform(0.1, 0.3, n_samples),  # 主场优势
            'home_injury_impact': np.random.uniform(0, 0.4, n_samples),  # 主队伤病影响
            'away_injury_impact': np.random.uniform(0, 0.4, n_samples),  # 客队伤病影响
            'head_to_head_record': np.random.uniform(0.2, 0.8, n_samples),  # 历史交锋记录
            
            # 比赛重要性
            'match_importance': np.random.uniform(0.3, 1.0, n_samples),  # 比赛重要性
            
            # 环境因素
            'weather_impact': np.random.uniform(-0.2, 0.2, n_samples),  # 天气影响
            'fatigue_factor': np.random.uniform(0, 0.3, n_samples),  # 疲劳因素
        }
        
        # 计算衍生特征
        features['strength_difference'] = features['home_team_strength'] - features['away_team_strength']
        features['form_difference'] = features['home_recent_form'] - features['away_recent_form']
        features['attack_defense_ratio'] = features['home_attack_power'] / (features['away_defense_strength'] + 0.001)
        features['defense_attack_ratio'] = features['home_defense_strength'] / (features['away_attack_power'] + 0.001)
        
        # 创建特征DataFrame
        X = pd.DataFrame(features)
        self.feature_names = X.columns.tolist()
        
        # 生成目标变量（基于复杂规则模拟真实比赛结果）
        if self.model_type == 'classifier':
            # 分类问题：胜(2)、平(1)、负(0)
            y = self._generate_classification_target(X)
        else:
            # 回归问题：预测比分差
            y = self._generate_regression_target(X)
        
        print(f"数据生成完成: {X.shape[0]} 个样本, {X.shape[1]} 个特征")
        return X, y
    
    def _generate_classification_target(self, X):
        """生成分类目标变量"""
        # 基于多个特征的综合评分
        score = (
            X['strength_difference'] * 0.3 +
            X['form_difference'] * 0.25 +
            X['home_advantage'] * 0.15 -
            X['home_injury_impact'] * 0.1 +
            X['away_injury_impact'] * 0.1 +
            (X['head_to_head_record'] - 0.5) * 0.1 +
            np.random.normal(0, 0.1, len(X))  # 随机噪声
        )
        
        # 根据评分生成结果
        y = np.where(score > 0.3, 2, np.where(score < -0.2, 0, 1))
        
        # 添加一些意外结果（冷门）
        n_samples = len(X)
        upset_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
        for idx in upset_indices:
            if y[idx] == 2:  # 主队胜变客队胜
                y[idx] = 0
            elif y[idx] == 0:  # 客队胜变主队胜
                y[idx] = 2
        
        return y
    
    def _generate_regression_target(self, X):
        """生成回归目标变量（比分差）"""
        # 基于特征预测比分差
        goal_difference = (
            X['strength_difference'] * 1.5 +
            X['form_difference'] * 1.2 +
            X['home_advantage'] * 0.8 -
            X['home_injury_impact'] * 0.6 +
            X['away_injury_impact'] * 0.6 +
            (X['head_to_head_record'] - 0.5) * 0.5 +
            np.random.normal(0, 0.3, len(X))  # 随机噪声
        )
        
        # 限制在合理范围
        goal_difference = np.clip(goal_difference, -4, 4)
        
        return goal_difference
    
    def preprocess_data(self, X, y=None, fit=True):
        """数据预处理"""
        print("数据预处理中...")
        
        if fit:
            # 训练模式：拟合转换器
            X_imputed = self.imputer.fit_transform(X)
            X_scaled = self.scaler.fit_transform(X_imputed)
        else:
            # 预测模式：使用已拟合的转换器
            X_imputed = self.imputer.transform(X)
            X_scaled = self.scaler.transform(X_imputed)
        
        print(f"数据预处理完成: 缺失值填充, 特征标准化")
        return X_scaled, y
    
    def train_model(self, X, y, test_size=0.2, optimize_params=True):
        """训练模型"""
        print("开始训练模型...")
        
        # 数据分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y if self.model_type == 'classifier' else None
        )
        
        # 预处理训练数据
        X_train_scaled, y_train = self.preprocess_data(X_train, y_train, fit=True)
        
        # 参数优化
        if optimize_params:
            print("进行参数优化...")
            best_params = self._optimize_parameters(X_train_scaled, y_train)
            if best_params:
                if self.model_type == 'classifier':
                    self.model = RandomForestClassifier(**best_params, random_state=self.random_state, n_jobs=-1)
                else:
                    self.model = RandomForestRegressor(**best_params, random_state=self.random_state, n_jobs=-1)
        
        # 训练模型
        print("训练随机森林模型...")
        self.model.fit(X_train_scaled, y_train)
        
        # 预处理测试数据
        X_test_scaled, y_test = self.preprocess_data(X_test, y_test, fit=False)
        
        # 评估模型
        print("评估模型性能...")
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        # 预测
        y_pred = self.model.predict(X_test_scaled)
        
        # 保存训练历史
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'train_score': train_score,
            'test_score': test_score,
            'n_samples': len(X_train),
            'n_features': X_train.shape[1]
        })
        
        # 返回评估结果
        evaluation = {
            'train_score': train_score,
            'test_score': test_score,
            'y_test': y_test,
            'y_pred': y_pred,
            'X_test': X_test,
            'X_test_scaled': X_test_scaled
        }
        
        return evaluation
    
    def _optimize_parameters(self, X, y):
        """优化模型参数"""
        if self.model_type == 'classifier':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2']
            }
        else:
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': [0.5, 0.7, 1.0]
            }
        
        try:
            grid_search = GridSearchCV(
                self.model.__class__(random_state=self.random_state),
                param_grid,
                cv=5,
                scoring='accuracy' if self.model_type == 'classifier' else 'r2',
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X, y)
            
            print(f"最佳参数: {grid_search.best_params_}")
            print(f"交叉验证最佳得分: {grid_search.best_score_:.4f}")
            
            return grid_search.best_params_
        except Exception as e:
            print(f"参数优化失败: {e}")
            return None
    
    def evaluate_model(self, evaluation):
        """评估模型性能"""
        print("\n" + "="*60)
        print("模型性能评估")
        print("="*60)
        
        y_test = evaluation['y_test']
        y_pred = evaluation['y_pred']
        
        if self.model_type == 'classifier':
            # 分类评估
            accuracy = accuracy_score(y_test, y_pred)
            print(f"准确率: {accuracy:.4f}")
            print(f"训练集得分: {evaluation['train_score']:.4f}")
            print(f"测试集得分: {evaluation['test_score']:.4f}")
            
            print("\n分类报告:")
            print(classification_report(y_test, y_pred, 
                                       target_names=['客队胜 (0)', '平局 (1)', '主队胜 (2)']))
            
            # 混淆矩阵
            cm = confusion_matrix(y_test, y_pred)
            self._plot_confusion_matrix(cm)
            
        else:
            # 回归评估
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"均方误差 (MSE): {mse:.4f}")
            print(f"平均绝对误差 (MAE): {mae:.4f}")
            print(f"R² 得分: {r2:.4f}")
            print(f"训练集得分: {evaluation['train_score']:.4f}")
            print(f"测试集得分: {evaluation['test_score']:.4f}")
            
            # 预测 vs 实际图
            self._plot_regression_results(y_test, y_pred)
        
        # 特征重要性
        self._analyze_feature_importance()
    
    def _plot_confusion_matrix(self, cm):
        """绘制混淆矩阵"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['客队胜', '平局', '主队胜'],
                   yticklabels=['客队胜', '平局', '主队胜'])
        plt.title('混淆矩阵')
        plt.ylabel('真实标签')
        plt.xlabel('预测标签')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_regression_results(self, y_true, y_pred):
        """绘制回归结果"""
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        plt.scatter(y_true, y_pred, alpha=0.5)
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
        plt.xlabel('实际值')
        plt.ylabel('预测值')
        plt.title('预测 vs 实际')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        residuals = y_true - y_pred
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('预测值')
        plt.ylabel('残差')
        plt.title('残差图')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('regression_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _analyze_feature_importance(self):
        """分析特征重要性"""
        if self.model is None:
            print("模型未训练，无法分析特征重要性")
            return
        
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            print("\n" + "="*60)
            print("特征重要性排名")
            print("="*60)
            
            feature_importance_df = pd.DataFrame({
                '特征': [self.feature_names[i] for i in indices],
                '重要性': importances[indices]
            })
            
            print(feature_importance_df.to_string(index=False))
            
            # 可视化特征重要性
            plt.figure(figsize=(12, 8))
            plt.barh(range(min(20, len(indices))), importances[indices][:20][::-1])
            plt.yticks(range(min(20, len(indices))), 
                      [self.feature_names[i] for i in indices[:20]][::-1])
            plt.xlabel('特征重要性')
            plt.title('Top 20 特征重要性')
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def predict_match(self, match_features):
        """预测单场比赛"""
        if self.model is None:
            print("请先训练模型")
            return None
        
        # 确保特征顺序正确
        if isinstance(match_features, dict):
            match_df = pd.DataFrame([match_features])
            # 确保所有特征都存在
            for feature in self.feature_names:
                if feature not in match_df.columns:
                    match_df[feature] = 0  # 默认值
            match_df = match_df[self.feature_names]
        else:
            match_df = pd.DataFrame(match_features, columns=self.feature_names)
        
        # 预处理
        match_scaled, _ = self.preprocess_data(match_df, fit=False)
        
        # 预测
        prediction = self.model.predict(match_scaled)
        
        # 获取概率（如果是分类器）
        if self.model_type == 'classifier' and hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(match_scaled)
        else:
            probabilities = None
        
        return prediction[0], probabilities
    
    def predict_batch(self, matches_features):
        """批量预测多场比赛"""
        if self.model is None:
            print("请先训练模型")
            return None
        
        # 准备批量数据
        matches_df = pd.DataFrame(matches_features)
        
        # 确保所有特征都存在
        for feature in self.feature_names:
            if feature not in matches_df.columns:
                matches_df[feature] = 0  # 默认值
        
        matches_df = matches_df[self.feature_names]
        
        # 预处理
        matches_scaled, _ = self.preprocess_data(matches_df, fit=False)
        
        # 预测
        predictions = self.model.predict(matches_scaled)
        
        # 获取概率（如果是分类器）
        if self.model_type == 'classifier' and hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(matches_scaled)
        else:
            probabilities = None
        
        return predictions, probabilities
    
    def save_model(self, filepath):
        """保存模型到文件"""
        import pickle
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'imputer': self.imputer,
            'feature_names': self.feature_names,
            'model_type': self.model_type,
            'random_state': self.random_state,
            'training_history': self.training_history
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"模型已保存到: {filepath}")
    
    @classmethod
    def load_model(cls, filepath):
        """从文件加载模型"""
        import pickle
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        # 创建新实例
        predictor = cls(
            model_type=model_data['model_type'],
            random_state=model_data['random_state']
        )
        
        # 恢复状态
        predictor.model = model_data['model']
        predictor.scaler = model_data['scaler']
        predictor.imputer = model_data['imputer']
        predictor.feature_names = model_data['feature_names']
        predictor.training_history = model_data['training_history']
        
        return predictor
    
    def get_model_info(self):
        """获取模型信息"""
        if self.model is None:
            return "模型未训练"
        
        info = {
            'model_type': self.model_type,
            'n_features': len(self.feature_names) if self.feature_names else 0,
            'n_training_samples': sum([h['n_samples'] for h in self.training_history]) if self.training_history else 0,
            'training_history': self.training_history,
            'feature_names': self.feature_names
        }
        
        if self.model_type == 'classifier':
            info['n_classes'] = len(self.model.classes_) if hasattr(self.model, 'classes_') else '未知'
        
        return info
    
    def plot_training_history(self):
        """绘制训练历史"""
        if not self.training_history:
            print("没有训练历史数据")
            return
        
        history_df = pd.DataFrame(self.training_history)
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(history_df['timestamp'], history_df['train_score'], 'b-o', label='训练得分')
        plt.plot(history_df['timestamp'], history_df['test_score'], 'r-s', label='测试得分')
        plt.xlabel('训练时间')
        plt.ylabel('得分')
        plt.title('训练历史')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.subplot(1, 2, 2)
        plt.bar(range(len(history_df)), history_df['n_samples'])
        plt.xlabel('训练轮次')
        plt.ylabel('样本数量')
        plt.title('训练样本数量')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.show()


def run_demo():
    """运行演示"""
    print("随机森林足球预测系统演示")
    print("="*50)
    
    # 创建分类预测器
    predictor = FootballRandomForestPredictor(model_type='classifier')
    
    # 准备数据
    print("准备数据...")
    X, y = predictor.prepare_synthetic_data(n_samples=3000)
    
    # 训练模型
    print("训练模型...")
    evaluation = predictor.train_model(X, y, test_size=0.2, optimize_params=True)
    
    # 评估模型
    print("评估模型...")
    predictor.evaluate_model(evaluation)
    
    # 示例预测
    print("\n示例预测:")
    example_match = {
        'home_team_strength': 0.8,
        'away_team_strength': 0.6,
        'strength_difference': 0.2,
        'home_recent_form': 0.9,
        'away_recent_form': 0.5,
        'form_difference': 0.4,
        'home_attack_power': 0.7,
        'away_attack_power': 0.5,
        'home_defense_strength': 0.6,
        'away_defense_strength': 0.4,
        'home_advantage': 0.2,
        'home_injury_impact': 0.1,
        'away_injury_impact': 0.2,
        'head_to_head_record': 0.6,
        'match_importance': 0.7,
        'weather_impact': 0.05,
        'fatigue_factor': 0.1,
        'attack_defense_ratio': 0.7 / 0.4,
        'defense_attack_ratio': 0.6 / 0.5
    }
    
    prediction, probabilities = predictor.predict_match(example_match)
    
    result_map = {0: '客队胜', 1: '平局', 2: '主队胜'}
    print(f"预测结果: {result_map[prediction]}")
    if probabilities is not None:
        print(f"概率分布: 客队胜={probabilities[0][0]:.2%}, 平局={probabilities[0][1]:.2%}, 主队胜={probabilities[0][2]:.2%}")
    
    # 保存模型
    predictor.save_model("demo_football_model.pkl")
    
    print("\n演示完成!")


if __name__ == "__main__":
    run_demo()