#!/usr/bin/env python3
"""
连接GitHub账户
"""

import os
import subprocess
from datetime import datetime

print("=" * 80)
print("连接GitHub账户")
print("账户: 15718628646@163.com")
print("开始时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("=" * 80)

def setup_git_config():
    """设置Git配置"""
    print("\n1. 设置Git全局配置...")
    
    try:
        # 设置用户名
        subprocess.run(['git', 'config', '--global', 'user.name', '15718628646'], 
                      check=True, capture_output=True)
        print("   用户名设置成功: 15718628646")
        
        # 设置邮箱
        subprocess.run(['git', 'config', '--global', 'user.email', '15718628646@163.com'], 
                      check=True, capture_output=True)
        print("   邮箱设置成功: 15718628646@163.com")
        
        # 验证配置
        name_result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                    capture_output=True, text=True)
        email_result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                     capture_output=True, text=True)
        
        print(f"   当前配置:")
        print(f"     用户名: {name_result.stdout.strip()}")
        print(f"     邮箱: {email_result.stdout.strip()}")
        
        return True
        
    except Exception as e:
        print(f"   Git配置失败: {e}")
        return False

def create_ssh_key():
    """创建SSH密钥"""
    print("\n2. 创建SSH密钥...")
    
    ssh_dir = os.path.expanduser('~/.ssh')
    key_file = os.path.join(ssh_dir, 'github_15718628646')
    
    try:
        # 创建.ssh目录
        os.makedirs(ssh_dir, exist_ok=True)
        print(f"   创建SSH目录: {ssh_dir}")
        
        # 生成SSH密钥
        cmd = [
            'ssh-keygen',
            '-t', 'rsa',
            '-b', '4096',
            '-C', '15718628646@163.com',
            '-f', key_file,
            '-N', ''
        ]
        
        # 使用输入重载自动确认
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 自动确认覆盖（如果存在）
        output, error = process.communicate(input='y\n')
        
        if process.returncode == 0:
            print(f"   SSH密钥创建成功: {key_file}")
            
            # 读取公钥
            pub_key_file = key_file + '.pub'
            if os.path.exists(pub_key_file):
                with open(pub_key_file, 'r') as f:
                    pub_key = f.read().strip()
                
                print(f"   公钥已生成")
                print(f"   公钥文件: {pub_key_file}")
                
                return pub_key
            else:
                print("   公钥文件未找到")
                return None
        else:
            print(f"   SSH密钥生成失败: {error}")
            return None
            
    except Exception as e:
        print(f"   SSH密钥创建失败: {e}")
        return None

def setup_ssh_config():
    """设置SSH配置"""
    print("\n3. 配置SSH...")
    
    ssh_config_path = os.path.expanduser('~/.ssh/config')
    
    try:
        config_content = """# GitHub配置
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_15718628646
    IdentitiesOnly yes
"""
        
        with open(ssh_config_path, 'a', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"   SSH配置已更新: {ssh_config_path}")
        
        # 设置权限
        os.chmod(ssh_config_path, 0o600)
        print("   SSH配置文件权限已设置")
        
        return True
        
    except Exception as e:
        print(f"   SSH配置失败: {e}")
        return False

def test_github_connection():
    """测试GitHub连接"""
    print("\n4. 测试GitHub连接...")
    
    try:
        # 测试SSH连接
        test_cmd = ['ssh', '-T', 'git@github.com']
        result = subprocess.run(
            test_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 1 and 'successfully authenticated' in result.stderr:
            print("   ✅ GitHub SSH连接成功!")
            print(f"   消息: {result.stderr.strip()}")
            return True
        else:
            print(f"   GitHub连接测试结果:")
            print(f"     返回码: {result.returncode}")
            print(f"     输出: {result.stdout[:100]}")
            print(f"     错误: {result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"   连接测试失败: {e}")
        return False

def create_github_setup_guide():
    """创建GitHub设置指南"""
    print("\n5. 创建GitHub设置指南...")
    
    try:
        # 读取公钥
        pub_key_file = os.path.expanduser('~/.ssh/github_15718628646.pub')
        if os.path.exists(pub_key_file):
            with open(pub_key_file, 'r') as f:
                pub_key = f.read().strip()
        else:
            pub_key = "公钥未找到，请重新生成"
        
        guide_content = f"""# GitHub账户连接指南

## 账户信息
- **用户名**: 15718628646
- **邮箱**: 15718628646@163.com
- **密码**: 147258369zB

## SSH公钥
```
{pub_key}
```

## GitHub设置步骤

### 1. 登录GitHub
1. 访问 https://github.com/login
2. 使用以下凭据登录:
   - 用户名/邮箱: 15718628646@163.com
   - 密码: 147258369zB

### 2. 添加SSH密钥
1. 登录后点击右上角头像 → Settings
2. 左侧菜单选择 "SSH and GPG keys"
3. 点击 "New SSH key"
4. 填写:
   - Title: Windows Server - {datetime.now().strftime('%Y-%m-%d')}
   - Key type: Authentication Key
   - Key: 粘贴上面的SSH公钥
5. 点击 "Add SSH key"

### 3. 验证连接
在终端运行:
```bash
ssh -T git@github.com
```
应该看到: "Hi 15718628646! You've successfully authenticated..."

## Git配置验证
运行以下命令检查配置:
```bash
git config --global user.name
git config --global user.email
```

## 开始使用
现在可以使用以下命令克隆仓库:
```bash
git clone git@github.com:15718628646/your-repo.git
```

## 故障排除
1. 如果SSH连接失败，检查SSH密钥是否正确添加
2. 确保.ssh目录权限正确 (700)
3. 确保配置文件权限正确 (600)
4. 重启SSH代理: `eval $(ssh-agent) && ssh-add ~/.ssh/github_15718628646`

---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_file = 'github_setup_guide.md'
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"   指南已创建: {guide_file}")
        print(f"   SSH公钥已保存到指南文件中")
        
        return guide_file
        
    except Exception as e:
        print(f"   创建指南失败: {e}")
        return None

def main():
    """主函数"""
    print("开始连接GitHub账户...")
    
    # 1. 设置Git配置
    if not setup_git_config():
        print("Git配置失败，继续其他步骤...")
    
    # 2. 创建SSH密钥
    pub_key = create_ssh_key()
    
    # 3. 设置SSH配置
    setup_ssh_config()
    
    # 4. 创建指南
    guide_file = create_github_setup_guide()
    
    # 5. 测试连接
    connection_ok = test_github_connection()
    
    # 总结
    print("\n" + "=" * 80)
    print("GitHub连接设置完成!")
    print("=" * 80)
    
    print("\n📋 设置总结:")
    print(f"   账户: 15718628646@163.com")
    print(f"   Git配置: 已设置")
    print(f"   SSH密钥: 已生成")
    print(f"   SSH配置: 已更新")
    print(f"   连接测试: {'✅ 成功' if connection_ok else '⚠️ 需要手动配置'}")
    
    if guide_file:
        print(f"\n📖 详细指南: {guide_file}")
        print("   请按照指南中的步骤在GitHub网站上添加SSH密钥")
    
    print("\n🚀 下一步:")
    print("   1. 登录GitHub: https://github.com/login")
    print("   2. 添加SSH公钥到GitHub账户")
    print("   3. 测试连接: ssh -T git@github.com")
    print("   4. 开始使用Git进行版本控制")
    
    print("\n" + "=" * 80)
    
    return connection_ok

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("部分设置可能需要手动完成")
    except Exception as e:
        print(f"设置过程中出错: {e}")
        print("请手动完成GitHub连接设置")