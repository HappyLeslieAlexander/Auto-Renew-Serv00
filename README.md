# Auto-Renew-Serv00

Auto-Renew-Serv00 是一个自动化项目，旨在通过定期登录Serv00面板来实现自动续期。本项目使用GitHub Actions自动执行脚本，定期登录Serv00面板并通过电子邮件发送登录结果报告。

## 功能
- 每60天自动登录Serv00面板。
- 检查多个账户的登录状态。
- 通过启用StartTLS的SMTP服务器发送登录结果报告到指定的电子邮件地址。

## 环境变量设置
在开始之前，请确保你已经在GitHub仓库的`Settings` -> `Secrets and variables` -> `Actions`中添加了以下Secrets：

- `USERNAME1`
- `PASSWORD1`
- `PANEL_INDEX1`
- `USERNAME2`
- `PASSWORD2`
- `PANEL_INDEX2`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`
- `SMTP_SERVER`
- `SMTP_PORT`
- `TO_EMAIL`