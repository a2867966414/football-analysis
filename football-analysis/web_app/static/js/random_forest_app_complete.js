// 完成特征重要性图表的配置
const featureImportanceChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y', // 水平条形图
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    return `重要性: ${context.raw.toFixed(2)}%`;
                }
            }
        }
    },
    scales: {
        x: {
            beginAtZero: true,
            title: {
                display: true,
                text: '重要性 (%)'
            }
        },
        y: {
            ticks: {
                autoSkip: false
            }
        }
    }
};

// 工具函数：格式化特征名称
function formatFeatureName(featureName) {
    return featureName
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

// 工具函数：显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 5秒后自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// 导出预测数据
function exportPredictionData(predictionData) {
    if (!predictionData) return;
    
    const dataStr = JSON.stringify(predictionData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `football_prediction_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
    
    showNotification('预测数据已导出', 'success');
}

// 分享预测结果
function sharePrediction(predictionData) {
    if (!navigator.share) {
        alert('您的浏览器不支持分享功能');
        return;
    }
    
    const shareData = {
        title: '足球比赛预测结果',
        text: `预测结果: ${predictionData.result}\n概率: 客队胜${(predictionData.probabilities.away_win * 100).toFixed(1)}%, 平局${(predictionData.probabilities.draw * 100).toFixed(1)}%, 主队胜${(predictionData.probabilities.home_win * 100).toFixed(1)}%`,
        url: window.location.href
    };
    
    navigator.share(shareData)
        .then(() => showNotification('分享成功', 'success'))
        .catch(error => {
            console.error('分享失败:', error);
            showNotification('分享失败', 'danger');
        });
}

// 页面性能监控
function initPerformanceMonitoring() {
    // 记录页面加载时间
    window.addEventListener('load', () => {
        const timing = performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        
        console.log(`页面加载时间: ${loadTime}ms`);
        
        if (loadTime > 3000) {
            console.warn('页面加载较慢，建议优化');
        }
    });
}

// 初始化性能监控
initPerformanceMonitoring();

// 批量预测功能
function initBatchPrediction() {
    const batchContainer = document.getElementById('batchContainer');
    if (!batchContainer) return;
    
    // 创建批量预测界面
    batchContainer.innerHTML = `
        <div class="prediction-card">
            <h5><i class="bi bi-collection"></i> 批量预测</h5>
            <p class="text-muted mb-3">添加多场比赛进行批量预测</p>
            
            <div id="batchMatchesList" class="mb-3">
                <!-- 比赛列表将在这里动态添加 -->
            </div>
            
            <button id="addMatchBtn" class="btn btn-outline-primary mb-3">
                <i class="bi bi-plus-circle"></i> 添加比赛
            </button>
            
            <div class="d-grid gap-2">
                <button id="runBatchPredictionBtn" class="btn btn-primary">
                    <i class="bi bi-lightning-charge"></i> 运行批量预测
                </button>
                <button id="clearBatchBtn" class="btn btn-outline-secondary">
                    <i class="bi bi-trash"></i> 清空列表
                </button>
            </div>
            
            <div id="batchResults" class="mt-4" style="display: none;">
                <h6>批量预测结果</h6>
                <div class="table-responsive">
                    <table class="table" id="batchResultsTable">
                        <thead>
                            <tr>
                                <th>比赛</th>
                                <th>预测结果</th>
                                <th>主队胜率</th>
                                <th>平局率</th>
                                <th>客队胜率</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- 结果将在这里动态添加 -->
                        </tbody>
                    </table>
                </div>
                <button id="exportBatchBtn" class="btn btn-outline-success mt-2">
                    <i class="bi bi-download"></i> 导出结果
                </button>
            </div>
        </div>
    `;
    
    // 绑定事件
    document.getElementById('addMatchBtn').addEventListener('click', addBatchMatch);
    document.getElementById('runBatchPredictionBtn').addEventListener('click', runBatchPrediction);
    document.getElementById('clearBatchBtn').addEventListener('click', clearBatchMatches);
    document.getElementById('exportBatchBtn')?.addEventListener('click', exportBatchResults);
    
    // 初始添加一个比赛
    addBatchMatch();
}

// 添加批量比赛
function addBatchMatch() {
    const matchesList = document.getElementById('batchMatchesList');
    const matchCount = matchesList.children.length;
    
    const matchElement = document.createElement('div');
    matchElement.className = 'batch-match-card mb-3 p-3 border rounded';
    matchElement.innerHTML = `
        <div class="row align-items-center">
            <div class="col-md-3">
                <input type="text" class="form-control form-control-sm" placeholder="主队名称" value="主队 ${matchCount + 1}">
            </div>
            <div class="col-md-3">
                <input type="text" class="form-control form-control-sm" placeholder="客队名称" value="客队 ${matchCount + 1}">
            </div>
            <div class="col-md-4">
                <div class="input-group input-group-sm">
                    <span class="input-group-text">实力比</span>
                    <input type="number" class="form-control" placeholder="主队实力" min="0.1" max="1.0" step="0.01" value="0.65">
                    <span class="input-group-text">:</span>
                    <input type="number" class="form-control" placeholder="客队实力" min="0.1" max="1.0" step="0.01" value="0.55">
                </div>
            </div>
            <div class="col-md-2">
                <button class="btn btn-sm btn-outline-danger remove-match-btn">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    matchesList.appendChild(matchElement);
    
    // 绑定删除事件
    const removeBtn = matchElement.querySelector('.remove-match-btn');
    removeBtn.addEventListener('click', function() {
        matchElement.remove();
    });
}

// 运行批量预测
function runBatchPrediction() {
    const matchesList = document.getElementById('batchMatchesList');
    const matchElements = matchesList.querySelectorAll('.batch-match-card');
    
    if (matchElements.length === 0) {
        showNotification('请先添加比赛', 'warning');
        return;
    }
    
    // 收集比赛数据
    const matches = [];
    matchElements.forEach((element, index) => {
        const inputs = element.querySelectorAll('input');
        const homeTeam = inputs[0].value;
        const awayTeam = inputs[1].value;
        const homeStrength = parseFloat(inputs[2].value) || 0.5;
        const awayStrength = parseFloat(inputs[3].value) || 0.5;
        
        matches.push({
            id: index + 1,
            home_team: homeTeam,
            away_team: awayTeam,
            home_strength: homeStrength,
            away_strength: awayStrength,
            home_form: homeStrength * 0.9, // 基于实力估算状态
            away_form: awayStrength * 0.9,
            home_attack: homeStrength * 0.8,
            away_attack: awayStrength * 0.8,
            home_defense: homeStrength * 0.7,
            away_defense: awayStrength * 0.7,
            home_advantage: 0.2,
            home_injuries: 0.1,
            away_injuries: 0.1,
            head_to_head: 0.5,
            importance: 0.7,
            weather: 0.0,
            fatigue: 0.1
        });
    });
    
    // 显示加载状态
    const runBtn = document.getElementById('runBatchPredictionBtn');
    const originalText = runBtn.innerHTML;
    runBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> 预测中...';
    runBtn.disabled = true;
    
    // 发送批量预测请求
    fetch('/api/predict/batch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ matches: matches })
    })
    .then(response => response.json())
    .then(data => {
        runBtn.innerHTML = originalText;
        runBtn.disabled = false;
        
        if (data.success) {
            displayBatchResults(data.predictions);
        } else {
            showNotification('批量预测失败: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        runBtn.innerHTML = originalText;
        runBtn.disabled = false;
        console.error('批量预测请求失败:', error);
        showNotification('批量预测请求失败', 'danger');
    });
}

// 显示批量预测结果
function displayBatchResults(predictions) {
    const resultsContainer = document.getElementById('batchResults');
    const resultsTable = document.getElementById('batchResultsTable');
    const tbody = resultsTable.querySelector('tbody');
    
    // 清空旧结果
    tbody.innerHTML = '';
    
    // 添加新结果
    predictions.forEach(prediction => {
        const row = document.createElement('tr');
        
        // 根据预测结果设置行样式
        let rowClass = '';
        switch(prediction.prediction) {
            case 0: rowClass = 'table-danger'; break;
            case 1: rowClass = 'table-warning'; break;
            case 2: rowClass = 'table-success'; break;
        }
        
        row.className = rowClass;
        row.innerHTML = `
            <td><strong>${prediction.home_team}</strong> vs <strong>${prediction.away_team}</strong></td>
            <td><span class="badge bg-${prediction.prediction === 2 ? 'success' : prediction.prediction === 1 ? 'warning' : 'danger'}">${prediction.result}</span></td>
            <td>${(prediction.probabilities.home_win * 100).toFixed(1)}%</td>
            <td>${(prediction.probabilities.draw * 100).toFixed(1)}%</td>
            <td>${(prediction.probabilities.away_win * 100).toFixed(1)}%</td>
        `;
        
        tbody.appendChild(row);
    });
    
    // 显示结果容器
    resultsContainer.style.display = 'block';
    
    // 滚动到结果
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
    
    showNotification(`批量预测完成，共 ${predictions.length} 场比赛`, 'success');
}

// 清空批量比赛
function clearBatchMatches() {
    if (!confirm('确定要清空所有比赛吗？')) {
        return;
    }
    
    const matchesList = document.getElementById('batchMatchesList');
    matchesList.innerHTML = '';
    
    const resultsContainer = document.getElementById('batchResults');
    resultsContainer.style.display = 'none';
    
    showNotification('已清空所有比赛', 'info');
}

// 导出批量结果
function exportBatchResults() {
    const rows = document.querySelectorAll('#batchResultsTable tbody tr');
    if (rows.length === 0) {
        showNotification('没有结果可导出', 'warning');
        return;
    }
    
    // 构建CSV数据
    let csv = '比赛,预测结果,主队胜率,平局率,客队胜率\n';
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const match = cells[0].textContent.trim();
        const result = cells[1].textContent.trim();
        const homeWin = cells[2].textContent.trim();
        const draw = cells[3].textContent.trim();
        const awayWin = cells[4].textContent.trim();
        
        csv += `"${match}","${result}","${homeWin}","${draw}","${awayWin}"\n`;
    });
    
    // 创建下载链接
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `batch_predictions_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    
    URL.revokeObjectURL(url);
    
    showNotification('批量结果已导出为CSV文件', 'success');
}

// 初始化所有功能
function initAllFeatures() {
    // 检查模型状态
    checkModelStatus();
    
    // 加载示例比赛
    loadExampleMatches();
    
    // 初始化滑块
    initSliders();
    
    // 初始化批量预测
    initBatchPrediction();
    
    // 绑定事件
    document.getElementById('predictBtn').addEventListener('click', predictMatch);
    document.getElementById('retrainBtn').addEventListener('click', retrainModel);
    
    // 初始化标签页
    initTabs();
    
    // 显示欢迎消息
    setTimeout(() => {
        showNotification('随机森林足球预测系统已就绪！', 'success');
    }, 1000);
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAllFeatures);
} else {
    initAllFeatures();
}