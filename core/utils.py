import datetime
import os
import getpass
import socket
import platform
import json

# Lokasi file konfigurasi user
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "user_config.json")

def get_system_info():
    """
    Mengambil informasi sistem untuk ditampilkan di Waybar.
    Menggunakan nama dari config jika tersedia, jika tidak menggunakan sistem.
    """
    time_now = datetime.datetime.now().strftime("%H:%M")
    date_now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Mencoba mengambil username dari config JSON
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                current_user = data.get("username", getpass.getuser())
        else:
            current_user = getpass.getuser()
    except Exception:
        current_user = getpass.getuser()
    
    return f" 󰣇 INDOS |  {current_user} |  {time_now} | 󰃭 {date_now} "

def get_user_prompt():
    """
    Menghasilkan string prompt terminal yang dinamis.
    """
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                user = data.get("username", getpass.getuser())
        else:
            user = getpass.getuser()
    except Exception:
        user = getpass.getuser()
    
    try:
        if os.path.exists(os.path.expanduser("~/.hostname")):
            with open(os.path.expanduser("~/.hostname"), "r") as f:
                host = f.read().strip()
        else:
            host = socket.gethostname()
            if host == "localhost" or not host:
                host = "INDOS"
    except Exception:
        host = "INDOS"
        
    arch = platform.machine()
    return f"   [{user}@{host} ({arch}) ~]$ _"

def validate_login(username_input, password_input):
    """
    Fungsi pembantu untuk memvalidasi login di main.py
    """
    if not os.path.exists(CONFIG_PATH):
        return False, "No account found"
        
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            if username_input == data["username"] and password_input == data["password"]:
                return True, "Success"
            else:
                return False, "Invalid username or password"
    except Exception as e:
        return False, str(e)

def save_user_config(username, password):
    """
    Menyimpan kredensial baru saat proses Sign Up.
    """
    try:
        data = {"username": username, "password": password}
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False
