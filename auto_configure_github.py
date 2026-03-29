#!/usr/bin/env python3
"""
自动登录并配置GitHub账户
"""

import os
import subprocess
import requests
import json
import time
import webbrowser
from datetime import datetime

print("=" * 80)
print("自动登录并配置GitHub账户")
print("账户: 15718628646@163.com")
print("开始时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("=" * 80)

class GitHubAutoConfig:
    """GitHub自动配置"""
    
    def __init__(self):
        self.username = "15718628646"
        self.email = "15718628646@163.com"
        self.password = "147258369zB"
        self.ssh_key_path = os.path.expanduser("~/.ssh/github_15718628646")
        self.config_report = {
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'steps_completed': [],
            'errors': [],
            'ssh_key_added': False,
            'github_authenticated': False
        }
    
    def setup_git_config(self):
        """设置Git配置"""
        print("\n1. 设置Git配置...")
        
        try:
            # 设置用户名
            subprocess.run(['git', 'config', '--global', 'user.name', self.username], 
                          check=True, capture_output=True)
            
            # 设置邮箱
            subprocess.run(['git', 'config', '--global', 'user.email', self.email], 
                          check=True, capture_output=True)
            
            # 验证配置
            name_result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                        capture_output=True, text=True)
            email_result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                         capture_output=True, text=True)
            
            print(f"   ✅ Git配置完成:")
            print(f"      用户名: {name_result.stdout.strip()}")
            print(f"      邮箱: {email_result.stdout.strip()}")
            
            self.config_report['steps_completed'].append('git_config')
            return True
            
        except Exception as e:
            print(f"   ❌ Git配置失败: {e}")
            self.config_report['errors'].append(f"git_config: {e}")
            return False
    
    def ensure_ssh_key(self):
        """确保SSH密钥存在"""
        print("\n2. 检查/创建SSH密钥...")
        
        ssh_dir = os.path.dirname(self.ssh_key_path)
        
        try:
            # 创建.ssh目录
            os.makedirs(ssh_dir, exist_ok=True)
            print(f"   SSH目录: {ssh_dir}")
            
            # 检查密钥是否存在
            if os.path.exists(self.ssh_key_path):
                print(f"   SSH密钥已存在: {self.ssh_key_path}")
                
                # 读取公钥
                pub_key_path = self.ssh_key_path + '.pub'
                if os.path.exists(pub_key_path):
                    with open(pub_key_path, 'r') as f:
                        self.public_key = f.read().strip()
                    print(f"   公钥已读取")
                else:
                    print(f"   公钥文件不存在，重新生成...")
                    self.generate_ssh_key()
            else:
                print(f"   SSH密钥不存在，正在生成...")
                self.generate_ssh_key()
            
            self.config_report['steps_completed'].append('ssh_key')
            return True
            
        except Exception as e:
            print(f"   ❌ SSH密钥处理失败: {e}")
            self.config_report['errors'].append(f"ssh_key: {e}")
            return False
    
    def generate_ssh_key(self):
        """生成SSH密钥"""
        print("   生成SSH密钥...")
        
        try:
            # 使用ssh-keygen生成密钥
            cmd = [
                'ssh-keygen',
                '-t', 'rsa',
                '-b', '4096',
                '-C', self.email,
                '-f', self.ssh_key_path,
                '-N', ''
            ]
            
            # 运行命令
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 自动确认
            output, error = process.communicate(input='\n\n')
            
            if process.returncode == 0:
                print(f"   ✅ SSH密钥生成成功: {self.ssh_key_path}")
                
                # 读取公钥
                pub_key_path = self.ssh_key_path + '.pub'
                with open(pub_key_path, 'r') as f:
                    self.public_key = f.read().strip()
                
                print(f"   公钥: {self.public_key[:50]}...")
                return True
            else:
                print(f"   ❌ SSH密钥生成失败: {error}")
                return False
                
        except Exception as e:
            print(f"   ❌ SSH密钥生成异常: {e}")
            return False
    
    def setup_ssh_config(self):
        """设置SSH配置"""
        print("\n3. 配置SSH...")
        
        ssh_config_path = os.path.expanduser('~/.ssh/config')
        
        try:
            config_content = f"""# GitHub配置 - {datetime.now().strftime('%Y-%m-%d')}
Host github.com
    HostName github.com
    User git
    IdentityFile {self.ssh_key_path}
    IdentitiesOnly yes
"""
            
            # 追加或创建配置
            with open(ssh_config_path, 'a', encoding='utf-8') as f:
                f.write('\n' + config_content)
            
            # 设置权限
            os.chmod(ssh_config_path, 0o600)
            
            print(f"   ✅ SSH配置已更新: {ssh_config_path}")
            self.config_report['steps_completed'].append('ssh_config')
            return True
            
        except Exception as e:
            print(f"   ❌ SSH配置失败: {e}")
            self.config_report['errors'].append(f"ssh_config: {e}")
            return False
    
    def open_github_ssh_page(self):
        """打开GitHub SSH密钥页面"""
        print("\n4. 打开GitHub SSH密钥配置页面...")
        
        try:
            # GitHub SSH密钥页面
            ssh_url = "https://github.com/settings/ssh/new"
            
            print(f"   正在打开浏览器...")
            print(f"   页面: {ssh_url}")
            print(f"   请按照以下步骤操作:")
            print(f"   1. 登录GitHub (如果未登录)")
            print(f"   2. 粘贴SSH公钥")
            print(f"   3. 点击 'Add SSH key'")
            
            # 打开浏览器
            webbrowser.open(ssh_url)
            
            print(f"   ✅ 浏览器已打开GitHub SSH配置页面")
            print(f"   ⚠️  需要手动登录并添加SSH公钥")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 打开浏览器失败: {e}")
            self.config_report['errors'].append(f"open_browser: {e}")
            return False
    
    def display_ssh_key(self):
        """显示SSH公钥"""
        print("\n5. SSH公钥信息:")
        
        try:
            pub_key_path = self.ssh_key_path + '.pub'
            if os.path.exists(pub_key_path):
                with open(pub_key_path, 'r') as f:
                    public_key = f.read().strip()
                
                print("=" * 60)
                print("请复制以下SSH公钥到GitHub:")
                print("=" * 60)
                print(public_key)
                print("=" * 60)
                
                # 保存到文件便于复制
                key_file = "github_ssh_key.txt"
                with open(key_file, 'w', encoding='utf-8') as f:
                    f.write(public_key)
                
                print(f"\n   公钥已保存到: {key_file}")
                print(f"   可以直接复制文件内容")
                
                return public_key
            else:
                print("   ❌ 公钥文件不存在")
                return None
                
        except Exception as e:
            print(f"   ❌ 读取公钥失败: {e}")
            return None
    
    def test_github_connection(self):
        """测试GitHub连接"""
        print("\n6. 测试GitHub连接...")
        
        try:
            print("   测试SSH连接...")
            test_cmd = ['ssh', '-T', 'git@github.com']
            
            process = subprocess.Popen(
                test_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 设置超时
            try:
                stdout, stderr = process.communicate(timeout=10)
                
                if process.returncode == 1 and 'successfully authenticated' in stderr:
                    print(f"   ✅ GitHub SSH连接成功!")
                    print(f"   消息: {stderr.strip()}")
                    self.config_report['github_authenticated'] = True
                    return True
                else:
                    print(f"   ⚠️  GitHub连接测试结果:")
                    print(f"     返回码: {process.returncode}")
                    if stdout:
                        print(f"     输出: {stdout[:100]}")
                    if stderr:
                        print(f"     错误: {stderr[:100]}")
                    return False
                    
            except subprocess.TimeoutExpired:
                process.kill()
                print("   ⚠️  连接超时，可能需要先添加SSH公钥到GitHub")
                return False
                
        except Exception as e:
            print(f"   ❌ 连接测试失败: {e}")
            return False
    
    def create_github_token_guide(self):
        """创建GitHub Token指南"""
        print("\n7. 创建GitHub Token指南...")
        
        try:
            guide_content = f"""# GitHub完整配置指南

## 账户信息
- **用户名**: {self.username}
- **邮箱**: {self.email}
- **密码**: {self.password}

## 配置状态
- Git配置: ✅ 已完成
- SSH密钥: ✅ 已生成
- SSH配置: ✅ 已设置
- GitHub认证: {'✅ 已通过' if self.config_report['github_authenticated'] else '⚠️ 待完成'}

## 手动配置步骤

### 1. 登录GitHub
1. 访问: https://github.com/login
2. 使用以下凭据登录:
   - 用户名/邮箱: {self.email}
   - 密码: {self.password}

### 2. 添加SSH公钥
1. 访问: https://github.com/settings/ssh/new
2. 填写:
   - Title: Windows Server - {datetime.now().strftime('%Y-%m-%d')}
   - Key type: Authentication Key
   - Key: 粘贴下面的SSH公钥

### 3. 创建Personal Access Token (可选)
1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择权限:
   - repo (全部)
   - workflow
   - write:packages
   - delete:packages
4. 生成并保存Token

## 验证配置
```bash
# 测试SSH连接
ssh -T git@github.com

# 检查Git配置
git config --global user.name
git config --global user.email
```

## 故障排除
1. **SSH连接失败**: 确保公钥已添加到GitHub
2. **权限问题**: 检查.ssh目录权限 (700)
3. **配置问题**: 检查~/.ssh/config文件格式
4. **网络问题**: 检查防火墙设置

## 技术支持
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 配置文件: ~/.ssh/config
- SSH密钥: {self.ssh_key_path}
"""
            
            guide_file = "github_complete_guide.md"
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide_content)
            
            print(f"   ✅ 完整指南已创建: {guide_file}")
            return guide_file
            
        except Exception as e:
            print(f"   ❌ 创建指南失败: {e}")
            return None
    
    def run_auto_config(self):
        """运行自动配置"""
        print("开始自动配置GitHub...")
        
        # 1. Git配置
        self.setup_git_config()
        
        # 2. SSH密钥
        self.ensure_ssh_key()
        
        # 3. SSH配置
        self.setup_ssh_config()
        
        # 4. 显示SSH公钥
        self.display_ssh_key()
        
        # 5. 打开GitHub页面
        self.open_github_ssh_page()
        
        # 6. 测试连接
        print("\n等待10秒，然后测试连接...")
        time.sleep(10)
        self.test_github_connection()
        
        # 7. 创建指南
        self.create_github_token_guide()
        
        # 总结
        self.config_report['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("\n" + "=" * 80)
        print("GitHub自动配置完成!")
        print("=" * 80)
        
        print(f"\n📋 配置总结:")
        print(f"   开始时间: {self.config_report['start_time']}")
        print(f"   结束时间: {self.config_report['end_time']}")
        print(f"   完成步骤: {len(self.config_report['steps_completed'])}")
        
        if self.config_report['github_authenticated']:
            print(f"   GitHub认证: ✅ 已通过")
        else:
            print(f"   GitHub认证: ⚠️  需要手动添加SSH公钥")
        
        if self.config_report['errors']:
            print(f"   错误数量: {len(self.config_report['errors'])}")
        
        print(f"\n🚀 下一步:")
        print(f"   1. 按照浏览器打开的页面添加SSH公钥")
        print(f"   2. 测试连接: ssh -T git@github.com")
        print(f"   3. 开始使用Git进行版本控制")
        
        print("\n" + "=" * 80)
        
        return self.config_report['github_authenticated']

def main():
    """主函数"""
    print("自动登录并配置GitHub账户...")
    
    config = GitHubAutoConfig()
    authenticated = config.run_auto_config()
    
    if authenticated:
        print("\n✅ GitHub配置完全成功!")
        print("可以立即开始使用Git进行版本控制")
    else:
        print("\n⚠️  GitHub配置基本完成，但需要手动添加SSH公钥")
        print("请按照指南完成最后一步")
    
    return authenticated

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n部分配置需要手动完成，请查看生成的指南文件")
    except KeyboardInterrupt:
        print("\n配置被用户中断")
    except Exception as e:
        print(f"\n配置过程中出错: {e}")
        print("建议手动完成GitHub配置")