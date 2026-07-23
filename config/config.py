import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek")
    
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DOUBAN_API_KEY = os.getenv("DOUBAN_API_KEY")
    ARK_API_KEY = os.getenv("ARK_API_KEY")
    ARK_MODEL = os.getenv("ARK_MODEL", "doubao-pro")
    AGNES_API_KEY = os.getenv("AGNES_API_KEY")
    AGNES_MODEL = os.getenv("AGNES_MODEL", "agnes-2.0-flash")
    
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER = os.getenv("SMTP_SENDER")
    SMTP_RECIPIENTS = [r.strip() for r in os.getenv("SMTP_RECIPIENTS", "").split(",") if r.strip()]
    
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    DAILY_DATA_DIR = os.path.join(DATA_DIR, "daily")
    
    @staticmethod
    def validate():
        if Config.AI_PROVIDER == "deepseek" and not Config.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is required when AI_PROVIDER is deepseek")
        if Config.AI_PROVIDER == "douban" and not Config.DOUBAN_API_KEY:
            raise ValueError("DOUBAN_API_KEY is required when AI_PROVIDER is douban")
        if Config.AI_PROVIDER == "ark" and not Config.ARK_API_KEY:
            raise ValueError("ARK_API_KEY is required when AI_PROVIDER is ark")
        if Config.AI_PROVIDER == "agnes" and not Config.AGNES_API_KEY:
            raise ValueError("AGNES_API_KEY is required when AI_PROVIDER is agnes")
        
        required_smtp_fields = ["SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_SENDER"]
        for field in required_smtp_fields:
            if not getattr(Config, field):
                raise ValueError(f"{field} is required for email sending")
        
        if not Config.SMTP_RECIPIENTS:
            raise ValueError("SMTP_RECIPIENTS is required")
