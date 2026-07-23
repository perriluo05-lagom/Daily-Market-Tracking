import json
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from logging.handlers import RotatingFileHandler

import akshare as ak

from config.config import Config
from modules.data_collector import DataCollector
from modules.ai_analyzer import AIAnalyzer
from modules.mail_sender import MailSender

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log_file = 'market_tracking.log'
max_size = 5 * 1024 * 1024
backup_count = 4

file_handler = RotatingFileHandler(
    log_file,
    maxBytes=max_size,
    backupCount=backup_count,
    encoding='utf-8',
    mode='a'
)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)

TIMEZONE = ZoneInfo("Asia/Shanghai")
SUBSCRIPTION_FILE = os.path.join(os.path.dirname(__file__), "data", "subscription_status.json")


def ensure_subscription_file():
    if not os.path.exists(SUBSCRIPTION_FILE):
        status = {"active": True, "last_updated": datetime.now(TIMEZONE).isoformat()}
        os.makedirs(os.path.dirname(SUBSCRIPTION_FILE), exist_ok=True)
        with open(SUBSCRIPTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        logger.info("Created subscription_status.json with active=True")


def is_subscription_active():
    ensure_subscription_file()
    try:
        with open(SUBSCRIPTION_FILE, 'r', encoding='utf-8') as f:
            status = json.load(f)
        return status.get("active", True)
    except Exception as e:
        logger.error(f"Failed to read subscription status: {e}")
        return True


def is_trading_day(date=None):
    if date is None:
        date = datetime.now(TIMEZONE).date()
    
    if date.weekday() >= 5:
        logger.info(f"{date} is a weekend (non-trading day)")
        return False
    
    try:
        trading_days = ak.tool_trade_date_hist_sina()
        trading_day_set = set(trading_days['trade_date'].astype(str).tolist())
        
        today_str = date.strftime("%Y-%m-%d")
        
        if today_str in trading_day_set:
            logger.info(f"{date} is a trading day")
            return True
        else:
            logger.info(f"{date} is not in trading calendar (holiday or non-trading day)")
            return False
    except Exception as e:
        logger.warning(f"Failed to check trading day from calendar: {e}. Checking weekday...")
        return date.weekday() < 5


def has_run_today():
    today_str = datetime.now(TIMEZONE).strftime("%Y%m%d")
    data_file = os.path.join(Config.DAILY_DATA_DIR, f"market_data_{today_str}.json")
    report_file = os.path.join(Config.DAILY_DATA_DIR, f"analysis_report_{today_str}.txt")
    
    return os.path.exists(data_file) or os.path.exists(report_file)


def cleanup_old_files(retention_days=7):
    try:
        now = datetime.now(TIMEZONE)
        cutoff_date = now - datetime.timedelta(days=retention_days)
        
        if not os.path.exists(Config.DAILY_DATA_DIR):
            return
        
        deleted_count = 0
        for filename in os.listdir(Config.DAILY_DATA_DIR):
            filepath = os.path.join(Config.DAILY_DATA_DIR, filename)
            
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath), TIMEZONE)
                if file_time < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old data files (older than {retention_days} days)")
    
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


def run_daily_task():
    now = datetime.now(TIMEZONE)
    today_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info("=" * 50)
    logger.info(f"Starting daily market tracking task at {today_str}")
    logger.info("=" * 50)
    
    if not is_trading_day():
        logger.info("Today is not a trading day, skipping...")
        logger.info("=" * 50)
        return
    
    if has_run_today():
        logger.info("Task already ran today, skipping...")
        logger.info("=" * 50)
        return
    
    if not is_subscription_active():
        logger.info("Subscription is inactive, skipping email sending...")
        logger.info("=" * 50)
        return
    
    try:
        Config.validate()
        
        data_collector = DataCollector(Config.DAILY_DATA_DIR)
        
        logger.info("Step 1: Collecting market data...")
        market_data = data_collector.collect()
        
        if not market_data:
            logger.error("Failed to collect market data")
            return
        
        if not market_data.get("ashare", {}).get("sector_index") and not market_data.get("global", {}).get("global_indices"):
            logger.error("No valid data collected, skipping analysis")
            return
        
        logger.info("Step 2: Saving market data...")
        data_collector.save_data(market_data)
        
        logger.info("Step 3: AI analysis...")
        if Config.AI_PROVIDER == "deepseek":
            ai_analyzer = AIAnalyzer("deepseek", Config.DEEPSEEK_API_KEY)
        elif Config.AI_PROVIDER == "douban":
            ai_analyzer = AIAnalyzer("douban", Config.DOUBAN_API_KEY)
        elif Config.AI_PROVIDER == "ark":
            ai_analyzer = AIAnalyzer("ark", Config.ARK_API_KEY, model=Config.ARK_MODEL)
        elif Config.AI_PROVIDER == "agnes":
            ai_analyzer = AIAnalyzer("agnes", Config.AGNES_API_KEY, model=Config.AGNES_MODEL)
        else:
            ai_analyzer = AIAnalyzer("deepseek", Config.DEEPSEEK_API_KEY)
        report = ai_analyzer.analyze(market_data)
        
        if not report:
            logger.error("Failed to generate AI analysis report")
            return
        
        logger.info("Step 4: Saving analysis report...")
        ai_analyzer.save_report(report, Config.DAILY_DATA_DIR)
        
        logger.info("Step 5: Sending email report...")
        mail_sender = MailSender(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            username=Config.SMTP_USERNAME,
            password=Config.SMTP_PASSWORD,
            sender=Config.SMTP_SENDER,
            recipients=Config.SMTP_RECIPIENTS
        )
        
        success = mail_sender.send_market_report(report, market_data)
        
        if success:
            logger.info("Daily task completed successfully!")
        else:
            logger.error("Failed to send email report")
        
        cleanup_old_files(retention_days=7)
            
    except Exception as e:
        logger.error(f"Daily task failed with error: {e}", exc_info=True)
    
    logger.info("=" * 50)


def main():
    logger.info("Daily Market Tracking System Started")
    logger.info(f"AI Provider: {Config.AI_PROVIDER}")
    logger.info(f"SMTP Server: {Config.SMTP_SERVER}")
    logger.info(f"Recipients: {Config.SMTP_RECIPIENTS}")
    logger.info(f"Subscription Status: {'Active' if is_subscription_active() else 'Inactive'}")
    
    ensure_subscription_file()
    run_daily_task()
    
    logger.info("Task completed, exiting...")


if __name__ == "__main__":
    main()
