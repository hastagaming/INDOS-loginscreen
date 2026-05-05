#!/bin/bash
clear
echo -e "\e[1;34m󰚰  INDOS Installer\e[0m"
echo -e "\e[1;36m[*] Installing dependencies...\e[0m"

pkg update && pkg upgrade -y
pkg install python -y
pip install textual

echo -e "\e[1;32m[+] Installation finished!\e[0m"
echo -e "\e[1;33m[!] Ensure you are using a NerdFont for icons to display correctly.\e[0m"
echo -e "\e[1;36m[*] Launch: python core/main.py\e[0m"
