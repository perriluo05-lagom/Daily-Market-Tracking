# 📊 每日市场分析报告

一个基于Python的A股市场每日分析报告工具，自动收集A股板块数据，通过AI智能分析，并将报告发送到你的邮箱。

## ✨ 功能特点

- 🇨🇳 **A股板块数据收集**：自动获取A股板块涨幅TOP10和跌幅TOP10数据
- 🤖 **AI智能分析**：基于Agnes AI进行市场分析，提供专业的投资建议
- 📧 **邮件推送**：每日18:00自动发送分析报告到指定邮箱
- 🔔 **订阅管理**：支持一键取消/恢复订阅
- 📅 **交易日判断**：自动识别交易日和节假日

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Git

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env` 文件并填写你的配置信息：

```bash
# AI配置
AI_PROVIDER=agnes
AGNES_API_KEY=你的Agnes AI API密钥

# 邮件配置
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=你的QQ邮箱地址
SMTP_PASSWORD=你的QQ邮箱授权码
SMTP_SENDER=你的发件邮箱地址
SMTP_RECIPIENTS=接收报告的邮箱地址
```

#### 获取QQ邮箱授权码

1. 登录QQ邮箱 → 设置 → 账户
2. 开启"POP3/SMTP服务"
3. 点击"生成授权码"

#### 获取Agnes AI API密钥

1. 访问 [Agnes AI Platform](https://platform.agnes-ai.com/)
2. 注册并登录 → 进入API Keys页面
3. 生成新的API密钥

### 4. 测试运行

```bash
python main.py
```

### 5. 配置自动运行

双击运行 `setup_scheduler.bat`，将自动创建Windows任务计划，每天18:00自动运行。

## 📁 项目结构

```
daily_market_tracking/
├── main.py                 # 主程序入口
├── .env                    # 环境配置文件
├── .gitignore              # Git忽略文件
├── requirements.txt        # Python依赖
├── run.bat                 # 手动运行脚本
├── setup_scheduler.bat     # 配置自动任务脚本
├── unsubscribe.bat         # 取消订阅脚本
├── resubscribe.bat         # 恢复订阅脚本
├── config/
│   └── config.py           # 配置管理
├── modules/
│   ├── data_collector.py   # 数据收集模块
│   ├── ai_analyzer.py      # AI分析模块
│   └── mail_sender.py      # 邮件发送模块
├── data/
│   ├── daily/              # 每日数据文件
│   └── subscription_status.json  # 订阅状态
└── market_tracking.log     # 运行日志
```

## 📝 使用说明

### 手动运行

```bash
python main.py
```

### 取消订阅

双击运行 `unsubscribe.bat`，将停止每日邮件推送。

### 恢复订阅

双击运行 `resubscribe.bat`，将恢复每日邮件推送。

### 查看日志

查看 `market_tracking.log` 文件了解程序运行情况。

## 🔧 技术栈

- **数据来源**: akshare
- **AI分析**: Agnes AI
- **邮件服务**: SMTP (QQ邮箱)
- **任务调度**: Windows Task Scheduler

## ⚠️ 注意事项

1. 程序仅在交易日运行（周一至周五，排除节假日）
2. 数据收集时间为交易日下午18:00后
3. 请确保电脑在18:00时处于开机状态
4. AI分析结果仅供参考，不构成投资建议

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！