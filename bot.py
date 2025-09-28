import requests
import time
import random
from datetime import datetime
from pathlib import Path
import os
import shutil

API_URL = "https://api.dawninternet.com/point"
TOKENS_FILE = "tokens.txt"
PROXY_FILE = "proxy.txt"
REFRESH_MIN = 15
REFRESH_MAX = 35

CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def center_line(text: str) -> str:
    width = shutil.get_terminal_size().columns
    pad = max((width - len(text)) // 2, 0)
    return " " * pad + text


def print_logo():
    os.system("clear" if os.name == "posix" else "cls")
    line = "=" * 40
    logo_text = "---- Auto-Bot by Jabrik ----"
    print(CYAN + center_line(line) + RESET)
    print(MAGENTA + center_line(logo_text) + RESET)
    print(CYAN + center_line(line) + RESET)
    print()


def load_tokens():
    path = Path(TOKENS_FILE)
    if not path.exists():
        raise FileNotFoundError(f"{TOKENS_FILE} not found.")
    tokens = [t.strip() for t in path.read_text(encoding="utf-8").splitlines() if t.strip()]
    if not tokens:
        raise ValueError("tokens.txt is empty. Please add at least one token.")
    return tokens


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
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [!] Token {token[:10]}... Request failed: {e}")
        return None


def run_bot():
    print_logo()
    tokens = load_tokens()
    proxy = load_proxy()
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Bot started for {len(tokens)} account(s)...\n")

    while True:
        for token in tokens:
            result = get_point(token, proxy)
            if result and "points" in result:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Token {token[:10]}... Points: {result['points']}")
            else:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Token {token[:10]}... Failed to fetch points.")
        delay = random.randint(REFRESH_MIN, REFRESH_MAX)
        time.sleep(delay)


if __name__ == "__main__":
    run_bot()
