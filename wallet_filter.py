wallets = []
with open('wallets.txt', 'r') as file:
    for wallet in file:
        if wallet.strip() not in wallets:
           wallets.append(wallet.strip())
            
print(*wallets, sep='\n') 