import time, threading
import http.client
import json
from os import system, name
import array
import keyboard

from pynput.keyboard import Key, Listener

from gateAPI import GateIO

fileObject = open("config.txt", "r")

data = fileObject.read()

config_data = json.loads(data)

# apiKey APISECRET
apiKey = config_data['apiKey']
secretKey = config_data['secretKey']

# address
btcAddress = config_data['btcAddress']
              

# Provide constants

API_QUERY_URL = 'data.gateio.life'
API_TRADE_URL = 'api.gateio.life'

# Create a gate class instance

gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)

StartTime=time.time()
init_value = 0
init_pair=[]
status = 0
buy_pair = ''
buy_rate = 0
current_balance_usdt = 0.
trad_start_time = 0
buy_amount = 0
max_percentage = 0
max_pair = ''
max_number = 0
max_amount = 0
max_rate = 0

Exit_sell = 0

def action() :
    global init_pair
    global init_value
    global status
    global StartTime
    global buy_pair
    global buy_rate
    global current_balance_usdt
    global trad_start_time
    global buy_amount
    global max_percentage
    global max_pair
    global max_number
    global max_amount
    global max_rate
    
    go_to_buy = 0
    
    # print(chr(27) + "[2J")
    # print('action ! -> time : {:.1f}s'.format(time.time()-StartTime))
    # print(time.time()-StartTime)
    conn = http.client.HTTPSConnection("data.gateapi.io")
    payload = ''
    headers = {}
    conn.request("GET", "/api2/1/marketlist", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    
    
    if (float(config_data['scanned_timeframe_seconds']) <= (time.time()-StartTime)):
        go_to_buy = 1

    if init_value == 0:
        print('%-10s %-20s %-15s %-22s %-22s' % ('Number', 'Pair', 'Rate', 'Percent', 'Volume'))
        file1 = open("init_val.txt","w")
        init_pair = data['data']
        for i in data['data']:
            pair_name = i['pair'].split('_')[1]
            if pair_name == 'usdt':
                L = [str(i['no']), " ",str(i['pair']), " ", str(i['rate']), " \n"]
                file1.writelines(L)
        file1.close() #to change file access modes

    global exitTrad
    # print(config_data['entry_variation_percentage'])
    keyboard.on_press_key('q', lambda _:exitTrad())
    def exitTrad():
        if status == 0:
            exit()

    init_value = 1
    if status == 0:
        max_percentage = -10.0
        max_pair = ''
        max_number = 0
        max_amount = 0
        max_rate = 0.0
        for i in data['data']:
            pair_name = i['pair'].split('_')[1]

            if pair_data['pair_name'] == i['pair']:
            
                for j in init_pair:
                    
                    
                    if i['pair'] == j['pair'] and float(i['rate']) != 0.0 and float(j['rate']) != 0.0 and float(i['vol_a']) > 0.0:
                        percent = (float(i['rate'])/float(j['rate']) - 1.0) * 100
                        
                        if max_percentage < percent:
                            max_percentage = percent
                            max_number = int(i['no'])
                            max_pair = i['pair']
                            max_rate = float(i['rate'])
                            buy_rate = float(i['rate'])
                            max_amount = float(i['vol_a'])
                #         # percent is small than config entry percent
                #         if percent < float(config_data['entry_variation_percentage']):
                            
                #             # print scan value
                #             print('%-10s %-20s %-15s %-22s %-22s' % (i['no'], i['pair'], i['rate'], percent, i['vol_a']))
                                
                #         # percent is big than config entry percent and status is scan 
                #         elif status == 0:
                #             buy_pair = i['pair']
                #             buy_rate = float(i['rate'])
                #             print('buy', i['pair'], percent, '       ', j['rate'], i['vol_a'])
                #             current_balance_usdt = json.loads(gate_trade.balances())
                #             amount = current_balance_usdt['available']['USDT']
                #             # amount = '1.00'
                #             # print(gate_trade.buy(i['pair'], float(amount)*float(config_data['entry_balance_percentage'])/100, float(amount)/(float(i['rate'])*(1+float(config_data['market_slippage_percentage'])/100))))
                #             buy_amount = float(amount)/(float(i['rate'])*(1+float(config_data['market_slippage_percentage'])/100))
                #             print('Buying by percentage',buy_pair, buy_rate, buy_amount)
                #             trad_start_time = time.time()
                #             status = 1
                #             break
                        
                # if status == 1:
                #     break

        # percent is big than config entry percent and status is scan 
        if go_to_buy == 0:
            print('%-10s %-20s %-15s %-22s %-22s' % (max_number, max_pair, max_rate, round(max_percentage, 2), max_amount))
        if max_percentage > float(config_data['entry_variation_percentage']):
            print("buy", max_percentage, max_pair)
            buy_pair = max_pair
            status = 1
            current_balance_usdt = json.loads(gate_trade.balances())
            amount = current_balance_usdt['available']['USDT']
            
            # amount = '1.00'
            print(gate_trade.buy(max_pair, float(amount)*float(config_data['entry_balance_percentage'])/100, float(amount)/(max_rate*(1+float(config_data['market_slippage_percentage'])/100))))
            buy_amount = float(amount)/(max_rate*(1+float(config_data['market_slippage_percentage'])/100))
            print('Buying by Percentage', buy_pair, max_rate, buy_amount)
            trad_start_time = time.time()
            go_to_buy = 0

        # time is reached 
        if go_to_buy == 1:
            print("buy", max_percentage, max_pair)
            buy_pair = max_pair
            status = 1
            current_balance_usdt = json.loads(gate_trade.balances())
            amount = current_balance_usdt['available']['USDT']
            
            # amount = '1.00'
            print(gate_trade.buy(max_pair, float(amount)*float(config_data['entry_balance_percentage'])/100, float(amount)/(max_rate*(1+float(config_data['market_slippage_percentage'])/100))))
            buy_amount = float(amount)/(max_rate*(1+float(config_data['market_slippage_percentage'])/100))
            print('Buying by Time_limit', buy_pair, max_rate, buy_amount)
            trad_start_time = time.time()
            go_to_buy = 0

    elif status == 1:
        for k in data['data']:
            if buy_pair == k['pair']:
                # print(time.time()-trad_start_time, Exit_sell)
                percent = (float(k['rate'])/buy_rate - 1.0) * 100
                print('%-10s %-20s %-15s %-22s %-22s' % (k['no'], k['pair'], k['rate'], round(percent, 2), k['vol_a']))
                if float(config_data['take_profit_percentage']) < percent:
                    
                    print(gate_trade.sell(buy_pair, buy_amount, buy_amount*(k['rate']*(1-float(config_data['market_slippage_percentage']/100)))))
                    StartTime = time.time()
                    status = 0
                    init_value = 0
                    print('Selling by take profit percentage', k['pair'], k['rate'], buy_amount)
                    break
                elif float(config_data['stop_loss_percentage']) > percent:
                    print(gate_trade.sell(buy_pair, buy_amount, buy_amount*(k['rate']*(1-float(config_data['market_slippage_percentage']/100)))))
                    status = 0
                    StartTime = time.time()
                    init_value = 0
                    print('Selling by take profit percentage', k['pair'], k['rate'], buy_amount)
                    break
                elif float(config_data['program_execution_time_limit_seconds']) <= (time.time()-trad_start_time):
                    print(gate_trade.sell(buy_pair, buy_amount, buy_amount*(k['rate']*(1-float(config_data['market_slippage_percentage']/100)))))
                    status = 0
                    StartTime = time.time()
                    init_value = 0
                    print('Selling by take profit percentage', k['pair'], k['rate'], buy_amount)
                    break
                keyboard.on_press_key('q', lambda _:exitTrad())
                def exitTrad():
                    print('sell', buy_amount, k['rate'])
                    print(gate_trade.sell(buy_pair, buy_amount, buy_amount*(k['rate']*(1-float(config_data['market_slippage_percentage']/100)))))
                    status = 0
                    StartTime = time.time()
                    init_value = 0
                    print('Selling by take profit percentage', k['pair'], k['rate'], buy_amount)
                    
                    

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

# open config file & read data


with open('pair_data.json') as f:
    pair_data = json.load(f)

# # start action every 0.6s
inter=setInterval(int(config_data['trade_refresh_speed_ms'])/1000, action)

# will stop interval in 2s
t=threading.Timer(int(pair_data['exit_hour']),inter.cancel)
t.start()


