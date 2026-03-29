@echo off
echo ========================================
echo 个人足球分析系统 - 完整安装
echo ========================================
echo.

echo [1/6] 创建项目目录结构...
mkdir football-analysis 2>nul
cd football-analysis
mkdir data 2>nul
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir data\models 2>nul
mkdir reports 2>nul
mkdir reports\visualizations 2>nul
mkdir reports\predictions 2>nul
mkdir scripts 2>nul

echo [2/6] 复制分析脚本...
copy ..\football_analysis_starter.py scripts\
copy ..\auto_football_report.py scripts\
copy ..\test_api.py scripts\

echo [3/6] 创建配置文件...
echo # 足球分析系统配置 > config.py
echo. >> config.py
echo API_CONFIG = { >> config.py
echo     'football_data': { >> config.py
echo         'api_key': '3d6575aa9dd54fb1aa460e194fafdef3', >> config.py
echo         'base_url': 'https://api.football-data.org/v4' >> config.py
echo     } >> config.py
echo } >> config.py
echo. >> config.py
echo ANALYSIS_CONFIG = { >> config.py
echo     'leagues': ['PL', 'PD', 'SA', 'BL1', 'FL1', 'CL'], >> config.py
echo     'update_interval': 3600, >> config.py
echo     'prediction_model': 'logistic_regression', >> config.py
echo     'data_retention_days': 30 >> config.py
echo } >> config.py

echo [4/6] 创建每日分析脚本...
echo #!/usr/bin/env python3 > daily_analysis.py
echo """ >> daily_analysis.py
echo 每日自动分析脚本 >> daily_analysis.py
echo """ >> daily_analysis.py
echo import sys >> daily_analysis.py
echo import os >> daily_analysis.py
echo sys.path.append(os.path.dirname(os.path.abspath(__file__))) >> daily_analysis.py
echo. >> daily_analysis.py
echo from datetime import datetime >> daily_analysis.py
echo import pandas as pd >> daily_analysis.py
echo from scripts.auto_football_report import AutoFootballReporter >> daily_analysis.py
echo. >> daily_analysis.py
echo def main(): >> daily_analysis.py
echo     print(f"开始每日分析 - {datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S')}") >> daily_analysis.py
echo. >> daily_analysis.py
echo     # 初始化分析器 >> daily_analysis.py
echo     api_key = "3d6575aa9dd54fb1aa460e194fafdef3" >> daily_analysis.py
echo     reporter = AutoFootballReporter(api_key) >> daily_analysis.py
echo. >> daily_analysis.py
echo     # 生成报告 >> daily_analysis.py
echo     reporter.generate_api_usage_report() >> daily_analysis.py
echo     reporter.generate_premier_league_report() >> daily_analysis.py
echo     reporter.generate_todays_matches_report() >> daily_analysis.py
echo     reporter.generate_top_teams_analysis() >> daily_analysis.py
echo     reporter.generate_prediction_insights() >> daily_analysis.py
echo. >> daily_analysis.py
echo     # 保存报告 >> daily_analysis.py
echo     filename = reporter.save_report(f"reports\daily_report_{datetime.now().strftime('%%Y%%m%%d')}.txt") >> daily_analysis.py
echo     print(f"报告已保存: {filename}") >> daily_analysis.py
echo. >> daily_analysis.py
echo if __name__ == "__main__": >> daily_analysis.py
echo     main() >> daily_analysis.py

echo [5/6] 创建启动脚本...
echo @echo off > start_system.bat
echo echo 启动足球分析系统... >> start_system.bat
echo echo ======================================== >> start_system.bat
echo echo. >> start_system.bat
echo echo 请选择操作: >> start_system.bat
echo echo 1. 生成今日分析报告 >> start_system.bat
echo echo 2. 启动交互式分析 >> start_system.bat
echo echo 3. 启动Jupyter Notebook >> start_system.bat
echo echo 4. 查看最新报告 >> start_system.bat
echo echo 5. 退出 >> start_system.bat
echo echo. >> start_system.bat
echo set /p choice="请输入选项 (1-5): " >> start_system.bat
echo. >> start_system.bat
echo if "%%choice%%"=="1" ( >> start_system.bat
echo     python daily_analysis.py >> start_system.bat
echo     pause >> start_system.bat
echo     start_system.bat >> start_system.bat
echo ) >> start_system.bat
echo. >> start_system.bat
echo if "%%choice%%"=="2" ( >> start_system.bat
echo     python scripts\football_analysis_starter.py >> start_system.bat
echo     pause >> start_system.bat
echo     start_system.bat >> start_system.bat
echo ) >> start_system.bat
echo. >> start_system.bat
echo if "%%choice%%"=="3" ( >> start_system.bat
echo     jupyter notebook >> start_system.bat
echo ) >> start_system.bat
echo. >> start_system.bat
echo if "%%choice%%"=="4" ( >> start_system.bat
echo     dir reports\*.txt /b /o-d >> start_system.bat
echo     echo. >> start_system.bat
echo     set /p report="请输入要查看的报告文件名: " >> start_system.bat
echo     type reports\%%report%% >> start_system.bat
echo     pause >> start_system.bat
echo     start_system.bat >> start_system.bat
echo ) >> start_system.bat
echo. >> start_system.bat
echo if "%%choice%%"=="5" ( >> start_system.bat
echo     exit >> start_system.bat
echo ) >> start_system.bat

