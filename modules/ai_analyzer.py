import json
import logging
from datetime import datetime

import openai
import requests

logger = logging.getLogger(__name__)


class DeepSeekAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

    def analyze(self, market_data):
        prompt = self._build_prompt(market_data)
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位专业的金融分析师，擅长分析股票市场数据并给出专业的投资建议。请用中文输出分析报告。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            return f"AI分析失败: {str(e)}"

    def _build_prompt(self, market_data):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        ashare_sectors = market_data.get("ashare", {}).get("sector_index", [])
        
        top_gainers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0), reverse=True)[:10]
        top_losers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0))[:10]

        prompt = f"""
你是一位专业的A股市场分析师，擅长基于板块数据进行深度分析。请根据以下数据，撰写一份完整、专业、详细的每日市场分析报告。

【分析日期】{date}

【A股板块涨幅榜TOP10】
{self._format_sectors(top_gainers_ashare)}

【A股板块跌幅榜TOP10】
{self._format_sectors(top_losers_ashare)}

请按照以下严格的结构输出分析报告，每个部分都必须详细展开，不能简略：

## 一、市场概览
- 当日市场整体走势（上涨/下跌家数对比）
- 市场情绪判断（乐观/谨慎/悲观）
- 成交量和资金流向分析
- 整体风格判断（价值/成长/周期）

## 二、A股市场分析
### 领涨板块深度解读
- 列出涨幅前三的板块
- 分析每个板块上涨的核心驱动因素（政策面、基本面、资金面）
- 相关行业动态和新闻事件
- 板块内部个股表现差异

### 领跌板块深度解读
- 列出跌幅前三的板块
- 分析每个板块下跌的核心原因（政策利空、业绩不及预期、资金出逃等）
- 板块面临的压力和风险
- 技术性调整还是趋势性下跌判断

## 三、热点板块解读
- 选取3-5个表现最突出的板块进行深入分析
- 每个板块包含：驱动逻辑、市场预期、风险提示、相关龙头股表现
- 板块间的联动关系分析

## 四、投资建议
### 短期建议（1-2周）
- 推荐关注的板块及理由
- 建议规避的板块及理由
- 仓位建议

### 中期建议（1-3个月）
- 行业配置方向
- 主题投资机会
- 风险提示

要求：
1. 分析必须基于提供的数据，结合市场常识进行合理推断
2. 语言专业但易懂，避免过于技术性的术语堆砌
3. 每个部分都要有具体内容，不能空洞泛泛而谈
4. 不要提及港股和美股相关内容
5. 报告结构清晰，使用Markdown格式输出
"""
        return prompt

    def _format_sectors(self, sectors):
        lines = []
        for i, sector in enumerate(sectors, 1):
            name = sector.get("name", "N/A")
            change = sector.get("change_percent", 0)
            price = sector.get("close", sector.get("value", "N/A"))
            volume = sector.get("volume", "N/A")
            lines.append(f"{i}. {name}: 涨跌幅 {change:.2f}%, 收盘价 {price}, 成交量 {volume}")
        return "\n".join(lines) if lines else "暂无数据"


class DoubanAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.douban.com/v1/chat/completions"

    def analyze(self, market_data):
        prompt = self._build_prompt(market_data)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "doubao-pro",
                "messages": [
                    {"role": "system", "content": "你是一位专业的金融分析师，擅长分析股票市场数据并给出专业的投资建议。请用中文输出分析报告。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 3000
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"Douban API error: {e}")
            return f"AI分析失败: {str(e)}"

    def _build_prompt(self, market_data):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        ashare_sectors = market_data.get("ashare", {}).get("sector_index", [])
        
        top_gainers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0), reverse=True)[:10]
        top_losers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0))[:10]

        prompt = f"""
你是一位专业的A股市场分析师，擅长基于板块数据进行深度分析。请根据以下数据，撰写一份完整、专业、详细的每日市场分析报告。

【分析日期】{date}

【A股板块涨幅榜TOP10】
{self._format_sectors(top_gainers_ashare)}

【A股板块跌幅榜TOP10】
{self._format_sectors(top_losers_ashare)}

请按照以下严格的结构输出分析报告，每个部分都必须详细展开，不能简略：

## 一、市场概览
- 当日市场整体走势（上涨/下跌家数对比）
- 市场情绪判断（乐观/谨慎/悲观）
- 成交量和资金流向分析
- 整体风格判断（价值/成长/周期）

## 二、A股市场分析
### 领涨板块深度解读
- 列出涨幅前三的板块
- 分析每个板块上涨的核心驱动因素（政策面、基本面、资金面）
- 相关行业动态和新闻事件
- 板块内部个股表现差异

### 领跌板块深度解读
- 列出跌幅前三的板块
- 分析每个板块下跌的核心原因（政策利空、业绩不及预期、资金出逃等）
- 板块面临的压力和风险
- 技术性调整还是趋势性下跌判断

## 三、热点板块解读
- 选取3-5个表现最突出的板块进行深入分析
- 每个板块包含：驱动逻辑、市场预期、风险提示、相关龙头股表现
- 板块间的联动关系分析

## 四、投资建议
### 短期建议（1-2周）
- 推荐关注的板块及理由
- 建议规避的板块及理由
- 仓位建议

### 中期建议（1-3个月）
- 行业配置方向
- 主题投资机会
- 风险提示

要求：
1. 分析必须基于提供的数据，结合市场常识进行合理推断
2. 语言专业但易懂，避免过于技术性的术语堆砌
3. 每个部分都要有具体内容，不能空洞泛泛而谈
4. 不要提及港股和美股相关内容
5. 报告结构清晰，使用Markdown格式输出
"""
        return prompt

    def _format_sectors(self, sectors):
        lines = []
        for i, sector in enumerate(sectors, 1):
            name = sector.get("name", "N/A")
            change = sector.get("change_percent", 0)
            price = sector.get("close", sector.get("value", "N/A"))
            volume = sector.get("volume", "N/A")
            lines.append(f"{i}. {name}: 涨跌幅 {change:.2f}%, 收盘价 {price}, 成交量 {volume}")
        return "\n".join(lines) if lines else "暂无数据"


class ArkAnalyzer:
    def __init__(self, api_key, model="doubao-3.5"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        self.available_models = ["doubao-3.5", "doubao-lite", "doubao-pro"]

    def analyze(self, market_data):
        prompt = self._build_prompt(market_data)
        
        for model_attempt in [self.model] + [m for m in self.available_models if m != self.model]:
            try:
                response = self.client.chat.completions.create(
                    model=model_attempt,
                    messages=[
                        {"role": "system", "content": "你是一位专业的金融分析师，擅长分析股票市场数据并给出专业的投资建议。请用中文输出分析报告。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                
                if model_attempt != self.model:
                    logger.info(f"Successfully used fallback model: {model_attempt}")
                return response.choices[0].message.content.strip()
            except Exception as e:
                if "NotFound" in str(e) or "InvalidEndpointOrModel" in str(e):
                    logger.warning(f"Model {model_attempt} not found, trying next model...")
                    continue
                else:
                    logger.error(f"Ark API error with model {model_attempt}: {e}")
                    return f"AI分析失败: {str(e)}\n\n请检查.env文件中的ARK_MODEL配置是否正确。火山引擎Ark平台常用模型名称包括: doubao-3.5, doubao-lite"

    def _build_prompt(self, market_data):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        ashare_sectors = market_data.get("ashare", {}).get("sector_index", [])
        hk_index = market_data.get("ashare", {}).get("hk_index", [])
        us_indices = market_data.get("global", {}).get("us_indices", [])
        
        top_gainers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0), reverse=True)[:5]
        top_losers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0))[:5]

        prompt = f"""
请根据以下股票市场数据，撰写一份专业的每日市场分析报告。

【分析日期】{date}

【A股板块涨幅榜TOP5】
{self._format_sectors(top_gainers_ashare)}

【A股板块跌幅榜TOP5】
{self._format_sectors(top_losers_ashare)}

【港股主要指数表现】
{self._format_indices(hk_index)}

【美股主要指数表现】
{self._format_indices(us_indices)}

请按照以下结构输出分析报告：

1. 市场概览：简要总结当日全球市场整体表现
2. A股市场分析：分析A股各板块的涨跌情况及原因
3. 港股市场分析：分析港股主要指数表现
4. 美股市场分析：分析美股三大指数表现
5. 热点板块解读：深入分析表现突出的板块及其背后逻辑
6. 投资建议：基于数据分析给出短期和中期投资建议

请用专业但易懂的语言撰写，避免过于技术性的术语。
"""
        return prompt


