
import yfinance as yf

def get_stock_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol).info
    market_price = ticker.get('currentPrice', 'N/A')
    previous_close_price = ticker.get('regularMarketPreviousClose', 'N/A')

    return {
        'ticker': ticker_symbol,
        'market_price': market_price,
        'previous_close_price': previous_close_price
    }