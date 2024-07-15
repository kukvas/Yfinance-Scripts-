import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
def fetch_stock_data(ticker, start_year, end_year):
    """
    Fetches stock data and the full name of the stock from the start of the start_year to the end of the end_year.
    """
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    try:
        full_name = stock.info['longName']
    except KeyError:
        full_name = ticker  # Fallback to ticker if full name not found
    return data, full_name
def calculate_total_percentage_change(data):
    """
    Calculates the total percentage change from the first to the last data point
    """
    if not data.empty:
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        return (end_price - start_price) / start_price * 100
    else:
        return None
def plot_histogram(years, changes, ticker, total_change, full_name):
    """
    Plots a histogram of the annual percentage changes using Seaborn with text labels above the bars.
    """
    plt.figure(figsize=(13, 7))
    
    # Define colors for positive and negative changes
    colors = ["skyblue" if change >= 0 else "#F6BDBD" for change in changes]
    bars = sns.barplot(x=years, y=changes, palette=colors)

    # Add the text labels above the bars
    for bar, label in zip(bars.patches, changes):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{label:.2f}%',  # Adjust offset as needed
                 ha='center', va='bottom', color='black')
    # Determine sign for total change
    sign = '+' if total_change >= 0 else ''
    plt.title(f'{full_name} ({ticker}) Annual Percentage Changes (Total: {sign}{total_change:.2f}%)')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change')
    plt.show()
def main():
    ticker = input("Enter the stock ticker symbol: ")
    start_year = int(input("Enter the start year for comparison: "))
    end_year = int(input("Enter the end year for comparison: "))
    years = list(range(start_year, end_year + 1))
    percentage_changes = []
    total_data, full_name = fetch_stock_data(ticker, start_year, end_year)
    total_change = calculate_total_percentage_change(total_data)
    for year in years:
        annual_data = total_data[total_data.index.year == year]
        change = calculate_total_percentage_change(annual_data)
        if change is not None:
            percentage_changes.append(change)
        else:
            percentage_changes.append(0)
    plot_histogram(years, percentage_changes, ticker, total_change, full_name)
if __name__ == "__main__":
    main()
