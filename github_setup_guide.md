# GitHub账户连接指南

## 账户信息
- **用户名**: 15718628646
- **邮箱**: 15718628646@163.com
- **密码**: 147258369zB

## SSH公钥
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQhnm20BUSyxttnh9SAdkW3pw51cuA36sO4ACiEHsAcW9moUbyGi/P3VK6/ej+hiKMksD9TiImz0CHRD8I8fVSgvSFHhfj0CY8y9VOUTG2my2xk1VQKA8LvWcDzcKrWmuWQvtJRC0nq8HdNDGYCuDmmt2nFTvKA7O2Reqaus46P/Vb0Cxat94M67iAQhjY+vFlr6P7gP3KQ73sUvIv9D4TQSY/GeJg9xvu3fNWriyKzN1b9TC/VdwI6at+gscDPC6TxzvlSEs2HSF0isYe0wwsf7cgtKKD2ArJ4I8WyWHOOS81AuK69IyolsaLjJ2FIvs7Xa8Xvtr/tJTbNfsXCvAIyDtsgQDR5u8/5b8LQ0UtgUT6YRP0gmTzLNSvWxpzvA3MRp6RL+yX9Tz911mdKfCrfNo7KeAvNf+gG6S3V8OUU60m244XDnuqeArGDnDkIsqYzZ9rHYssfuGBNLczWGIc9arALPuhz2thvzesGeNq1K5GNZXOV4gV9ISuhOVAlqwcAUZtLkS3nHrHz3zX5qxwWUUK4ey34ICAoyoj6HKbaHnZwT6D26M/jdmis1dxmuZ1cGqbytSBDNtuWs/VK3IM2gEH1jHEOcjsS9pXCoctEVDEwDwG998rcupdNBMHva+UZJZXuf7lwiO21SBHoFuN+eVbMc/Zjm887bZht8naPQ== 15718628646@163.com
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
   - Title: Windows Server - 2026-03-30
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
生成时间: 2026-03-30 03:34:19
