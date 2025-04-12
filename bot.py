import time
import os
import random
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup koneksi ke RPC
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Informasi wallet kita
private_key = os.getenv("PRIVATE_KEY")
my_address = Web3.to_checksum_address(os.getenv("PUBLIC_ADDRESS"))

# Alamat kontrak token dan ABI
token_address = Web3.to_checksum_address("Your-Token-Contract")erc20_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

# Inisialisasi kontrak
token_contract = w3.eth.contract(address=token_address, abi=erc20_abi)

# Baca dan konversi alamat tujuan ke checksum
with open('addresses.txt', 'r') as f:
    recipient_addresses = []
    for line in f:
        try:
            addr = Web3.to_checksum_address(line.strip())
            recipient_addresses.append(addr)
        except Exception as e:
            print(f"❌ Alamat tidak valid: {line.strip()} - {e}")

print(f"Jumlah alamat tujuan yang valid: {len(recipient_addresses)}")

# Fungsi kirim token
def send_token(to_address, amount):
    try:
        nonce = w3.eth.get_transaction_count(my_address)
        tx = token_contract.functions.transfer(to_address, amount).build_transaction({            
            'chainId': 10218,  # ganti sesuai network kamu
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ TX terkirim ke {to_address}: {w3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"❌ Gagal kirim ke {to_address}: {e}")

# Loop pengiriman token
for i, address in enumerate(recipient_addresses):
    # Acak jumlah token antara 1.00 hingga 5.00 Token
    random_amount = round(random.uniform(1.0, 5.0), 2)
    amount_wei = int(random_amount * (10 ** 18))

    print(f"[{i+1}/{len(recipient_addresses)}] Mengirim {random_amount} Token ke {addres>    send_token(address, amount_wei)

    # Delay antara 60 sampai 120 detik
    delay = random.randint(60, 120)
    print(f"⏳ Menunggu sekitar {delay} detik sebelum transaksi berikutnya...\n")
    time.sleep(delay)
