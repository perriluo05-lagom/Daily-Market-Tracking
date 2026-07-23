import json
import logging
import os
import sys
from datetime import datetime

os.environ['NO_PROXY'] = '*'

import akshare as ak

logger = logging.getLogger(__name__)


class AShareDataCollector:
    def __init__(self):
        self.ak = ak

    def get_sector_index(self):
        try:
            df = self.ak.stock_sector_spot()
            results = []
            for _, row in df.iterrows():
                results.append({
                    "name": row.get("板块", row.get("name", "N/A")),
                    "close": row.get("平均价格", row.get("close", row.get("value", 0))),
                    "change": row.get("涨跌额", 0),
                    "change_percent": row.get("涨跌幅", 0),
                    "volume": row.get("总成交量", row.get("volume", "N/A")),
                    "amount": row.get("总成交额", "N/A")
                })
            return results
        except Exception as e:
            logger.error(f"Failed to get A-share sector index: {e}")
            return []

    def collect_all(self):
        logger.info("Collecting A-share data...")
        sector_data = self.get_sector_index()
        top_gainers = sorted(sector_data, key=lambda x: x.get("change_percent", 0), reverse=True)[:10]
        top_losers = sorted(sector_data, key=lambda x: x.get("change_percent", 0))[:10]
        
        data = {
            "sector_index": sector_data,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Successfully collected A-share data")
        return data


class DataCollector:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.ashare_collector = AShareDataCollector()

    def collect(self):
        logger.info("Starting data collection...")
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "ashare": self.ashare_collector.collect_all()
        }
        return data

    def save_data(self, data):
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"market_data_{date_str}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            return None

    def load_data(self, date_str=None):
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        
        filename = f"market_data_{date_str}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Data loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return None
