#!/usr/bin/env python3
"""
自动足球分析报告
生成完整的分析报告，无需交互
"""

import requests
import json
from datetime import datetime, timedelta

class AutoFootballReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': self.api_key}
        self.report = []
        
    def add_to_report(self, section_title, content):
        """添加内容到报告"""
        self.report.append(f"\n{'='*60}")
        self.report.append(section_title)
        self.report.append('='*60)
        if isinstance(content, list):
            self.report.extend(content)
        else:
            self.report.append(content)
    
    def generate_premier_league_report(self):
        """生成英超报告"""
        try:
            # 获取英超积分榜
            response = requests.get(
                f"{self.base_url}/competitions/PL/standings",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                standings = data.get('standings', [])
                
                if standings and len(standings) > 0:
                    table = standings[0].get('table', [])
                    
                    report_lines = []
                    report_lines.append(f"数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    report_lines.append(f"球队总数: {len(table)}")
                    report_lines.append("")
                    report_lines.append("积分榜前10名:")
                    report_lines.append("-"*70)
                    report_lines.append("排名 | 球队 | 场次 | 胜 | 平 | 负 | 进球 | 失球 | 积分 | 近5场")
                    report_lines.append("-"*70)
                    
                    for i, team in enumerate(table[:10]):
                        position = team.get('position', 'N/A')
                        team_name = team.get('team', {}).get('name', '未知')
                        played = team.get('playedGames', 0)
                        won = team.get('won', 0)
                        draw = team.get('draw', 0)
                        lost = team.get('lost', 0)
                        goals_for = team.get('goalsFor', 0)
                        goals_against = team.get('goalsAgainst', 0)
                        points = team.get('points', 0)
                        form = team.get('form', '-----')
                        
                        report_lines.append(f"{position:4} | {team_name:20} | {played:4} | {won:2} | {draw:2} | {lost:2} | {goals_for:4} | {goals_against:6} | {points:4} | {form}")
                    
                    # 分析
                    if len(table) >= 3:
                        leader = table[0]
                        second = table[1]
                        point_gap = leader.get('points', 0) - second.get('points', 0)
                        
                        report_lines.append("")
                        report_lines.append("[争冠形势分析]")
                        report_lines.append(f"  领头羊: {leader.get('team', {}).get('name')} ({leader.get('points')}分)")
                        report_lines.append(f"  第二名: {second.get('team', {}).get('name')} ({second.get('points')}分)")
                        report_lines.append(f"  积分差距: {point_gap}分")
                        
                        if point_gap >= 10:
                            report_lines.append("  分析: 争冠悬念不大")
                        elif point_gap >= 5:
                            report_lines.append("  分析: 争冠形势明朗")
                        else:
                            report_lines.append("  分析: 争冠激烈")
                    
                    self.add_to_report("英超联赛分析报告", report_lines)
                    return True
                    
            return False
            
        except Exception as e:
            self.add_to_report("英超联赛分析报告", [f"生成报告时出错: {str(e)}"])
            return False
    
    def generate_todays_matches_report(self):
        """生成今日比赛报告"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            response = requests.get(
                f"{self.base_url}/matches",
                headers=self.headers,
                params={
                    'dateFrom': today,
                    'dateTo': tomorrow,
                    'competitions': 'PL,CL,BL1,SA,PD,FL1'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                report_lines = []
                report_lines.append(f"查询时间: {today} 至 {tomorrow}")
                report_lines.append(f"找到比赛: {len(matches)} 场")
                report_lines.append("")
                
                if matches:
                    # 按联赛分组
                    matches_by_comp = {}
                    for match in matches:
                        comp = match.get('competition', {}).get('name', '其他')
                        if comp not in matches_by_comp:
                            matches_by_comp[comp] = []
                        matches_by_comp[comp].append(match)
                    
                    for comp, comp_matches in matches_by_comp.items():
                        report_lines.append(f"{comp} ({len(comp_matches)}场):")
                        for match in comp_matches:
                            home = match.get('homeTeam', {}).get('name', '未知')
                            away = match.get('awayTeam', {}).get('name', '未知')
                            time = match.get('utcDate', '未知')
                            status = match.get('status', 'SCHEDULED')
                            
                            if 'T' in time:
                                time = time.split('T')[1][:5] + " UTC"
                            
                            status_map = {
                                'SCHEDULED': '⏳ 未开始',
                                'LIVE': '🔥 进行中',
                                'IN_PLAY': '🔥 进行中',
                                'PAUSED': '⏸️ 暂停',
                                'FINISHED': '✅ 已结束',
                                'POSTPONED': '❌ 延期',
                                'CANCELLED': '❌ 取消'
                            }
                            
                            status_text = status_map.get(status, status)
                            report_lines.append(f"  {home} vs {away} - {time} {status_text}")
                        report_lines.append("")
                else:
                    report_lines.append("今日无重要比赛安排")
                
                self.add_to_report("今日比赛安排", report_lines)
                return True
                
            return False
            
        except Exception as e:
            self.add_to_report("今日比赛安排", [f"生成报告时出错: {str(e)}"])
            return False
    
    def generate_top_teams_analysis(self):
        """生成顶级球队分析"""
        try:
            # 获取英超前4名球队
            response = requests.get(
                f"{self.base_url}/competitions/PL/standings",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                standings = data.get('standings', [])
                
                if standings:
                    table = standings[0].get('table', [])
                    top_teams = table[:4]  # 前4名
                    
                    report_lines = []
                    report_lines.append("英超前4名球队深度分析")
                    report_lines.append("")
                    
                    for team_data in top_teams:
                        team_name = team_data.get('team', {}).get('name')
                        team_id = team_data.get('team', {}).get('id')
                        
                        if team_id:
                            # 获取球队详情
                            team_response = requests.get(
                                f"{self.base_url}/teams/{team_id}",
                                headers=self.headers,
                                timeout=10
                            )
                            
                            if team_response.status_code == 200:
                                team_info = team_response.json()
                                
                                report_lines.append(f"【{team_name}】")
                                report_lines.append(f"  排名: {team_data.get('position')}")
                                report_lines.append(f"  积分: {team_data.get('points')}")
                                report_lines.append(f"  胜/平/负: {team_data.get('won')}/{team_data.get('draw')}/{team_data.get('lost')}")
                                report_lines.append(f"  进球/失球: {team_data.get('goalsFor')}/{team_data.get('goalsAgainst')}")
                                report_lines.append(f"  净胜球: {team_data.get('goalsFor') - team_data.get('goalsAgainst')}")
                                report_lines.append(f"  近期状态: {team_data.get('form', '-----')}")
                                
                                # 计算场均数据
                                played = team_data.get('playedGames', 1)
                                avg_goals_for = team_data.get('goalsFor', 0) / played
                                avg_goals_against = team_data.get('goalsAgainst', 0) / played
                                win_rate = team_data.get('won', 0) / played * 100
                                
                                report_lines.append(f"  场均进球: {avg_goals_for:.2f}")
                                report_lines.append(f"  场均失球: {avg_goals_against:.2f}")
                                report_lines.append(f"  胜率: {win_rate:.1f}%")
                                
                                # 实力评估
                                strength = ""
                                if avg_goals_for > 2.0 and avg_goals_against < 1.0:
                                    strength = "攻防俱佳"
                                elif avg_goals_for > 1.5:
                                    strength = "攻击力强"
                                elif avg_goals_against < 1.0:
                                    strength = "防守稳固"
                                else:
                                    strength = "表现均衡"
                                
                                report_lines.append(f"  实力评估: {strength}")
                                report_lines.append("")
                    
                    self.add_to_report("顶级球队分析", report_lines)
                    return True
                    
            return False
            
        except Exception as e:
            self.add_to_report("顶级球队分析", [f"生成报告时出错: {str(e)}"])
            return False
    
    def generate_prediction_insights(self):
        """生成预测洞察"""
        report_lines = []
        report_lines.append("足球预测关键因素分析")
        report_lines.append("")
        report_lines.append("1. 📊 球队状态因素:")
        report_lines.append("   - 近期战绩 (最近5-10场比赛)")
        report_lines.append("   - 主场/客场表现差异")
        report_lines.append("   - 对阵历史记录")
        report_lines.append("")
        report_lines.append("2. ⚽ 战术因素:")
        report_lines.append("   - 进攻效率 (射门转化率)")
        report_lines.append("   - 防守稳定性")
        report_lines.append("   - 控球率和传球成功率")
        report_lines.append("")
        report_lines.append("3. 👥 人员因素:")
        report_lines.append("   - 关键球员伤病")
        report_lines.append("   - 停赛情况")
        report_lines.append("   - 阵容轮换")
        report_lines.append("")
        report_lines.append("4. 🏟️ 外部因素:")
        report_lines.append("   - 天气条件")
        report_lines.append("   - 球迷支持")
        report_lines.append("   - 赛程密集度")
        report_lines.append("")
        report_lines.append("5. 💡 预测建议:")
        report_lines.append("   - 关注球队近期状态而非赛季初表现")
        report_lines.append("   - 主场优势在足球中非常重要")
        report_lines.append("   - 强队对阵弱队时，大比分概率较高")
        report_lines.append("   - 德比战往往难以预测")
        
        self.add_to_report("预测洞察与分析", report_lines)
        return True
    
    def generate_api_usage_report(self):
        """生成API使用报告"""
        try:
            # 测试请求以获取API限制信息
            response = requests.get(f"{self.base_url}/competitions/PL", headers=self.headers, timeout=5)
            
            report_lines = []
            report_lines.append("API使用状态报告")
            report_lines.append("")
            report_lines.append(f"API密钥: {self.api_key[:8]}...{self.api_key[-4:]}")
            report_lines.append(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append(f"连接状态: {'成功' if response.status_code == 200 else '失败'}")
            report_lines.append(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                # 尝试获取API限制信息
                if 'X-Requests-Available' in response.headers:
                    available = response.headers.get('X-Requests-Available', '未知')
                    reset = response.headers.get('X-RequestCounter-Reset', '未知')
                    report_lines.append(f"剩余请求次数: {available}")
                    report_lines.append(f"重置时间(秒): {reset}")
                    
                    # 使用建议
                    report_lines.append("")
                    report_lines.append("💡 使用建议:")
                    if available.isdigit() and int(available) < 50:
                        report_lines.append("  - 剩余请求次数较少，请合理使用")
                    else:
                        report_lines.append("  - API使用状态良好")
                    report_lines.append("  - 建议缓存数据以减少API调用")
                    report_lines.append("  - 定期检查API限制")
                else:
                    report_lines.append("API限制信息: 未提供")
            elif response.status_code == 403:
                report_lines.append("⚠️ 警告: API密钥可能无效或已过期")
            elif response.status_code == 429:
                report_lines.append("⚠️ 警告: 请求过于频繁，请稍后重试")
            
            self.add_to_report("API状态报告", report_lines)
            return True
            
        except Exception as e:
            self.add_to_report("API状态报告", [f"生成报告时出错: {str(e)}"])
            return False
    
    def save_report(self, filename=None):
        """保存报告到文件"""
        if filename is None:
            filename = f"football_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("个人足球分析系统 - 完整报告\n")
            f.write("="*70 + "\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"API密钥: {self.api_key[:8]}...{self.api_key[-4:]}\n")
            f.write("\n")
            
            for line in self.report:
                f.write(line + "\n")
        
        return filename
    
    def print_report(self):
        """打印报告到控制台"""
        print("="*70)
        print("个人足球分析系统 - 完整报告")
        print("="*70)
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API密钥: {self.api_key[:8]}...{self.api_key[-4:]}")
        print()
        
        for line in self.report:
            print(line)

def main():
    """主函数"""
    api_key = "3d6575aa9dd54fb1aa460e194fafdef3"
    
    print("正在生成足球分析报告...")
    print("这可能需要几秒钟时间...")
    print()
    
    reporter = AutoFootballReporter(api_key)
    
    # 生成各个部分的报告
    print("1. 检查API连接状态...")
    reporter.generate_api_usage_report()
    
    print("2. 生成英超联赛分析...")
    reporter.generate_premier_league_report()
    
    print("3. 生成今日比赛安排...")
    reporter.generate_todays_matches_report()
    
    print("4. 分析顶级球队表现...")
    reporter.generate_top_teams_analysis()
    
    print("5. 生成预测洞察...")
    reporter.generate_prediction_insights()
    
    # 保存报告
    filename = reporter.save_report()
    
    # 打印报告摘要
    reporter.print_report()
    
    print("\n" + "="*70)
    print(f"✅ 报告已生成并保存到: {filename}")
    print("="*70)
    print("\n📋 报告包含:")
    print("  1. API使用状态")
    print("  2. 英超积分榜分析")
    print("  3. 今日比赛安排")
    print("  4. 顶级球队深度分析")
    print("  5. 预测关键因素洞察")
    print("\n🚀 下一步建议:")
    print("  1. 查看生成的报告文件")
    print("  2. 安装pandas等库进行更深入分析")
    print("  3. 设置定时任务自动生成报告")
    print("  4. 探索更多免费足球数据源")
    print("="*70)

if __name__ == "__main__":
    main()