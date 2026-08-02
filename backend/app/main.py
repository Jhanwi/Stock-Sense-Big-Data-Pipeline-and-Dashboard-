import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

from app.models import PipelineTriggerRequest, PipelineStatusResponse, StockDataSnapshot, HistoricalPricePoint
from app.spark_executor import execute_distributed_etl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("stock_sense_api")

app = FastAPI(title="Stock Sense API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/v1/stocks/snapshot/{exchange}/{ticker}", response_model=StockDataSnapshot)
async def get_ticker_snapshot(exchange: str, ticker: str):
    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    symbol = f"{ticker.upper()}{suffix}"
    
    try:
        t = yf.Ticker(symbol)
        info = t.info
        
        if not info or 'longName' not in info:
            raise HTTPException(status_code=404, detail="Stock symbol not found or invalid.")
            
        hist_df = t.history(period="1mo", interval="1d")
        chart_payload = []
        
        if not hist_df.empty:
            hist_df = hist_df.reset_index()
            for _, row in hist_df.iterrows():
                if pd.isna(row['Close']) or pd.isna(row['Open']):
                    continue
                chart_payload.append(
                    HistoricalPricePoint(
                        date=row['Date'].strftime('%b %d'),
                        open=round(float(row['Open']), 2),
                        close=round(float(row['Close']), 2),
                        high=round(float(row['High']), 2),
                        low=round(float(row['Low']), 2)
                    )
                )

        mcap = info.get("marketCap", 0)
        mcap_formatted = f"₹{mcap/10000000:,.2f} Cr" if mcap >= 10000000 else f"₹{mcap:,.2f}"
        
        return StockDataSnapshot(
            company_name=info.get("longName", ticker),
            ticker=ticker.upper(),
            ltp=info.get("currentPrice") or info.get("regularMarketPrice"),
            open_price=info.get("open") or info.get("regularMarketOpen"),
            day_high=info.get("dayHigh"),
            day_low=info.get("dayLow"),
            market_cap_formatted=mcap_formatted,
            historical_series=chart_payload
        )
    except Exception as e:
        logger.error(f"Error fetching ticker snapshot for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error processing stock data.")

@app.post("/api/v1/pipeline/ingest", response_model=PipelineStatusResponse)
async def trigger_pipeline_ingestion(payload: PipelineTriggerRequest, background_tasks: BackgroundTasks):
    try:
        execution_duration = execute_distributed_etl(
            ticker=payload.ticker, exchange=payload.exchange, s3_bucket=payload.s3_bucket
        )
        return PipelineStatusResponse(
            status="SUCCESS", ticker=payload.ticker, exchange=payload.exchange,
            message="Raw records successfully processed and saved to S3 Parquet partitions.", execution_time_seconds=execution_duration
        )
    except Exception as e:
        logger.error(f"ETL pipeline run failed for {payload.ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")

