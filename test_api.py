#!/usr/bin/env python3
"""
测试足球数据API连接
"""

import requests
import json
from datetime import datetime

def test_api_connection():
    """测试API连接"""
    api_key = "3d6575aa9dd54fb1aa460e194fafdef3"
    base_url = "https://api.football-data.org/v4"
    
    headers = {
        'X-Auth-Token': api_key,
        'User-Agent': 'FootballAnalysis/1.0'
    }
    
    print("=" * 60)
    print("测试足球数据API连接")
    print("=" * 60)
    print(f"API密钥: {api_key[:8]}...{api_key[-4:]}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试1: 获取可用联赛
    print("1. 测试联赛数据获取...")
    try:
        response = requests.get(f"{base_url}/competitions", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            competitions = data.get('competitions', [])
            
            print(f"   [OK] 连接成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   找到联赛数量: {len(competitions)}")
            
            # 显示主要联赛
            major_leagues = ['PL', 'PD', 'SA', 'BL1', 'FL1', 'CL']
            major = [c for c in competitions if c.get('code') in major_leagues]
            
            print(f"   主要联赛 ({len(major)}个):")
            for comp in major[:5]:  # 显示前5个
                print(f"     - {comp.get('name', '未知')} ({comp.get('code', 'N/A')})")
            
            # 测试2: 获取英超信息
            print("\n2. 测试具体联赛数据...")
            pl_competition = next((c for c in competitions if c.get('code') == 'PL'), None)
            if pl_competition:
                comp_id = pl_competition.get('id')
                comp_response = requests.get(f"{base_url}/competitions/{comp_id}", headers=headers, timeout=10)
                if comp_response.status_code == 200:
                    comp_data = comp_response.json()
                    print(f"   [OK] 英超数据获取成功")
                    print(f"   联赛: {comp_data.get('name', '未知')}")
                    print(f"   当前赛季: {comp_data.get('currentSeason', {}).get('startDate', '未知')} 至 {comp_data.get('currentSeason', {}).get('endDate', '未知')}")
            
            # 测试3: 检查API限制
            print("\n3. 检查API限制...")
            if 'X-Requests-Available' in response.headers:
                available = response.headers.get('X-Requests-Available', '未知')
                reset = response.headers.get('X-RequestCounter-Reset', '未知')
                print(f"   剩余请求次数: {available}")
                print(f"   重置时间(秒): {reset}")
            
            return True
            
        elif response.status_code == 403:
            print(f"   [ERROR] 连接失败: API密钥无效或已过期 (状态码: {response.status_code})")
            print(f"   响应: {response.text[:200]}")
            return False
        elif response.status_code == 429:
            print(f"   [WARN] 请求过多，请稍后重试 (状态码: {response.status_code})")
            return False
        else:
            print(f"   [ERROR] 连接失败 (状态码: {response.status_code})")
            print(f"   响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("   [ERROR] 连接超时，请检查网络")
        return False
    except requests.exceptions.ConnectionError:
        print("   [ERROR] 连接错误，无法访问API服务器")
        return False
    except Exception as e:
        print(f"   [ERROR] 未知错误: {str(e)}")
        return False

def get_quick_analysis():
    """快速分析演示"""
    print("\n" + "=" * 60)
    print("快速分析演示")
    print("=" * 60)
    
    api_key = "3d6575aa9dd54fb1aa460e194fafdef3"
    base_url = "https://api.football-data.org/v4"
    headers = {'X-Auth-Token': api_key}
    
    # 获取英超比赛
    print("\n获取今日英超比赛...")
    try:
        # 获取英超ID
        comp_response = requests.get(f"{base_url}/competitions/PL", headers=headers, timeout=10)
        if comp_response.status_code == 200:
            comp_data = comp_response.json()
            current_season = comp_data.get('currentSeason', {}).get('id')
            
            if current_season:
                # 获取比赛
                matches_response = requests.get(
                    f"{base_url}/competitions/PL/matches",
                    headers=headers,
                    params={'season': current_season, 'status': 'SCHEDULED'},
                    timeout=10
                )
                
                if matches_response.status_code == 200:
                    matches_data = matches_response.json()
                    matches = matches_data.get('matches', [])
                    
                    if matches:
                        print(f"找到 {len(matches)} 场即将进行的比赛:")
                        for i, match in enumerate(matches[:3]):  # 显示前3场
                            home = match.get('homeTeam', {}).get('name', '未知')
                            away = match.get('awayTeam', {}).get('name', '未知')
                            date = match.get('utcDate', '未知')
                            print(f"  {i+1}. {home} vs {away}")
                            print(f"     时间: {date}")
                    else:
                        print("今日无英超比赛")
                else:
                    print("无法获取比赛数据")
            else:
                print("无法获取当前赛季信息")
        else:
            print("无法获取英超信息")
            
    except Exception as e:
        print(f"分析出错: {str(e)}")

def main():
    """主函数"""
    # 测试API连接
    if test_api_connection():
        # 如果连接成功，进行快速分析
        get_quick_analysis()
    
    print("\n" + "=" * 60)
    print("下一步操作:")
    print("1. 安装完整分析包: pip install pandas numpy matplotlib seaborn")
    print("2. 运行完整分析: python football_analysis_starter.py")
    print("3. 查看API文档: https://www.football-data.org/documentation/api")
    print("=" * 60)

if __name__ == "__main__":
    main()