import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime

logger = logging.getLogger(__name__)


class MailSender:
    def __init__(self, smtp_server, smtp_port, username, password, sender, recipients):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender = sender
        self.recipients = recipients

    def send_mail(self, subject, body, is_html=False):
        logger.info(f"Sending email to {self.recipients}...")
        
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.recipients)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        if is_html:
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.sender, self.recipients, msg.as_string())
            
            logger.info(f"Email sent successfully to {self.recipients}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_market_report(self, report, market_data=None):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d")) if market_data else datetime.now().strftime("%Y-%m-%d")
        
        subject = f"📊 每日市场分析报告 - {date}"
        
        html_body = self._format_html_report(report, market_data)
        
        return self.send_mail(subject, html_body, is_html=True)

    def _format_html_report(self, report, market_data):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d")) if market_data else datetime.now().strftime("%Y-%m-%d")
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日市场分析报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            font-size: 15px;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header .date {{
            margin-top: 8px;
            opacity: 0.9;
            font-size: 15px;
        }}
        .content {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            line-height: 1.8;
        }}
        .content h2 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .content h2:first-child {{
            margin-top: 0;
        }}
        .content h3 {{
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .content p {{
            color: #555;
            margin: 12px 0;
            font-size: 15px;
            line-height: 1.8;
        }}
        .content ul, .content ol {{
            color: #555;
            padding-left: 24px;
            font-size: 15px;
            line-height: 1.8;
        }}
        .content li {{
            margin: 10px 0;
            font-size: 15px;
            line-height: 1.8;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 10px 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
            font-size: 15px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }}
        .risk {{
            background-color: #f8d7da;
            padding: 10px 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin: 15px 0;
            font-size: 15px;
        }}
        .subscription {{
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
            margin: 15px 0;
            font-size: 14px;
            color: #444;
        }}
        .subscription strong {{
            color: #007bff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }}
        th {{
            background-color: #667eea;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #ddd;
            font-size: 14px;
        }}
        td {{
            padding: 8px 10px;
            border: 1px solid #ddd;
            font-size: 14px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
        .positive {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .negative {{
            color: #27ae60;
            font-weight: bold;
        }}
        .content strong {{
            font-weight: bold;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 每日市场分析报告</h1>
        <div class="date">{date}</div>
    </div>
    <div class="content">
        <h2>📈 市场数据概览</h2>
"""
        
        html += self._format_data_tables(market_data)
        
        html += """
        <h2>🤖 AI分析报告</h2>
"""
        
        report_lines = report.split('\n')
        current_section = ""
        
        for line in report_lines:
            if line.startswith('# '):
                continue
            elif line.startswith('## '):
                if current_section.strip():
                    html += f"        <p>{current_section.strip()}</p>\n"
                    current_section = ""
                title = line[3:].strip()
                html += f"        <h2>{title}</h2>\n"
            elif line.startswith('### '):
                if current_section.strip():
                    html += f"        <p>{current_section.strip()}</p>\n"
                    current_section = ""
                title = line[4:].strip()
                html += f"        <h3>{title}</h3>\n"
            elif line.startswith('#### '):
                if current_section.strip():
                    html += f"        <p>{current_section.strip()}</p>\n"
                    current_section = ""
                title = line[5:].strip()
                html += f"        <h4>{title}</h4>\n"
            elif line.strip() == "":
                if current_section.strip():
                    html += f"        <p>{current_section.strip()}</p>\n"
                    current_section = ""
            else:
                if current_section:
                    current_section += '<br>' + self._convert_markdown_to_html(line)
                else:
                    current_section = self._convert_markdown_to_html(line)
        
        if current_section.strip():
            html += f"        <p>{current_section.strip()}</p>\n"
        
        html += r"""
        <div class="subscription">
            <strong>📧 订阅管理</strong><br>
            当前状态：<strong style="color:green;">已开启</strong><br>
            <br>
            <strong>🔕 取消订阅：</strong><br>
            双击运行文件：<code>d:\Trae CN\program\daily_market_tracking\unsubscribe.bat</code><br>
            <br>
            <strong>🔔 恢复订阅：</strong><br>
            双击运行文件：<code>d:\Trae CN\program\daily_market_tracking\resubscribe.bat</code><br>
            <br>
            <strong>📝 查看日志：</strong><br>
            文件 <code>market_tracking.log</code> 记录了所有运行日志
        </div>
    </div>
    <div class="footer">
        <p>--- 本报告由AI自动生成，仅供参考，不构成投资建议 ---</p>
    </div>
</body>
</html>
"""
        return html

    def _convert_markdown_to_html(self, text):
        text = text.strip()
        text = text.replace('\n', '<br>')
        text = text.replace('**', '<strong>')
        text = text.replace('# ', '')
        text = text.replace('## ', '')
        text = text.replace('### ', '')
        text = text.replace('#', '')
        text = text.replace('*', '')
        text = text.replace('`', '')
        text = text.replace('- ', '• ')
        text = text.replace('> ', '')
        return text

    def _format_data_tables(self, market_data):
        html = ""
        
        ashare_top_gainers = market_data.get("ashare", {}).get("top_gainers", [])
        ashare_top_losers = market_data.get("ashare", {}).get("top_losers", [])
        
        if ashare_top_gainers:
            html += """
        <h3>🇨🇳 A股板块涨幅TOP10</h3>
        <table>
            <tr><th>排名</th><th>板块名称</th><th>收盘价</th><th>涨跌幅</th><th>成交量</th></tr>
"""
            for i, sector in enumerate(ashare_top_gainers, 1):
                name = sector.get("name", "N/A")
                close = sector.get("close", sector.get("value", "N/A"))
                change = sector.get("change_percent", 0)
                volume = sector.get("volume", "N/A")
                change_class = "positive" if change > 0 else "negative" if change < 0 else ""
                html += f"            <tr><td>{i}</td><td>{name}</td><td>{close}</td><td class='{change_class}'>{change:+.2f}%</td><td>{volume}</td></tr>\n"
            html += """
        </table>
"""
        
        if ashare_top_losers:
            html += """
        <h3>🇨🇳 A股板块跌幅TOP10</h3>
        <table>
            <tr><th>排名</th><th>板块名称</th><th>收盘价</th><th>涨跌幅</th><th>成交量</th></tr>
"""
            for i, sector in enumerate(ashare_top_losers, 1):
                name = sector.get("name", "N/A")
                close = sector.get("close", sector.get("value", "N/A"))
                change = sector.get("change_percent", 0)
                volume = sector.get("volume", "N/A")
                change_class = "positive" if change > 0 else "negative" if change < 0 else ""
                html += f"            <tr><td>{i}</td><td>{name}</td><td>{close}</td><td class='{change_class}'>{change:+.2f}%</td><td>{volume}</td></tr>\n"
            html += """
        </table>
"""
        
        return html
