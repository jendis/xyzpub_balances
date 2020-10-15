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
    transfers = []
    for t in transactions:
        timestamp = int(datetime.datetime.strptime(t['date'], '%Y-%m-%d %H:%M:%S%z').timestamp())
        if "outgoing" == t['direction']:
            transfers.append([timestamp, -t['amount']])
        else:
            transfers.append([timestamp,  t['amount']])

    transfers.sort(key=lambda r: r[0], reverse=False)

    balances = [[transfers[0][0], 'BTC', transfers[0][1]]]
    for t in transfers[1:]:
        if t[0] == balances[-1][0]:
            balances[-1][2] += t[1]
            continue
        balances.append([t[0], 'BTC', t[1]])

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
    if transactions:
        balances = get_balances(transactions)
        print(balances)
    else:
        print("No transactions")