class AgnesAnalyzer:
    def __init__(self, api_key, model="agnes-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://apihub.agnes-ai.com/v1"
        )

    def analyze(self, market_data):
        prompt = self._build_prompt(market_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的金融分析师，擅长分析股票市场数据并给出专业的投资建议。请用中文输出分析报告。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Agnes AI API error: {e}")
            return f"AI分析失败: {str(e)}\n\n请检查.env文件中的AGNES_API_KEY配置是否正确。Agnes AI模型名称: agnes-2.0-flash"

    def _build_prompt(self, market_data):
        date = market_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        ashare_sectors = market_data.get("ashare", {}).get("sector_index", [])
        
        top_gainers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0), reverse=True)[:10]
        top_losers_ashare = sorted(ashare_sectors, key=lambda x: x.get("change_percent", 0))[:10]

        prompt = f"""
你是一位专业的A股市场分析师，擅长基于板块数据进行深度分析。请根据以下数据，撰写一份完整、专业、详细的每日市场分析报告。

【分析日期】{date}

【A股板块涨幅榜TOP10】
{self._format_sectors(top_gainers_ashare)}

【A股板块跌幅榜TOP10】
{self._format_sectors(top_losers_ashare)}

请按照以下严格的结构输出分析报告，每个部分都必须详细展开，不能简略：

## 一、市场概览
- 当日市场整体走势（上涨/下跌家数对比）
- 市场情绪判断（乐观/谨慎/悲观）
- 成交量和资金流向分析
- 整体风格判断（价值/成长/周期）

## 二、A股市场分析
### 领涨板块深度解读
- 列出涨幅前三的板块
- 分析每个板块上涨的核心驱动因素（政策面、基本面、资金面）
- 相关行业动态和新闻事件
- 板块内部个股表现差异

### 领跌板块深度解读
- 列出跌幅前三的板块
- 分析每个板块下跌的核心原因（政策利空、业绩不及预期、资金出逃等）
- 板块面临的压力和风险
- 技术性调整还是趋势性下跌判断

## 三、热点板块解读
- 选取3-5个表现最突出的板块进行深入分析
- 每个板块包含：驱动逻辑、市场预期、风险提示、相关龙头股表现
- 板块间的联动关系分析

## 四、投资建议
### 短期建议（1-2周）
- 推荐关注的板块及理由
- 建议规避的板块及理由
- 仓位建议

### 中期建议（1-3个月）
- 行业配置方向
- 主题投资机会
- 风险提示

要求：
1. 分析必须基于提供的数据，结合市场常识进行合理推断
2. 语言专业但易懂，避免过于技术性的术语堆砌
3. 每个部分都要有具体内容，不能空洞泛泛而谈
4. 不要提及港股和美股相关内容
5. 报告结构清晰，使用Markdown格式输出
"""
        return prompt

    def _format_sectors(self, sectors):
        lines = []
        for i, sector in enumerate(sectors, 1):
            name = sector.get("name", "N/A")
            change = sector.get("change_percent", 0)
            price = sector.get("close", sector.get("value", "N/A"))
            volume = sector.get("volume", "N/A")
            lines.append(f"{i}. {name}: 涨跌幅 {change:.2f}%, 收盘价 {price}, 成交量 {volume}")
        return "\n".join(lines) if lines else "暂无数据"


class AIAnalyzer:
    def __init__(self, provider, api_key, model=None):
        self.provider = provider
        self.api_key = api_key
        
        if provider == "deepseek":
            self.analyzer = DeepSeekAnalyzer(api_key)
        elif provider == "douban":
            self.analyzer = DoubanAnalyzer(api_key)
        elif provider == "ark":
            self.analyzer = ArkAnalyzer(api_key, model=model or "doubao-3.5")
        elif provider == "agnes":
            self.analyzer = AgnesAnalyzer(api_key, model=model or "agnes-2.0-flash")
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    def analyze(self, market_data):
        logger.info(f"Starting AI analysis with {self.provider}...")
        report = self.analyzer.analyze(market_data)
        logger.info("AI analysis completed")
        return report

    def save_report(self, report, data_dir):
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"analysis_report_{date_str}.txt"
        filepath = f"{data_dir}/{filename}"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Analysis report saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return None
