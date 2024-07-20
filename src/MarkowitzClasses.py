from random import randrange
from datetime import datetime
import json
import re
import pandas as pd
import yfinance as yf
from pyetfdb_scraper.etf import ETF, load_etfs
from utils import extract_percent

ETF_FILE = 'data/etf_returns.json'
USER_AGENT_FILE = 'data/user-agents.txt'
RETURN_PERIODS = ['1_month_return',
                  '3_month_return',
                  'ytd_return',
                  '1_year_return',
                  '3_year_return',
                  '5_year_return']
STOCK_HORIZON = '5y'

class MarkowitzOptimizer:
    def __init__(self, stocks: list[tuple[str, str]]):
        self.stocks = stocks

    def get_user_agents(self) -> list[str]:
        """Retrieve list of all randomized user agents"""
        user_agent_list = []
        with open(USER_AGENT_FILE) as text_file:
            for line in text_file:
                user_agent_list.append(line)
        return user_agent_list

    def should_update_data(self) -> bool:
        """Check if the ETF returns data should be updated by looking at last download date metadata"""
        with open(ETF_FILE, encoding='utf-8', mode='r') as file:  # encoding parameter for windows machines
            etf_dict = json.load(file)
            last_date = datetime.strptime(etf_dict['download_date'], '%m/%d/%y %H:%M:%S')
        return (datetime.now() - last_date).days > 28

    def update_etf_data(self) -> None:
        """Update the file containing monthly ETF return data"""
        full_etf_list = load_etfs()
        user_agent_list = self.get_user_agents()
        user_agent_count = len(user_agent_list)
        etf_dict = {}
        for etf_symbol in full_etf_list[0:100]:
            user_agent = user_agent_list[randrange(user_agent_count)]  # use a random user agent each time
            etf = ETF(etf_symbol, user_agent)
            curr_dict = {}
            for horizon in RETURN_PERIODS:
                for time_data in etf.performance:
                    if horizon in time_data:
                        return_val = time_data[horizon]
                        curr_dict[horizon] = return_val
            etf_dict[etf_symbol] = curr_dict
        etf_dict['download_date'] = datetime.now().strftime('%m/%d/%y %H:%M:%S')
        with open(ETF_FILE, encoding='utf-8', mode='w') as file:
            json.dump(etf_dict, file, ensure_ascii = False)
        return etf_dict
    
    def historical_returns(self, stock_name: str) -> list[int]:
        """Produces a list containing the 6 (annualized) returns in percent"""
        stock_obj = yf.Ticker(stock_name)
        stock_df = stock_obj.history(period=STOCK_HORIZON)
        print(stock_df['Close']['2019-07-22 00:00:00-04:00'])

    def compute_portfolio_variance(self) -> int:
        return 0

    def suggest_etfs(self):
        if self.should_update_data():
            self.update_etf_data()
        with open(ETF_FILE, encoding='utf-8', mode='r') as file:
            etf_dict = json.load(file)
        returns_matrix = []
        for etf in etf_dict:
            if etf == 'download_date':
                continue
            returns_list = []
            for horizon in RETURN_PERIODS:
                returns_list.append(extract_percent(etf_dict[etf][horizon]))
            returns_matrix.append(returns_list)
        for stock in self.stocks:
            stock_name = stock[0]
            shares = stock[1]
            returns_list = self.historical_returns(stock_name)
            returns_matrix.append(returns_list)