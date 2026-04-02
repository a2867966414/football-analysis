/**
 * 随机森林足球预测系统 - 前端JavaScript
 */

// 全局变量
let probabilityChart = null;
let featureImportanceChart = null;
let modelAccuracy = 0;

// 初始化函数
document.addEventListener('DOMContentLoaded', function() {
    // 初始化滑块事件
    initSliders();
    
    // 检查模型状态
    checkModelStatus();
    
    // 加载示例比赛
    loadExampleMatches();
    
    // 绑定按钮事件
    document.getElementById('predictBtn').addEventListener('click', predictMatch);
    document.getElementById('retrainBtn').addEventListener('click', retrainModel);
    document.getElementById('batchPredictBtn')?.addEventListener('click', predictBatch);
    
    // 初始化标签页切换
    initTabs();
});

// 初始化滑块
function initSliders() {
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valueElement = document.getElementById(slider.id + 'Value');
        if (valueElement) {
            // 初始值
            valueElement.textContent = parseFloat(slider.value).toFixed(2);
            
            // 滑块变化事件
            slider.addEventListener('input', function() {
                valueElement.textContent = parseFloat(this.value).toFixed(2);
            });
        }
    });
}

// 检查模型状态
function checkModelStatus() {
    fetch('/api/model/status')
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById('modelStatusText');
            const badgeElement = document.getElementById('modelStatusBadge');
            
            if (data.status === 'trained') {
                statusElement.innerHTML = `
                    <div class="row">
                        <div class="col-6">
                            <small>准确率</small><br>
                            <strong>${(data.accuracy * 100).toFixed(1)}%</strong>
                        </div>
                        <div class="col-6">
                            <small>特征数量</small><br>
                            <strong>${data.feature_count}</strong>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-12">
                            <small>训练样本</small><br>
                            <strong>${data.n_training_samples.toLocaleString()}</strong>
                        </div>
                    </div>
                `;
                
                badgeElement.className = 'status-badge status-trained';
                badgeElement.textContent = '已训练';
                modelAccuracy = data.accuracy;
            } else {
                statusElement.innerHTML = '<span class="text-danger">模型未训练，请点击重新训练按钮</span>';
                badgeElement.className = 'status-badge status-not-trained';
                badgeElement.textContent = '未训练';
            }
        })
        .catch(error => {
            console.error('检查模型状态失败:', error);
            document.getElementById('modelStatusText').innerHTML = 
                '<span class="text-danger">连接服务器失败</span>';
        });
}

