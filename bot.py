import requests
import time
import random
from datetime import datetime
from pathlib import Path
import os

API_URL = "https://api.dawninternet.com/point"
TOKEN_FILE = "token.txt"
PROXY_FILE = "proxy.txt"
REFRESH_MIN = 20
REFRESH_MAX = 30


def print_logo():
    os.system("clear" if os.name == "posix" else "cls")
    print("=" * 40)
    print("        ---- Auto Bot by Jabrik ----")
    print("=" * 40)
    print()


def load_token():
    path = Path(TOKEN_FILE)
    if not path.exists():
        raise FileNotFoundError(f"File {TOKEN_FILE} tidak ditemukan.")
    token = path.read_text(encoding="utf-8").strip()
    if not token:
        raise ValueError("token.txt kosong, isi dengan Bearer Token.")
    return token


def load_proxy():
    path = Path(PROXY_FILE)
    if not path.exists():
        return None
    proxy = path.read_text(encoding="utf-8").strip()
    return proxy if proxy else None


def get_point(token, proxy=None):
    headers = {"Accept": "*/*", "Authorization": f"Bearer {token}"}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        r = requests.get(API_URL, headers=headers, proxies=proxies, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [!] Gagal request: {e}")
        return None


def run_bot():
    print_logo()
    token = load_token()
    proxy = load_proxy()
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Bot mulai berjalan...\n")

    while True:
        result = get_point(token, proxy)
        if result:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Point terkini: {result}")
        else:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Gagal ambil point.")

        delay = random.randint(REFRESH_MIN, REFRESH_MAX)
        time.sleep(delay)


if __name__ == "__main__":
    run_bot()
