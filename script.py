import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playwright.sync_api import sync_playwright
import os

# 从环境变量中获取账户信息和后台序数
accounts = [
    {"username": os.getenv("USERNAME1"), "password": os.getenv("PASSWORD1"), "panel_index": os.getenv("PANEL_INDEX1")},
    {"username": os.getenv("USERNAME2"), "password": os.getenv("PASSWORD2"), "panel_index": os.getenv("PANEL_INDEX2")}
]

# SMTP配置
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("EMAIL_USERNAME")
smtp_password = os.getenv("EMAIL_PASSWORD")
recipient_email = os.getenv("TO_EMAIL")

# 登录并检查状态的函数
def login_and_check(account):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            login_url = f"https://panel{account['panel_index']}.serv00.com/login/?next=/"
            page.goto(login_url)

            # 输入用户名和密码
            page.fill('#id_username', account['username'])
            page.fill('#id_password', account['password'])

            # 提交登录表单并等待导航
            with page.expect_navigation():
                page.click('#submit')

            # 判断是否登录成功
            is_logged_in = page.query_selector('a[href="/logout/"]') is not None
            browser.close()

            if is_logged_in:
                return f"账号 {account['username']} 登录成功！"
            else:
                return f"账号 {account['username']} 登录失败，请检查账号和密码是否正确。"

    except Exception as e:
        return f"账号 {account['username']} 登录时出现错误: {e}"

# 汇总结果
results = [login_and_check(account) for account in accounts if account["username"] and account["password"]]

# 生成邮件内容
email_content = "\n\n".join(results)

# 发送邮件
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = recipient_email
msg['Subject'] = "Serv00面板登录结果"

msg.attach(MIMEText(email_content, 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 启用StartTLS
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(smtp_username, recipient_email, text)
    server.quit()
    print("邮件发送成功")
except Exception as e:
    print(f"邮件发送失败: {e}")