echo [6/6] 创建机器学习预测模型...
echo #!/usr/bin/env python3 > ml_predictor.py
echo """ >> ml_predictor.py
echo 机器学习预测模型 >> ml_predictor.py
echo """ >> ml_predictor.py
echo import pandas as pd >> ml_predictor.py
echo import numpy as np >> ml_predictor.py
echo from sklearn.model_selection import train_test_split >> ml_predictor.py
echo from sklearn.linear_model import LogisticRegression >> ml_predictor.py
echo from sklearn.ensemble import RandomForestClassifier >> ml_predictor.py
echo from sklearn.metrics import accuracy_score >> ml_predictor.py
echo import joblib >> ml_predictor.py
echo from datetime import datetime >> ml_predictor.py
echo. >> ml_predictor.py
echo class FootballPredictor: >> ml_predictor.py
echo     def __init__(self): >> ml_predictor.py
echo         self.models = {} >> ml_predictor.py
echo         self.model_path = "data\models" >> ml_predictor.py
echo. >> ml_predictor.py
echo     def create_sample_data(self): >> ml_predictor.py
echo         """创建示例数据用于演示""" >> ml_predictor.py
echo         print("创建示例数据...") >> ml_predictor.py
echo         # 这里可以替换为真实API数据 >> ml_predictor.py
echo         data = { >> ml_predictor.py
echo             'home_attack': np.random.rand(100) * 2, >> ml_predictor.py
echo             'home_defense': np.random.rand(100) * 2, >> ml_predictor.py
echo             'away_attack': np.random.rand(100) * 2, >> ml_predictor.py
echo             'away_defense': np.random.rand(100) * 2, >> ml_predictor.py
echo             'home_advantage': np.ones(100), >> ml_predictor.py
echo             'result': np.random.choice([0, 1, 2], 100)  # 0:主场负, 1:平, 2:主场胜 >> ml_predictor.py
echo         } >> ml_predictor.py
echo         return pd.DataFrame(data) >> ml_predictor.py
echo. >> ml_predictor.py
echo     def train_models(self, data): >> ml_predictor.py
echo         """训练预测模型""" >> ml_predictor.py
echo         print("训练预测模型...") >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 准备特征和标签 >> ml_predictor.py
echo         X = data[['home_attack', 'home_defense', 'away_attack', 'away_defense', 'home_advantage']] >> ml_predictor.py
echo         y = data['result'] >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 分割数据 >> ml_predictor.py
echo         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 训练逻辑回归模型 >> ml_predictor.py
echo         lr_model = LogisticRegression(max_iter=1000) >> ml_predictor.py
echo         lr_model.fit(X_train, y_train) >> ml_predictor.py
echo         lr_pred = lr_model.predict(X_test) >> ml_predictor.py
echo         lr_accuracy = accuracy_score(y_test, lr_pred) >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 训练随机森林模型 >> ml_predictor.py
echo         rf_model = RandomForestClassifier(n_estimators=100, random_state=42) >> ml_predictor.py
echo         rf_model.fit(X_train, y_train) >> ml_predictor.py
echo         rf_pred = rf_model.predict(X_test) >> ml_predictor.py
echo         rf_accuracy = accuracy_score(y_test, rf_pred) >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 保存模型 >> ml_predictor.py
echo         self.models['logistic_regression'] = { >> ml_predictor.py
echo             'model': lr_model, >> ml_predictor.py
echo             'accuracy': lr_accuracy >> ml_predictor.py
echo         } >> ml_predictor.py
echo. >> ml_predictor.py
echo         self.models['random_forest'] = { >> ml_predictor.py
echo             'model': rf_model, >> ml_predictor.py
echo             'accuracy': rf_accuracy >> ml_predictor.py
echo         } >> ml_predictor.py
echo. >> ml_predictor.py
echo         # 保存到文件 >> ml_predictor.py
echo         joblib.dump(lr_model, f"{self.model_path}\logistic_regression.pkl") >> ml_predictor.py
echo         joblib.dump(rf_model, f"{self.model_path}\random_forest.pkl") >> ml_predictor.py
echo. >> ml_predictor.py
echo         print(f"模型训练完成:") >> ml_predictor.py
echo         print(f"  逻辑回归准确率: {lr_accuracy:.2%}") >> ml_predictor.py
echo         print(f"  随机森林准确率: {rf_accuracy:.2%}") >> ml_predictor.py
echo. >> ml_predictor.py
echo     def predict_match(self, home_stats, away_stats): >> ml_predictor.py
echo         """预测单场比赛""" >> ml_predictor.py
echo         # 这里可以替换为真实数据 >> ml_predictor.py
echo         features = np.array([[ >> ml_predictor.py
echo             home_stats.get('attack', 1.5), >> ml_predictor.py
echo             home_stats.get('defense', 1.0), >> ml_predictor.py
echo             away_stats.get('attack', 1.2), >> ml_predictor.py
echo             away_stats.get('defense', 1.3), >> ml_predictor.py
echo             1.0  # 主场优势 >> ml_predictor.py
echo         ]]) >> ml_predictor.py
echo. >> ml_predictor.py
echo         if 'logistic_regression' in self.models: >> ml_predictor.py
echo             model = self.models['logistic_regression']['model'] >> ml_predictor.py
echo             prediction = model.predict(features)[0] >> ml_predictor.py
echo             probabilities = model.predict_proba(features)[0] >> ml_predictor.py
echo. >> ml_predictor.py
echo             result_map = {0: '客场胜', 1: '平局', 2: '主场胜'} >> ml_predictor.py
echo             return { >> ml_predictor.py
echo                 'prediction': result_map.get(prediction, '未知'), >> ml_predictor.py
echo                 'probabilities': { >> ml_predictor.py
echo                     '客场胜': f"{probabilities[0]:.1%}", >> ml_predictor.py
echo                     '平局': f"{probabilities[1]:.1%}", >> ml_predictor.py
echo                     '主场胜': f"{probabilities[2]:.1%}" >> ml_predictor.py
echo                 }, >> ml_predictor.py
echo                 'model_accuracy': self.models['logistic_regression']['accuracy'] >> ml_predictor.py
echo             } >> ml_predictor.py
echo         return None >> ml_predictor.py
echo. >> ml_predictor.py
echo def main(): >> ml_predictor.py
echo     """主函数""" >> ml_predictor.py
echo     print("="*60) >> ml_predictor.py
echo     print("机器学习足球预测模型") >> ml_predictor.py
echo     print("="*60) >> ml_predictor.py
echo. >> ml_predictor.py
echo     predictor = FootballPredictor() >> ml_predictor.py
echo. >> ml_predictor.py
echo     # 创建示例数据并训练模型 >> ml_predictor.py
echo     data = predictor.create_sample_data() >> ml_predictor.py
echo     predictor.train_models(data) >> ml_predictor.py
echo. >> ml_predictor.py
echo     # 示例预测 >> ml_predictor.py
echo     print("\n示例预测:") >> ml_predictor.py
echo     home_stats = {'attack': 1.8, 'defense': 0.9} >> ml_predictor.py
echo     away_stats = {'attack': 1.5, 'defense': 1.2} >> ml_predictor.py
echo     prediction = predictor.predict_match(home_stats, away_stats) >> ml_predictor.py
echo. >> ml_predictor.py
echo     if prediction: >> ml_predictor.py
echo         print(f"预测结果: {prediction['prediction']}") >> ml_predictor.py
echo         print("概率分布:") >> ml_predictor.py
echo         for outcome, prob in prediction['probabilities'].items(): >> ml_predictor.py
echo             print(f"  {outcome}: {prob}") >> ml_predictor.py
echo         print(f"模型准确率: {prediction['model_accuracy']:.2%}") >> ml_predictor.py
echo. >> ml_predictor.py
echo     print("\n提示: 使用真实比赛数据替换示例数据可获得更准确的预测") >> ml_predictor.py
echo. >> ml_predictor.py
echo if __name__ == "__main__": >> ml_predictor.py
echo     main() >> ml_predictor.py

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 系统已安装在: %CD%
echo.
echo 启动系统: start_system.bat
echo 生成报告: python daily_analysis.py
echo 机器学习预测: python ml_predictor.py
echo.
echo 按任意键退出...
pause >nul