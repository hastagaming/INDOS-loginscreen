import datetime
import os
import getpass
import socket

def get_system_info():
    time_now = datetime.datetime.now().strftime("%H:%M")
    date_now = datetime.datetime.now().strftime("%d/%m/%y")
    current_user = getpass.getuser()
    # Menggunakan ikon NerdFont untuk User, Clock, dan Calendar
    return f"  {current_user}   {time_now}  󰃭 {date_now} "

def get_user_prompt():
    user = getpass.getuser()
    try:
        # Cek file .hostname, jika tidak ada pakai hostname sistem
        if os.path.exists(os.path.expanduser("~/.hostname")):
            with open(os.path.expanduser("~/.hostname"), "r") as f:
                host = f.read().strip()
        else:
            host = socket.gethostname()
    except:
        host = "indos-device"
        
    return f"   [{user}@{host} ~]$ _"
