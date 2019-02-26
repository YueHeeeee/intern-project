# change data form
def extract_stock_history(this_stock_history):
    dates = this_stock_history[0]
    prices = this_stock_history[1]
    dates.pop(0)
    prices.pop(0)
    res = {"date":dates, "price":prices}
    return res

# change data form
def extract_news_info(this_news_info):
    titles = this_news_info[1]
    urls = this_news_info[0]
    polarity = list(map(lambda x : None if x == 0 else x, this_news_info[2]))
    res = {"title":titles, "url":urls, "polarity":polarity}
    
    for i in range(len(titles)):
        res["url"][i] = res["url"][i][31:]
    return res


# the main function to retrun all data
def toDict(comp):
#      done
    this_stock_history = extract_stock_history(stock_history(comp))
#      to be done
    this_stock_info = stock_info(comp)
#      done
    this_news_info = extract_news_info(news_info(comp))
    this_market_cap = int(marketcap_info(comp).replace(",", ""))
    if cashflow_info(comp)[0] == "None":
        this_cashflow = None
    else:
        this_cashflow = int(cashflow_info(comp)[0].replace(",", "").replace("$", ""))
    
    res = {}
    res["company"] = comp
    res["stock_price"] = this_stock_history
    res["article"] = this_news_info
    res["market_cap"] = this_market_cap
    res["net_cash_flow"] = this_cashflow
    return res


# change all data to json
import json

comp_list = ["OXY", "EOG", "APC", "APA", "COP", "PXD"]
res = {}
for comp in comp_list:
    res[comp] = toDict(comp)

output = json.dumps(res)
f = open("data.json", "w")
f.write(output)
f.close()