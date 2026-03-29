# 智能技能安装脚本
# 基于官方API最佳实践：指数退避重试策略

function Install-SkillWithRetry {
    param(
        [string]$SkillName,
        [int]$MaxRetries = 5,
        [int]$BaseWaitSeconds = 2
    )
    
    Write-Host "开始安装技能: $SkillName" -ForegroundColor Cyan
    
    for ($i = 1; $i -le $MaxRetries; $i++) {
        Write-Host "尝试 #$i ..." -ForegroundColor Yellow
        
        # 计算等待时间（指数退避）
        $waitTime = [math]::Pow($BaseWaitSeconds, $i)
        if ($i -gt 1) {
            Write-Host "等待 $waitTime 秒后重试..." -ForegroundColor Gray
            Start-Sleep -Seconds $waitTime
        }
        
        try {
            # 尝试安装
            $result = clawhub install $SkillName 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ 成功安装: $SkillName" -ForegroundColor Green
                return $true
            }
            else {
                # 分析错误类型
                $errorText = $result -join "`n"
                
                if ($errorText -match "Rate limit exceeded") {
                    Write-Host "⚠️ 速率限制，等待后重试" -ForegroundColor Yellow
                    
                    # 从错误信息中提取重置时间
                    if ($errorText -match "reset in (\d+)s") {
                        $resetTime = [int]$matches[1]
                        Write-Host "检测到重置时间: ${resetTime}秒" -ForegroundColor Gray
                        Start-Sleep -Seconds ($resetTime + 1)
                    }
                }
                elseif ($errorText -match "Skill not found") {
                    Write-Host "❌ 技能未找到: $SkillName" -ForegroundColor Red
                    return $false
                }
                elseif ($errorText -match "flagged as suspicious") {
                    Write-Host "⚠️ 安全警告: 技能被标记为可疑" -ForegroundColor Red
                    Write-Host "使用 --force 参数或审查代码后再安装" -ForegroundColor Yellow
                    return $false
                }
                else {
                    Write-Host "❌ 安装失败: $errorText" -ForegroundColor Red
                }
            }
        }
        catch {
            Write-Host "❌ 异常错误: $_" -ForegroundColor Red
        }
    }
    
    Write-Host "❌ 达到最大重试次数，安装失败: $SkillName" -ForegroundColor Red
    return $false
}

# 安装函数结束
Write-Host "智能安装脚本已加载" -ForegroundColor Green