import yfinance as yf
import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)



def get_stock_info(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol).info
        market_price = ticker.get('currentPrice', 'N/A')
        previous_close_price = ticker.get('regularMarketPreviousClose', 'N/A')

        return {
            'ticker': ticker_symbol,
            'market_price': market_price,
            'previous_close_price': previous_close_price
        }

    except yf.errors.YFinanceError as yfe:
        if "404 Client Error" in str(yfe):
            print(f"LangChain prompt for {ticker_symbol}: No stock information found for this ticker symbol.")
            return {'warning': f"No stock information found for {ticker_symbol}"}
        else:
            print(f"Other YFinanceError: {yfe}")
            return {'error': f"An error occurred while retrieving stock info for {ticker_symbol}"}