// 加载示例比赛
function loadExampleMatches() {
    fetch('/api/examples')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.examples) {
                const container = document.getElementById('exampleMatches');
                container.innerHTML = '';
                
                data.examples.forEach(example => {
                    const exampleElement = document.createElement('div');
                    exampleElement.className = 'example-match';
                    exampleElement.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${example.name}</strong><br>
                                <small class="text-muted">实力: ${example.home_strength.toFixed(2)} vs ${example.away_strength.toFixed(2)}</small>
                            </div>
                            <button class="btn btn-sm btn-outline-primary load-example-btn" data-id="${example.id}">
                                <i class="bi bi-arrow-down-circle"></i>
                            </button>
                        </div>
                    `;
                    
                    container.appendChild(exampleElement);
                    
                    // 绑定加载事件
                    const loadBtn = exampleElement.querySelector('.load-example-btn');
                    loadBtn.addEventListener('click', function() {
                        loadExampleData(example);
                        
                        // 高亮当前示例
                        document.querySelectorAll('.example-match').forEach(el => {
                            el.classList.remove('active');
                        });
                        exampleElement.classList.add('active');
                    });
                });
            }
        })
        .catch(error => {
            console.error('加载示例比赛失败:', error);
        });
}

// 加载示例数据到表单
function loadExampleData(example) {
    // 设置所有滑块值
    Object.keys(example).forEach(key => {
        const slider = document.getElementById(key);
        const valueElement = document.getElementById(key + 'Value');
        
        if (slider && valueElement) {
            slider.value = example[key];
            valueElement.textContent = example[key].toFixed(2);
            
            // 触发input事件以更新其他依赖元素
            slider.dispatchEvent(new Event('input'));
        }
    });
}

// 预测单场比赛
function predictMatch() {
    // 显示加载状态
    const loadingElement = document.getElementById('predictionLoading');
    const resultElement = document.getElementById('predictionResult');
    
    loadingElement.style.display = 'block';
    resultElement.style.display = 'none';
    
    // 收集特征数据
    const features = {
        home_strength: parseFloat(document.getElementById('homeStrength').value),
        away_strength: parseFloat(document.getElementById('awayStrength').value),
        home_form: parseFloat(document.getElementById('homeForm').value),
        away_form: parseFloat(document.getElementById('awayForm').value),
        home_attack: parseFloat(document.getElementById('homeAttack').value),
        away_attack: parseFloat(document.getElementById('awayAttack').value),
        home_defense: parseFloat(document.getElementById('homeDefense').value),
        away_defense: parseFloat(document.getElementById('awayDefense').value),
        home_advantage: parseFloat(document.getElementById('homeAdvantage').value),
        home_injuries: parseFloat(document.getElementById('homeInjuries').value),
        away_injuries: parseFloat(document.getElementById('awayInjuries').value),
        head_to_head: parseFloat(document.getElementById('headToHead').value),
        importance: 0.7, // 默认值
        weather: 0.0,    // 默认值
        fatigue: 0.1     // 默认值
    };
    
    // 发送预测请求
    fetch('/api/predict/single', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(features)
    })
    .then(response => response.json())
    .then(data => {
        // 隐藏加载状态
        loadingElement.style.display = 'none';
        resultElement.style.display = 'block';
        
        if (data.success) {
            // 显示预测结果
            displayPredictionResult(data);
            
            // 更新概率图表
            updateProbabilityChart(data.probabilities);
            
            // 显示关键影响因素
            displayTopFeatures(data.top_features);
        } else {
            alert('预测失败: ' + data.error);
        }
    })
    .catch(error => {
        loadingElement.style.display = 'none';
        console.error('预测请求失败:', error);
        alert('预测请求失败，请检查网络连接');
    });
}

// 显示预测结果
function displayPredictionResult(data) {
    const resultElement = document.getElementById('resultDisplay');
    
    // 清除所有结果类
    resultElement.className = 'prediction-result';
    
    // 根据结果设置样式
    let resultClass = '';
    let resultIcon = '';
    
    switch(data.prediction) {
        case 0: // 客队胜
            resultClass = 'result-away-win';
            resultIcon = '<i class="bi bi-trophy"></i> ';
            resultText = '预测结果: 客队胜';
            break;
        case 1: // 平局
            resultClass = 'result-draw';
            resultIcon = '<i class="bi bi-dash-circle"></i> ';
            resultText = '预测结果: 平局';
            break;
        case 2: // 主队胜
            resultClass = 'result-home-win';
            resultIcon = '<i class="bi bi-trophy-fill"></i> ';
            resultText = '预测结果: 主队胜';
            break;
        default:
            resultText = '预测结果未知';
    }
    
    // 添加准确率信息
    if (modelAccuracy > 0) {
        resultText += ` (模型准确率: ${(modelAccuracy * 100).toFixed(1)}%)`;
    }
    
    resultElement.className = `prediction-result ${resultClass}`;
    resultElement.innerHTML = `${resultIcon}${resultText}`;
}

// 更新概率图表
function updateProbabilityChart(probabilities) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');
    
    // 销毁旧图表
    if (probabilityChart) {
        probabilityChart.destroy();
    }
    
    // 创建新图表
    probabilityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['客队胜', '平局', '主队胜'],
            datasets: [{
                data: [
                    probabilities.away_win * 100,
                    probabilities.draw * 100,
                    probabilities.home_win * 100
                ],
                backgroundColor: [
                    '#e53e3e', // 客队胜 - 红色
                    '#d69e2e', // 平局 - 黄色
                    '#38a169'  // 主队胜 - 绿色
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw.toFixed(1)}%`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

// 显示关键影响因素
function displayTopFeatures(topFeatures) {
    const container = document.getElementById('topFeatures');
    
    if (!topFeatures || topFeatures.length === 0) {
        container.innerHTML = '<p class="text-muted">无特征重要性数据</p>';
        return;
    }
    
    let html = '<div class="list-group">';
    
    topFeatures.forEach((feature, index) => {
        const importancePercent = (feature[1] * 100).toFixed(1);
        const featureName = feature[0].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        html += `
            <div class="list-group-item border-0 py-2 px-0">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="badge bg-primary me-2">${index + 1}</span>
                        ${featureName}
                    </div>
                    <div>
                        <span class="badge bg-light text-dark">${importancePercent}%</span>
                    </div>
                </div>
                <div class="progress mt-1" style="height: 6px;">
                    <div class="progress-bar bg-primary" style="width: ${importancePercent}%"></div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// 重新训练模型
function retrainModel() {
    if (!confirm('确定要重新训练模型吗？这可能需要几秒钟时间。')) {
        return;
    }
    
    const retrainBtn = document.getElementById('retrainBtn');
    const originalText = retrainBtn.innerHTML;
    
    retrainBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> 训练中...';
    retrainBtn.disabled = true;
    
    fetch('/api/model/retrain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ n_samples: 5000 })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`模型重新训练完成！\n准确率: ${(data.accuracy * 100).toFixed(1)}%\n训练样本: ${data.training_samples}`);
            checkModelStatus(); // 刷新模型状态
        } else {
            alert('重新训练失败: ' + data.error);
        }
    })
    .catch(error => {
        console.error('重新训练失败:', error);
        alert('重新训练请求失败');
    })
    .finally(() => {
        retrainBtn.innerHTML = originalText;
        retrainBtn.disabled = false;
    });
}

// 批量预测
function predictBatch() {
    // 这里可以实现批量预测功能
    alert('批量预测功能正在开发中...');
}

// 初始化标签页
function initTabs() {
    const tabTriggers = document.querySelectorAll('#predictionTabs button[data-bs-toggle="tab"]');
    
    tabTriggers.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const targetId = event.target.getAttribute('data-bs-target');
            
            // 根据激活的标签页执行相应操作
            switch(targetId) {
                case '#analysis':
                    loadModelAnalysis();
                    break;
                case '#batch':
                    // 可以在这里初始化批量预测界面
                    break;
            }
        });
    });
}

// 加载模型分析
function loadModelAnalysis() {
    fetch('/api/model/info')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayModelAnalysis(data);
            }
        })
        .catch(error => {
            console.error('加载模型分析失败:', error);
        });
}

// 显示模型分析
function displayModelAnalysis(data) {
    const analysisTab = document.getElementById('analysis');
    
    // 创建分析内容
    let html = `
        <div class="row">
            <div class="col-lg-6">
                <div class="prediction-card">
                    <h5><i class="bi bi-info-circle"></i> 模型信息</h5>
                    <table class="table">
                        <tr>
                            <td><strong>模型类型</strong></td>
                            <td>${data.model_type === 'classifier' ? '分类器' : '回归器'}</td>
                        </tr>
                        <tr>
                            <td><strong>特征数量</strong></td>
                            <td>${data.n_features}</td>
                        </tr>
                        <tr>
                            <td><strong>训练样本</strong></td>
                            <td>${data.n_training_samples.toLocaleString()}</td>
                        </tr>
                        <tr>
                            <td><strong>创建时间</strong></td>
                            <td>${new Date(data.model_created).toLocaleString()}</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div class="col-lg-6">
                <div class="prediction-card">
                    <h5><i class="bi bi-graph-up"></i> 特征重要性</h5>
                    <div class="feature-importance">
                        <canvas id="featureImportanceChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="prediction-card">
                    <h5><i class="bi bi-clock-history"></i> 训练历史</h5>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>训练时间</th>
                                    <th>训练样本</th>
                                    <th>训练得分</th>
                                    <th>测试得分</th>
                                </tr>
                            </thead>
                            <tbody>
    `;
    
    // 添加训练历史
    if (data.training_history && data.training_history.length > 0) {
        data.training_history.forEach(history => {
            html += `
                <tr>
                    <td>${new Date(history.timestamp).toLocaleString()}</td>
                    <td>${history.n_samples.toLocaleString()}</td>
                    <td>${history.train_score.toFixed(4)}</td>
                    <td>${history.test_score.toFixed(4)}</td>
                </tr>
            `;
        });
    } else {
        html += `<tr><td colspan="4" class="text-center">无训练历史数据</td></tr>`;
    }
    
    html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    analysisTab.innerHTML = html;
    
    // 绘制特征重要性图表
    if (data.feature_importance && data.feature_importance.length > 0) {
        drawFeatureImportanceChart(data.feature_importance);
    }
}

// 绘制特征重要性图表
function drawFeatureImportanceChart(features) {
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');
    
    // 准备数据
    const labels = features.map(f => {
        // 美化特征名称
        return f.feature
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase())
            .substring(0, 20); // 限制长度
    });
    
    const data = features.map(f => f.importance * 100);
    
    // 销毁旧图表
    if (featureImportanceChart) {
        featureImportanceChart.destroy();
    }
    
    // 创建新图表
    featureImportanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '重要性 (%)',
                data: data,
                backgroundColor: 'rgba(49, 130, 206, 0.7)',
                borderColor: 'rgba(49, 130, 206, 1)',
                borderWidth: 1
            }]
        },
        options: {
