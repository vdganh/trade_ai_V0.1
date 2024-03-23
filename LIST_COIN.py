import requests
import sys

def get_coin_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Gagal mendapatkan daftar koin. Kode status:", response.status_code)
        return None

def print_coin_list(coin_list):
    if coin_list:
        print("Daftar Koin pada CoinGecko:")
        for i, coin in enumerate(coin_list, start=1):
            print(f"{i}. Nama koin: {coin['name']}")
            print(f"   Simbol: {coin['symbol']}")
            print(f"   Nama: {coin['name']}")
            print(f"   ID: {coin['id']}\n")
    else:
        print("Gagal mendapatkan daftar koin.")

def search_coin_by_initial(coin_list, initial):
    results = []
    for coin in coin_list:
        if coin['name'].lower().startswith(initial.lower()) or coin['symbol'].lower().startswith(initial.lower()):
            results.append(coin)
    return results

def handle_user_input():
    try:
        initial = input("\nMasukkan huruf awalan koin yang ingin dicari (Ctrl+C untuk keluar): ")
        return initial
    except KeyboardInterrupt:
        print("\nPencarian koin telah dibatalkan.")
        sys.exit()

# Mendapatkan daftar koin
coin_list = get_coin_list()

# Menampilkan daftar koin
print_coin_list(coin_list)

# Pengulangan untuk pencarian koin
while True:
    initial = handle_user_input()

    # Pencarian koin berdasarkan huruf awalan
    search_results = search_coin_by_initial(coin_list, initial)

    if search_results:
        print("\nHasil Pencarian:")
        print_coin_list(search_results)
    else:
        print("Tidak ada koin yang ditemukan dengan huruf awalan tersebut.")
