import blockapi
import datetime

def get_transactions(myapi):
    transactions = []
    page = 1
    limit = 10
    while True:
        t = myapi.get_txs(page, limit)
        if not t:
            return transactions
        transactions += t
        page += 1

def get_balances(transactions):
    balances = []
    for t in transactions:
        timestamp = int(datetime.datetime.strptime(t['date'], '%Y-%m-%d %H:%M:%S%z').timestamp())
        if "outgoing" == t['direction']:
            balances.append([timestamp, 'BTC', -t['amount']])
        else:
            balances.append([timestamp, 'BTC', t['amount']])

    balances.sort(key=lambda r: r[0], reverse=False)

    for i in range(1, len(balances)):
        balances[i][2] = balances[i - 1][2] + balances[i][2]
    return balances

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise ValueError("Only address as a first parameter required.")
    address = sys.argv[1]

    myapi = blockapi.api.Btc2TrezorAPI(address)
    transactions = get_transactions(myapi)
    balances = get_balances(transactions)

    assert format(float(myapi.get_balance()[0]['amount']), '.8f') == format(balances[-1][2], '.8f')
    print(balances)
