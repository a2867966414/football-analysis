/**
 * 专业足球AI分析系统 - 前端JavaScript
 * 现代化UI交互和数据可视化
 */

class ProfessionalFootballUI {
    constructor() {
        this.currentTab = 'dashboard';
        this.lastUpdate = new Date();
        this.autoRefreshInterval = null;
        this.charts = {};
    }

    // 初始化系统
    async init() {
        console.log('初始化专业足球AI分析系统...');
        
        // 设置事件监听器
        this.setupEventListeners();
        
        // 检查系统状态
        await this.checkSystemStatus();
        
        // 加载初始数据
        await this.loadDashboardData();
        
        // 启动自动刷新
        this.startAutoRefresh();
        
        // 更新最后更新时间
        this.updateLastUpdateTime();
        
        console.log('系统初始化完成');
    }

    // 设置事件监听器
    setupEventListeners() {
        // 标签页切换
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });

        // 侧边栏导航
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const tab = e.target.closest('.nav-link').dataset.tab;
                this.switchTab(tab);
            });
        });

        // 刷新按钮
        document.querySelectorAll('[onclick*="refresh"]').forEach(button => {
            button.addEventListener('click', () => this.refreshData());
        });

        // 搜索功能
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch(e.target.value);
                }
            });
        }
    }

    // 切换标签页
    switchTab(tabName) {
        if (this.currentTab === tabName) return;

        // 更新当前标签页
        this.currentTab = tabName;

        // 更新标签页按钮状态
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.toggle('active', button.dataset.tab === tabName);
        });

        // 更新侧边栏导航状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.tab === tabName);
        });

        // 显示对应的标签页内容
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}Tab`);
        });

        // 加载对应标签页的数据
        this.loadTabData(tabName);

        // 显示通知
        this.showNotification(`切换到${this.getTabName(tabName)}`, 'info');
    }

    // 获取标签页名称
    getTabName(tab) {
        const tabNames = {
            'dashboard': '仪表板',
            'live': '实时监控',
            'predictions': 'AI预测',
            'value': '价值检测',
            'worldcup': '世界杯2026',
            'analytics': '数据分析',
            'settings': '系统设置'
        };
        return tabNames[tab] || tab;
    }

    // 检查系统状态
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/system/status');
            if (response.ok) {
                const data = await response.json();
                console.log('系统状态:', data);
                this.updateSystemStatus(data);
                return true;
            }
        } catch (error) {
            console.error('检查系统状态失败:', error);
            this.showNotification('系统连接失败', 'error');
            return false;
        }
    }

    // 更新系统状态显示
    updateSystemStatus(data) {
        // 更新版本信息
        const versionElement = document.querySelector('.version-info');
        if (versionElement) {
            versionElement.textContent = `v${data.version}`;
        }

        // 更新性能指标
        const accuracyElement = document.getElementById('predictionAccuracy');
        if (accuracyElement && data.performance) {
            accuracyElement.textContent = `${data.performance.accuracy}%`;
        }
    }

    // 加载仪表板数据
    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard/data');
            if (response.ok) {
                const data = await response.json();
                this.updateDashboard(data);
                this.lastUpdate = new Date();
                this.updateLastUpdateTime();
            }
        } catch (error) {
            console.error('加载仪表板数据失败:', error);
            this.showNotification('数据加载失败', 'error');
        }
    }

    // 更新仪表板
    updateDashboard(data) {
        // 更新实时比赛数量
        const liveCountElement = document.getElementById('liveMatchCount');
        if (liveCountElement && data.live_matches) {
            liveCountElement.textContent = data.live_matches.count;
        }

        // 更新价值机会数量
        const valueCountElement = document.getElementById('valueOpportunities');
        if (valueCountElement && data.value_opportunities) {
            valueCountElement.textContent = data.value_opportunities.count;
        }

        // 更新活跃用户数量
        const userCountElement = document.getElementById('activeUsers');
        if (userCountElement && data.user_stats) {
            userCountElement.textContent = data.user_stats.active_users.toLocaleString();
        }

        // 更新预测准确率
        const accuracyElement = document.getElementById('predictionAccuracy');
        if (accuracyElement && data.ai_predictions) {
            accuracyElement.textContent = `${data.ai_predictions.accuracy}%`;
        }

        // 更新实时比赛列表
        this.updateLiveMatches(data.live_matches?.matches || []);

        // 更新价值机会列表
        this.updateValueOpportunities(data.value_opportunities?.opportunities || []);

        // 更新世界杯分析
        this.updateWorldCupAnalysis(data.world_cup || {});

        // 更新AI预测结果
        if (data.ai_predictions?.featured) {
            this.updatePredictionResult(data.ai_predictions.featured);
        }
    }

    // 更新实时比赛列表
    updateLiveMatches(matches) {
        const container = document.getElementById('liveMatchesContainer');
        if (!container) return;

        if (matches.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-calendar-x text-muted" style="font-size: 2rem;"></i>
                    <p class="mt-2 text-muted">当前没有进行中的比赛</p>
                </div>`;
            return;
        }

        let html = '';
        matches.forEach(match => {
            html += `
            <div class="live-match-card">
                <div class="match-header">
                    <span class="match-competition">${match.competition}</span>
                    <span class="live-badge">LIVE ${match.minute}'</span>
                </div>
                <div class="match-teams">
                    <div class="team">
                        <div class="team-name">${match.home_team}</div>
                        <div class="team-label">主队</div>
                    </div>
                    <div class="match-score">${match.score}</div>
                    <div class="team">
                        <div class="team-name">${match.away_team}</div>
                        <div class="team-label">客队</div>
                    </div>
                </div>
                <div class="match-stats">
                    <span>控球: ${match.possession}%</span>
                    <span>射门: ${match.shots}</span>
                    <span>事件: ${match.events}</span>
                </div>
            </div>`;
        });

        container.innerHTML = html;
    }

    // 更新价值机会列表
    updateValueOpportunities(opportunities) {
        const container = document.getElementById('valueOpportunitiesContainer');
        if (!container) return;

        if (opportunities.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-search text-muted" style="font-size: 2rem;"></i>
                    <p class="mt-2 text-muted">当前没有检测到价值机会</p>
                </div>`;
            return;
        }

        let html = '';
        opportunities.forEach(opp => {
            const riskColor = opp.risk_level === 'high' ? 'danger' : 
                            opp.risk_level === 'medium' ? 'warning' : 'success';
            
            html += `
            <div class="opportunity-card">
                <div class="opportunity-header">
                    <span class="opportunity-type">${opp.type.replace('_opportunity', '')}</span>
                    <span class="opportunity-confidence">置信度: ${Math.round(opp.confidence * 100)}%</span>
                </div>
                <div class="opportunity-value text-${riskColor}">${opp.value}</div>
                <p class="text-muted mb-2">${opp.description}</p>
                <div class="flex justify-between items-center">
                    <span class="text-sm">${opp.match}</span>
                    <span class="text-sm text-muted">${new Date(opp.timestamp).toLocaleTimeString()}</span>
                </div>
            </div>`;
        });

        container.innerHTML = html;
    }

    // 更新世界杯分析
    updateWorldCupAnalysis(data) {
        const container = document.getElementById('worldCupContainer');
        if (!container || !data.probabilities) return;

        let html = `
            <div class="mb-3">
                <h4 class="text-center mb-2">${data.tournament}</h4>
                <p class="text-center text-muted text-sm">${data.location} • ${data.teams_count}支球队 • ${data.matches_count}场比赛</p>
            </div>`;

        // 夺冠概率
        html += '<h5 class="mb-2">夺冠概率排名</h5>';
        data.probabilities.forEach(team => {
            const trendIcon = team.trend === 'rising' ? '↗️' : 
                            team.trend === 'falling' ? '↘️' : '➡️';
            
            html += `
            <div class="probability-bar">
                <div class="probability-label">
                    <span>${team.flag} ${team.team}</span>
                    <span>${team.probability}% ${trendIcon}</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill bar-home" style="width: ${team.probability}%"></div>
                </div>
            </div>`;
        });

        // 黑马球队
        if (data.dark_horses && data.dark_horses.length > 0) {
            html += '<h5 class="mt-3 mb-2">黑马球队</h5>';
            data.dark_horses.forEach(horse => {
                html += `<p class="text-sm mb-1">• ${horse.team}: ${horse.reason}</p>`;
            });
        }

        container.innerHTML = html;
    }

    // 运行AI预测
    async runPrediction() {
        const homeTeam = document.getElementById('homeTeam')?.value || 'Manchester United';
        const awayTeam = document.getElementById('awayTeam')?.value || 'Liverpool';

        if (!homeTeam || !awayTeam) {
            this.showNotification('请输入球队名称', 'warning');
            return;
        }

        this.showNotification('正在运行AI预测...', 'info');

        try {
            const response = await fetch('/api/ai/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    home_team: homeTeam,
                    away_team: awayTeam
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.updatePredictionResult(data.prediction);
                this.showNotification('预测完成', 'success');
            }
        } catch (error) {
            console.error('预测失败:', error);
            this.showNotification('预测失败', 'error');
        }
    }

    // 更新预测结果
    updatePredictionResult(prediction) {
        const container = document.getElementById('predictionResult');
        if (!container || !prediction) return;

        const { home_team, away_team, probabilities, confidence, analysis, recommendation } = prediction;

        let html = `
            <h5 class="text-center mb-3">${home_team} vs ${away_team}</h5>
            
            <div class="probability-bar">
                <div class="probability-label">
                    <span>主队胜</span>
                    <span>${probabilities.home_win}%</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill bar-home" style="width: ${probabilities.home_win}%"></div>
                </div>
            </div>
            
            <div class="probability-bar">
                <div class="probability-label">
                    <span>平局</span>
                    <span>${probabilities.draw}%</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill bar-draw" style="width: ${probabilities.draw}%"></div>
                </div>
            </div>
            
            <div class="probability-bar">
                <div class="probability-label">
                    <span>客队胜</span>
                    <span>${probabilities.away_win}%</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill bar-away" style="width: ${probabilities.away_win}%"></div>
                </div>
            </div>
            
            <div class="mt-3 text-center">
                <span class="badge bg-info me-2">推荐: ${recommendation}</span>
                <span class="badge bg-light text-dark">置信度: ${confidence}%</span>
            </div>`;

        // 添加分析点
        if (analysis && analysis.length > 0) {
            html += '<div class="mt-3"><h6>AI分析:</h6>';
            analysis.forEach(point => {
                html += `<p class="text-sm mb-1">• ${point}</p>`;
            });
            html += '</div>';
        }

        container.innerHTML = html;
    }

    // 扫描价值机会
    async scanValueOpportunities() {
        this.showNotification('正在扫描价值机会...', 'info');

        try {
            const response = await fetch('/api/value/scan');
            if (response.ok) {
                const data = await response.json();
                this.updateValueOpportunities(data.scan?.opportunities || []);
                this.showNotification(`发现 ${data.scan?.total_opportunities || 0} 个价值机会`, 'success');
            }
        } catch (error) {
            console.error('扫描失败:', error);
            this.showNotification('扫描失败', 'error');
        }
    }

    // 加载世界杯分析
    async loadWorldCupAnalysis() {
        this.showNotification('正在加载世界杯分析...', 'info');

        try {
            const response = await fetch('/api/worldcup/analysis');
            if (response.ok) {
                const data = await response.json();
                this.updateWorldCupAnalysis(data.analysis || {});
                this.showNotification('世界杯分析已更新', 'success');
            }
        } catch (error) {
            console.error('加载失败:', error);
            this.showNotification('加载失败', 'error');
        }
    }

    // 加载标签页数据
    async loadTabData(tabName) {
        switch (tabName) {
            case 'live':
                await this.loadLiveMatches();
                break;
            case 'predictions':
                await this.loadPredictions();
                break;
            case 'value':
                await this.loadValueOpportunities();
                break;
            case 'worldcup':
                await this.loadWorldCupAnalysis();
                break;
            case 'analytics':
                await this.loadAnalytics();
                break;
        }
    }

    // 加载实时比赛
    async loadLiveMatches() {
        try {
            const response = await fetch('/api/dashboard/data');
            if (response.ok) {
                const data = await response.json();
                this.updateLiveMatches(data.live_matches?.matches || []);
            }
        } catch (error) {
            console.error('加载实时比赛失败:', error);
        }
    }

    // 加载预测数据
    async loadPredictions() {
        // 可以添加更多的预测功能
        console.log('加载预测数据...');
    }

    // 加载价值机会
    async loadValueOpportunities() {
        await this.scanValueOpportunities();
    }

    // 加载分析数据
    async loadAnalytics() {
        try {
            const response = await fetch('/api/analytics/trends');
            if (response.ok) {
                const data = await response.json();
                this.updateAnalytics(data.trends || {});
            }
        } catch (error) {
            console.error('加载分析数据失败:', error);
        }
    }

    // 更新分析数据
    updateAnalytics(trends) {
        const container = document.getElementById('analyticsTab');
        if (!container) return;

        let html = '<h3 class="mb-3">系统分析</h3>';
        
        if (trends.user_growth) {
            html += `
            <div class="stat-card mb-3">
                <h5>用户增长</h5>
                <div class="grid grid-cols-3 gap-2 mt-2">
                    <div class="text-center">
                        <div class="text-lg font-bold">${trends.user_growth.daily}</div>
                        <div class="text-sm text-muted">日增长</div>
                    </div>
                    <div class="text-center">
                        <div class="text-lg font-bold">${trends.user_growth.weekly}</div>
                        <div class="text-sm text-muted">周增长</div>
                    </div>
                    <div class="text-center">
                        <div class="text-lg font-bold">${trends.user_growth.monthly}</div>
                        <div class="text