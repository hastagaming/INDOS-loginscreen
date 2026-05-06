import datetime
import os
import getpass
import socket
import platform
import json
import subprocess

# --- Configuration Path ---
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "user_config.json")

def get_system_info():
    """
    Fetches system information formatted with Tmux color codes
    to emulate a modern Waybar aesthetic.
    """
    time_now = datetime.datetime.now().strftime("%H:%M")
    date_now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                user = data.get("username", getpass.getuser())
        else:
            user = getpass.getuser()
    except Exception:
        user = getpass.getuser()
        
    # Using Catppuccin-inspired colors for the status bar
    return f"#[fg=#89b4fa,bold] 󰣇 INDOS #[fg=#cdd6f4,nobold] |  {user} |  {time_now} | 󰃭 {date_now} "

# --- Authentication Logic ---

def validate_login(username_input, password_input):
    """Checks user credentials against the stored JSON config."""
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
    """Saves new user credentials during the sign-up process."""
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"username": username, "password": password}, f, indent=4)
        return True
    except Exception:
        return False

# --- Tmux Engine (The Workspace Core) ---

def start_tmux_session():
    """
    Initializes a persistent Tmux session with a tiling layout
    and Hyprland-style aesthetics.
    """
    session_name = "INDOS"
    
    # Clean up any existing session with the same name
    subprocess.run(["tmux", "kill-session", "-t", session_name], stderr=subprocess.DEVNULL)
    
    # 1. Create a new detached session
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name])
    
    # 2. Status Bar Configuration (Waybar-style)
    # Position: Top, Style: Catppuccin Mocha
    subprocess.run(["tmux", "set-option", "-t", session_name, "status-position", "top"])
    subprocess.run(["tmux", "set-option", "-t", session_name, "status-style", "bg=#11111b,fg=#cdd6f4"])
    subprocess.run(["tmux", "set-option", "-t", session_name, "status-left", ""])
    subprocess.run(["tmux", "set-option", "-t", session_name, "status-right", get_system_info()])
    subprocess.run(["tmux", "set-option", "-t", session_name, "status-interval", "1"])

    # 3. Pane Border Configuration (Hyprland Aesthetic)
    subprocess.run(["tmux", "set-option", "-t", session_name, "pane-border-style", "fg=#313244"])
    subprocess.run(["tmux", "set-option", "-t", session_name, "pane-active-border-style", "fg=#89b4fa"])

    # 4. Default Layout Construction
    # Split horizontally: Main terminal (70%) | Info Panel (30%)
    subprocess.run(["tmux", "split-window", "-h", "-t", f"{session_name}.0", "-p", "30"])
    
    # Initialize the secondary panel with a welcome message
    welcome_cmd = "clear && echo -e '\\n  󰣇  Welcome to INDOS Workspace\\n  ----------------------------\\n  󰝰  FILES  : Type yazi\\n    AI     : Type gemini\\n  󰠚  EXIT   : Ctrl+b then d'"
    subprocess.run(["tmux", "send-keys", "-t", f"{session_name}.1", welcome_cmd, "C-m"])

    # Refocus the main working pane
    subprocess.run(["tmux", "select-pane", "-t", f"{session_name}.0"])
    
    # 5. Attach to the session
    os.system(f"tmux attach-session -t {session_name}")

# --- Integrated Tools ---

def open_file_manager():
    """Opens Yazi in a new Tmux window for seamless multitasking."""
    subprocess.run(["tmux", "new-window", "-n", "Files", "yazi"])

def open_gemini_chat():
    """Opens the Gemini AI chat in a new Tmux window."""
    subprocess.run(["tmux", "new-window", "-n", "Gemini AI", "gemini"])
