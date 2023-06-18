import asyncio
import aiohttp
from loguru import logger


async def fetch_nft_positions(session, wallet, chain):
    url = f"https://api.zerion.io/v1/wallets/{wallet}/nft-positions/?filter[chain_ids]={chain}&currency=usd&page[size]=100"
    headers = {
        "accept": "application/json",
        "authorization": "" # Check https://developers.zerion.io/
    }

    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            response_json = await response.json()
            await asyncio.sleep(0.5)

            nfts_number = len(response_json.get("data", []))
            if nfts_number > 0:
                return nfts_number

    return 0


async def check_nfts(worker: str, wallet: str, chains: list):
    async with aiohttp.ClientSession() as session:
        for chain in chains:
            nfts_number = await fetch_nft_positions(session, wallet, chain)

            logger.success(
                f'{worker} На кошельке {wallet} в сети {chain} найдено: {nfts_number} NFT\n'
            )


async def main(wallets, selected_chains):
    chains = selected_chains.split(',')
    tasks = []

    for i, wallet in enumerate(wallets):
        worker = f"Worker {i+1}"
        task = asyncio.create_task(check_nfts(worker, wallet, chains))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        selected_chains = input('Введите EVM сети через запятую без пробелов: ')
        with open('another_wallets.txt', 'r', encoding='utf-8') as file:
            wallets = file.read().splitlines()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(main(wallets, selected_chains))

    except KeyboardInterrupt:
        pass