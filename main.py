import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests
from json import dumps, loads, load as jsonload

# v1.1

root = tk.Tk()
root.title("BeedKoen")
root.geometry("500x500")

url = 'https://api.coingecko.com/api/v3/simple/price'
headers = { 'x-cg-demo-api-key': 'YOUR_API_KEY' }

labels = []
coins = ('Bitcoin', 'FPI-BANK', 'Toncoin')
prices = {'Bitcoin': 0,
          'FPI-BANK': 0,
          'Toncoin': 0}
balance = {'USD': 100,
           'Bitcoin': 0,
           'FPI-BANK': 0,
           'Toncoin': 0}

def update_response():
    response = requests.get(url, params = {  
            'ids': ','.join(coins).lower(),
            'vs_currencies': 'USD'
    }) 
    if response.status_code == 200:
        print(response.json())

        # price = lambda coin: response.json().get(coin, {}).get('usd', 'undefined')
        for i in prices:
            prices[i] = response.json().get(i.lower(), {}).get('usd', '-')

        #                                                                            toncoin pls work, allah hear me
        return (f"BTC: {prices['Bitcoin']}", f"FPI: {prices['FPI-BANK']}", f"TON: {prices['Toncoin']}")
    else:
        print(f'HTTP Error {response.status_code}')
        return (f'HTTP Error {response.status_code}','','')
    
def update_labels():
    i = 0
    response = update_response()
    for data in labels:
        data['text'] = response[i]
        i += 1

def loop_update():
    root.after(11000, loop_update)
    update_labels()

def buy(price, coin):
    global balance
    if price == 'all':
        price = balance["USD"]
    elif '%' in price:
        price = int(price.replace('%', '')) / 100 * balance["USD"]
    else:
        price = round(float(price), 9)
    print(price, balance[coin])
    if balance["USD"] >= price:
        print(round(price/prices[coin], 9))
        balance[coin] += round(price/prices[coin], 9)
        balance["USD"] -= price
        
        update_bal()

def sell(price, coin):
    global balance
    if price == 'all':
        price = balance[coin]
    elif '%' in price:
        price = int(price.replace('%', '')) / 100 * balance[coin]
    else:
        price = round(float(price), 9)
    print(price, balance[coin])
    if balance[coin] >= price:
        print(round(price, 9))
        balance[coin] -= price
        balance["USD"] += price*prices[coin]
        
    update_bal()

def update_bal():
    result = ''
    for coin in balance:
        if balance[coin] > 0: result += f'{coin}: {round(balance[coin], 9)}\n'
    balance_display['text'] = result

def save():
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(dumps(balance))
    root.destroy()

def load():
    global balance
    with open('data.json', 'r', encoding='utf-8') as f:
        file = f.read()
        balance = loads(file)
        update_bal()

tk.Label(root, text="Beedkoen", font=("Arial", 35),justify="center").pack()

tk.Label(root, text='Price (USD)').place(x=5,y=200)
price_inp = ttk.Entry(root, width=15)
price_inp.place(x=5,y=220)

tk.Label(root, text='Coin').place(x=130,y=200)
coin_inp = ttk.Combobox(root, width=15, values=coins)
coin_inp.place(x=130,y=220)

ttk.Button(root, text='Update', command=update_response).place(x=5,y=150)
balance_display = tk.Label(root, text=f'Balance: {balance["USD"]}$', justify='left')
balance_display.place(x=5, y=280)

def capitalize(string: str):
    return string.capitalize()

i = 0
response = update_response()
for coin in response:
    data = tk.Label(root, text=coins, justify="left")
    labels.append(data)
    data.place(x=5,y=i*30+70)
    i += 1

ttk.Button(root, text='Buy', command=lambda: buy(price_inp.get(), coin_inp.get())).place(x=5,y=250)
ttk.Button(root, text='Sell', command=lambda: sell(price_inp.get(), coin_inp.get())).place(x=95,y=250)

root.protocol('WM_DELETE_WINDOW',save)

load()

loop_update()


root.mainloop() 