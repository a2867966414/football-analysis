#!/usr/bin/env python3
"""
测试足球分析系统
"""

import sys
import os

# 添加football-analysis目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'football-analysis'))

def test_all_components():
    """测试所有组件"""
    print("="*60)
    print("测试足球分析系统")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    # 测试1: 配置文件
    print("\n1. 测试配置文件...")
    try:
        import config
        print("   [OK] config.py 加载成功")
        print(f"   API密钥: {config.API_CONFIG['football_data']['api_key'][:8]}...")
        print(f"   关注联赛: {config.ANALYSIS_CONFIG['leagues']}")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] config.py 加载失败: {str(e)}")
        tests_failed += 1
    
    # 测试2: API连接
    print("\n2. 测试API连接...")
    try:
        from scripts.test_api import test_api_connection
        if test_api_connection():
            print("   [OK] API连接测试成功")
            tests_passed += 1
        else:
            print("   [ERROR] API连接测试失败")
            tests_failed += 1
    except Exception as e:
        print(f"   [ERROR] API测试失败: {str(e)}")
        tests_failed += 1
    
    # 测试3: 分析脚本
    print("\n3. 测试分析脚本...")
    try:
        from scripts.football_analysis_starter import FootballAnalyzer
        analyzer = FootballAnalyzer()
        print("   [OK] 分析器初始化成功")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] 分析器初始化失败: {str(e)}")
        tests_failed += 1
    
    # 测试4: 机器学习模型
    print("\n4. 测试机器学习模型...")
    try:
        import ml_predictor
        print("   [OK] 机器学习模块加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"   [WARN] 机器学习模块加载警告: {str(e)}")
        print("   (这可能是正常的，如果没有安装scikit-learn)")
    
    # 测试5: 目录结构
    print("\n5. 测试目录结构...")
    required_dirs = ['data', 'data/raw', 'data/processed', 'data/models', 
                    'reports', 'reports/visualizations', 'reports/predictions',
                    'scripts']
    
    for dir_path in required_dirs:
        full_path = os.path.join('football-analysis', dir_path)
        if os.path.exists(full_path):
            print(f"   [OK] 目录存在: {dir_path}")
        else:
            print(f"   [ERROR] 目录缺失: {dir_path}")
            tests_failed += 1
    
    # 测试6: 必要文件
    print("\n6. 测试必要文件...")
    required_files = ['config.py', 'daily_analysis.py', 'ml_predictor.py', 
                     'README.md', 'start_system.bat',
                     'scripts/football_analysis_starter.py', 'scripts/test_api.py']
    
    for file_path in required_files:
        full_path = os.path.join('football-analysis', file_path)
        if os.path.exists(full_path):
            print(f"   [OK] 文件存在: {file_path}")
            tests_passed += 1
        else:
            print(f"   [ERROR] 文件缺失: {file_path}")
            tests_failed += 1
    
    # 总结
    print("\n" + "="*60)
    print("测试结果总结")
    print("="*60)
    print(f"通过测试: {tests_passed}")
    print(f"失败测试: {tests_failed}")
    print(f"总测试数: {tests_passed + tests_failed}")
    
    if tests_failed == 0:
        print("\n[SUCCESS] 所有测试通过！系统安装成功！")
        print("\n下一步操作:")
        print("1. 进入足球分析目录: cd football-analysis")
        print("2. 运行每日分析: python daily_analysis.py")
        print("3. 或运行启动脚本: start_system.bat")
    else:
        print(f"\n[WARNING] 有 {tests_failed} 个测试失败，请检查安装")
    
    print("="*60)

if __name__ == "__main__":
    test_all_components()