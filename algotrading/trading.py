import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import datetime
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import json
import websocket
import asyncio


class trading:
    
    def display(self):
        account = self.client.get_account()
        print("--------ACCOUNT INFORMATION--------")
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        print('Portfolio Value: ${:.2f}'.format(float(account.portfolio_value))+'\n'+
              'Cash: ${:.2f}'.format(float(account.cash))+'\n'+
              'Buying Power: ${:.2f}'.format(float(account.buying_power))+'\n'+
              'Status: {}'.format(account.status)+'\n'+
              'Equity: ${:.2f}'.format(float(account.long_market_value+account.short_market_value))+'\n'+
              'Daily Change: ${:.2f}'.format(float(account.equity)-float(account.last_equity))+'\n')
        
    def positions(self):
        data = self.client.get_all_positions()
        print("--------POSITIONS--------")
        positions = pd.DataFrame(columns=['Symbol','Qty','Avg Entry Price','Current Price','Market Value','Unrealized P/L'])
        positions['Symbol'] = [data[i].symbol for i in range(len(data))]
        positions['Qty'] = ["{:.2f}".format(float(data[i].qty)) for i in range(len(data))]
        positions['Avg Entry Price'] = ["{:.2f}".format(float(data[i].avg_entry_price)) for i in range(len(data))]
        positions['Current Price'] = ["{:.2f}".format(float(data[i].current_price)) for i in range(len(data))]
        positions['Market Value'] = ["{:.2f}".format(float(data[i].market_value)) for i in range(len(data))]
        positions['Unrealized P/L'] = ["{:.2f}".format(float(data[i].unrealized_pl)) for i in range(len(data))]
        print(positions)
        
    def buy(self, symbol, qty):
        market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
        market_order = self.client.submit_order(market_order_data)
        
    def sell(self, symbol, qty):
        market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
        market_order = self.client.submit_order(market_order_data)

    def stream(self):
        websocket_url = 'wss://paper-api.alpaca.markets/stream'
        ws = websocket.WebSocket()
        auth_message = {
            'action': 'authenticate',
            'data': {
                'key_id': self.API_KEY,
                'secret_key': self.API_SECRET
            }
        }
        listen_message = {
            'action': 'listen',
            'data': {
                'streams': ['account_updates']
            }
        }
        
        
        
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.API_SECRET = os.getenv("API_SECRET")
        self.BASE_URL = os.getenv("APCA_API_BASE_URL")
        self.client = TradingClient(self.API_KEY, self.API_SECRET)
        self.display()
        self.stream()
        
# bot = trading()
# bot.positions()

def on_message(ws, message):
    data = json.loads(message)
    for x in data:
        print(x['S']+": ${:.2f}".format(x['bp']))
def on_open(ws):
    load_dotenv()
    
    # Create the authentication message
    auth_message = {"action": "auth","key": "PK1DDRUA0TIK3D7JI154","secret": "5xcLDJfOIGksdng2tlGnGzRZbq0QKEIXuQSI70pH"}
    
    # Send the authentication message to the server
    ws.send(json.dumps(auth_message))
        
    # Create the listen message
    listen_message = {"action":"subscribe","trades":["BTC/USD"],"quotes":["BTC/USD"],"bars":["BTC/USD"]}
    
    ws.send(json.dumps(listen_message))
    
if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://stream.data.alpaca.markets/v1beta2/crypto",
                                on_open=on_open,
                                on_message=on_message
                                )
    ws.run_forever()