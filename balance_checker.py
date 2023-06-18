import requests 
import json
import time

def get_balance(wallet, selected_chains):
    url = f"https://api.zerion.io/v1/wallets/{wallet}/portfolio/?currency=usd"

    headers = {
        "accept": "application/json",
        "authorization": "" # Check https://developers.zerion.io/
    }

    response = requests.get(url, headers=headers)
    parsed_data = json.loads(response.text)
    try:
        balances = parsed_data['data']['attributes']['positions_distribution_by_chain']
    except KeyError:
        return 0
    
    total_balance = sum(balances.values())
    
    print(f"Баланс кошелька {wallet}:")
    for chain in selected_chains:
        if chain in balances:
            print(f'    {chain}: {balances[chain]} USD')
        else:
            print(f"    {chain}: нет данных")
    print(f'Общий баланс кошелька {total_balance} USD\n')
    return total_balance
    
                

total_balance_of_all_wallets = 0

if __name__ == '__main__':
    selected_chains = input('Введите сети через запятую, в которых вы хотите узнать баланс: ').split(',')
    print()
    with open('wallets.txt', 'r', encoding='utf-8') as file:
        for wallet in file:    
            total_balance_of_all_wallets += get_balance(wallet.strip(), selected_chains)
            time.sleep(1)

    print(f'Общий баланс всех кошельков: {total_balance_of_all_wallets}')           