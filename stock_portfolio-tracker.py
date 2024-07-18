import yfinance as yf
import pandas as pd
import datetime

class StockPortfolioTracker:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, ticker, quantity, purchase_date):
        """
        Adds a stock to the portfolio.

        Args:
            ticker: The stock ticker symbol.
            quantity: The number of shares purchased.
            purchase_date: The date of purchase in YYYY-MM-DD format.
        """
        if ticker not in self.portfolio:
            self.portfolio[ticker] = {
                "quantity": quantity,
                "purchase_date": datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date(),
                "purchase_price": self.get_historical_price(ticker, purchase_date),
                "current_price": self.get_historical_price(ticker, purchase_date) # Add current_price
            }
        else:
            print(f"Stock {ticker} already exists in the portfolio.")

    def get_historical_price(self, ticker, date):
        """
        Retrieves the historical price of a stock on a specific date.

        Args:
            ticker: The stock ticker symbol.
            date: The date in YYYY-MM-DD format.

        Returns:
            The historical price on the specified date.
        """
        try:
            data = yf.download(ticker, start=date, end=date)
            return data["Adj Close"][0]
        except Exception as e:
            print(f"Error retrieving historical price for {ticker}: {e}")
            return None

    def update_portfolio(self):
        """
        Updates the portfolio with current stock prices.
        """
        today = datetime.date.today()
        for ticker in self.portfolio:
            current_price = self.get_historical_price(ticker, today.strftime("%Y-%m-%d"))
            if current_price is not None:
                self.portfolio[ticker]["current_price"] = current_price

    def calculate_returns(self):
        """
        Calculates the returns for each stock in the portfolio.
        """
        for ticker in self.portfolio:
            purchase_price = self.portfolio[ticker]["purchase_price"]
            current_price = self.portfolio[ticker]["current_price"]
            if current_price is not None:
                return_percentage = ((current_price - purchase_price) / purchase_price) * 100
                self.portfolio[ticker]["return_percentage"] = return_percentage

    def print_portfolio(self):
        """
        Prints the current state of the portfolio.
        """
        print("\nPortfolio Summary:")
        print("-" * 30)
        for ticker, data in self.portfolio.items():
            print(f"Ticker: {ticker}")
            print(f"  Quantity: {data['quantity']}")
            print(f"  Purchase Date: {data['purchase_date']}")
            print(f"  Purchase Price: ${data['purchase_price']:.2f}")
            if "current_price" in data:
                print(f"  Current Price: ${data['current_price']:.2f}")
                if "return_percentage" in data:
                    print(f"  Return: {data['return_percentage']:.2f}%")
            print("-" * 30)

    def main(self):
        """
        Main function to interact with the portfolio tracker.
        """
        while True:
            print("\nPortfolio Tracker Menu:")
            print("1. Add Stock")
            print("2. Update Portfolio")
            print("3. Calculate Returns")
            print("4. Print Portfolio")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                ticker = input("Enter stock ticker: ")
                quantity = int(input("Enter quantity: "))
                purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
                self.add_stock(ticker, quantity, purchase_date)
            elif choice == '2':
                self.update_portfolio()
            elif choice == '3':
                self.calculate_returns()
            elif choice == '4':
                self.print_portfolio()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    portfolio_tracker = StockPortfolioTracker()
    portfolio_tracker.main()
