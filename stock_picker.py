import csv
import sys
from math import sqrt
from datetime import datetime, timedelta


def process_csv(from_date, to_date, stock, path):
    csv_data = read_csv_data(path)
    from_date = datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.strptime(to_date, '%d-%b-%Y')
    stock_data = get_range_data(from_date, to_date, csv_data[stock])
    final_data = get_final_data(from_date, to_date, stock_data)
    mean, sd = stddev_mean(list(final_data.values()))
    profit, p_time = maxProfit(final_data)
    return mean, sd, profit, p_time


def read_csv_data(path):
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = {}
        for row in csv_reader:
            data[row['stock']] = data.get(row['stock'], []) + [
                {row['date']: row['price']}]
    return data


def get_range_data(fromdate, to_date, val):
    stock_data = {}
    for w in val:
        for k, v in w.items():
            if fromdate <= datetime.strptime(k, '%d-%b-%Y') <= to_date:
                stock_data[datetime.strptime(k, '%d-%b-%Y').date()] = float(v)
    return stock_data


def get_final_data(from_date, to_date, stock_data):
    if len(stock_data) == 0:
        sys.exit('No data available b/w given dates')
    from_date = min(stock_data)
    to_date = max(stock_data)
    delta = to_date - from_date
    final_data = {}
    for i in range(delta.days + 1):
        nd = from_date + timedelta(i)
        if nd in stock_data:
            final_data[nd] = stock_data[nd]
        else:
            final_data[nd] = stock_data[from_date + timedelta(i-1)]
            stock_data[nd] = stock_data[from_date + timedelta(i-1)]
    return final_data


def stddev_mean(stk_list):
    mean = float(sum(stk_list)) / len(stk_list)
    sd = sqrt(sum((x - mean)**2 for x in stk_list) / len(stk_list))
    return mean, sd


def maxProfit(stock_data):
    p_time = {'buy_date': None, 'sell_date': None}
    if not stock_data or len(stock_data) is 1:
        return 0, p_time

    profit = 0
    key_list = list(stock_data.keys())
    val_list = list(stock_data.values())
    price = list(stock_data.values())

    for i in range(1, len(price)):
        if price[i] > price[i-1]:
            p_time['buy_date'] = key_list[val_list.index(price[i-1])]
            p_time['sell_date'] = key_list[(val_list).index(price[i])]
            profit += price[i]*100 - price[i-1]*100
    return profit, p_time


def check_stock_in_data(stock, path):
    csv_data = read_csv_data(path)
    key = set(csv_data.keys())
    if stock not in csv_data:
        return [k for k in key if k.startswith(stock)][0]


def check_answer(sug_input):
    if sug_input is 'n':
        sys.exit()


path = str(sys.argv[1])
stock = input('Which stock you need to process? \n').upper()
sug_stock = check_stock_in_data(stock, path)
if sug_stock:
    stock = sug_stock
    sug_input = input('Oops! Do you mean {} ? y or n \n'.format(sug_stock))
    check_answer(sug_input)
from_date = input('From which date you want to start \n')
to_date = input('Till which date you want to analyze \n')
mean, sd, profit, p_time = process_csv(from_date, to_date, stock, path)
result = 'Here is your result:\n Mean: {} \n Std: {} \n Buy Date: {} \n Sell Date: {} \n Profit: {} \n'.format(
         mean, sd, p_time['buy_date'], p_time['sell_date'], profit)
print(result)
