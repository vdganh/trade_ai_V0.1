import locale
import requests
import numpy as np
from alpha_vantage.timeseries import TimeSeries

# Variabel global untuk status login
logged_in = False

# Fungsi untuk memuat data harga menggunakan Alpha Vantage API
def load_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, _ = ts.get_daily(symbol=symbol, outputsize='full')
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return data

# Fungsi untuk menentukan level buy, stop loss, dan take profit
def calculate_levels(last_close_price):
    # Menggunakan deviasi standar dari harga penutupan sebelumnya
    volatility = 0.05 * last_close_price  # Anggap volatilitas sebesar 5%
    buy_level = last_close_price + (2 * volatility)
    stop_loss_level = last_close_price - (1.5 * volatility)
    take_profit_level = last_close_price + (4 * volatility)
    return buy_level, stop_loss_level, take_profit_level

# Fungsi untuk format nilai menjadi mata uang Rupiah
def format_to_idr(amount):
    locale.setlocale(locale.LC_ALL, 'id_ID')
    return locale.currency(amount, grouping=True)

# Fungsi untuk mendapatkan harga kripto secara real-time
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=idr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[crypto_id]["idr"]
    else:
        print("Gagal mendapatkan data kripto.")
        return None

# Fungsi untuk menyimpan data pengguna
def save_user_data(username, password):
    # Implementasi penyimpanan data pengguna ke database atau file
    print("Pengguna berhasil dibuat.")

# Fungsi untuk memeriksa kredensial pengguna saat login
def check_user_credentials(username, password):
    # Implementasi pemeriksaan kredensial pengguna dari database atau file
    # Contoh sederhana: jika pengguna adalah "admin" dan kata sandinya adalah "password123"
    return username == "admin" and password == "password123"

# Fungsi untuk membuat akun
def create_account():
    global logged_in  # Deklarasikan variabel logged_in sebagai global
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    save_user_data(username, password)
    
    # Set logged_in menjadi True setelah berhasil membuat akun
    logged_in = True
    print("Akun berhasil dibuat dan Anda telah login.")

# Fungsi untuk login
def login():
    global logged_in  # Deklarasikan variabel logged_in sebagai global
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if check_user_credentials(username, password):
        print("Login berhasil. Selamat datang kembali, ", username, "!")
        logged_in = True  # Set logged_in menjadi True setelah login berhasil
        return True
    else:
        print("Username atau password salah.")
        return False

# Trading otomatis saham
def trading_auto_stock(api_key):
    symbol = input("Masukkan simbol saham: ")

    data = load_stock_data(symbol, api_key)
    buy_level, stop_loss_level, take_profit_level = calculate_levels(data['Close'].iloc[-1])

    last_close_price = data['Close'].iloc[-1]

    print("Simbol:", symbol)
    print("Harga Penutupan Terakhir:", format_to_idr(last_close_price))
    print("Level Beli:", format_to_idr(buy_level))
    print("Level Stop Loss:", format_to_idr(stop_loss_level))
    print("Level Take Profit:", format_to_idr(take_profit_level))

# Trading manual saham
def trading_manual_stock(api_key):
    symbol = input("Masukkan simbol saham: ")
    last_close_price = float(input("Masukkan harga penutupan saham saat ini (dalam Rupiah): "))

    buy_level, stop_loss_level, take_profit_level = calculate_levels(last_close_price)

    print("Harga penutupan saham:", format_to_idr(last_close_price))
    print("Level Beli (Buy Level):", format_to_idr(buy_level))
    print("Level Stop Loss:", format_to_idr(stop_loss_level))
    print("Level Take Profit:", format_to_idr(take_profit_level))

# Trading manual kripto
def trading_manual_crypto():
    crypto_id = input("Masukkan ID kripto (contoh: bitcoin): ").lower().strip()  # Strip spasi ekstra di akhir dan ubah ke huruf kecil
    last_close_price = get_crypto_price(crypto_id)

    if last_close_price is not None:
        buy_level, stop_loss_level, take_profit_level = calculate_levels(last_close_price)

        print("Harga penutupan kripto:", format_to_idr(last_close_price))
        print("Level Beli (Buy Level):", format_to_idr(buy_level))
        print("Level Stop Loss:", format_to_idr(stop_loss_level))
        print("Level Take Profit:", format_to_idr(take_profit_level))

# Menu utama
def main():
    global logged_in  # Deklarasikan variabel logged_in sebagai global
    api_key = 'VDIM2WU91HAKTNX0'  # Ganti dengan API key Alpha Vantage Anda

    while True:
        print("\n== MENU ==")
        if not logged_in:  # Jika belum login, tampilkan opsi login dan buat akun
            print("1. Buat Akun Sementara (Login Sekali Saja)")
            print("2. Buat Akun Permanen (Login Setiap Saat)")
        else:  # Jika sudah login, tampilkan semua opsi menu kecuali opsi keluar
            print("1. Trading Otomatis Saham & Crypto")
            print("2. Trading Manual Saham & Crypto")
            print("3. Trading Manual Crypto")
            print("4. Keluar")

        # Meminta input pilihan menu dari pengguna
        choice = input("Pilih menu: ")

        # Tindakan sesuai dengan pilihan pengguna
        if not logged_in and choice == '1':
            create_account()
        elif not logged_in and choice == '2':
            login()
        elif logged_in and choice == '1':
            trading_auto_stock(api_key)
        elif logged_in and choice == '2':
            trading_manual_stock(api_key)
        elif logged_in and choice == '3':
            trading_manual_crypto()
        elif logged_in and choice == '4':
            print("1. Kembali ke Menu Login")
            print("2. Keluar dari Program")
            exit_choice = input("Pilih: ")
            if exit_choice == '1':
                logged_in = False
            elif exit_choice == '2':
                print("Terima kasih!")
                break
            else:
                print("Pilihan tidak valid")
        else:
            print("Pilihan tidak valid")


if __name__ == "__main__":
    main()
