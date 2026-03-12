#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "[!] Please run as root: sudo ./install.sh"
  exit 1
fi

echo "[*] Updating package lists..."
apt-get update -y

echo "[*] Installing required packages..."
apt-get install -y \
  python3 \
  python3-setuptools \
  aircrack-ng \
  wireless-tools \
  net-tools

echo "[*] Installing optional (recommended) tools..."
apt-get install -y \
  tshark \
  reaver \
  bully \
  cowpatty \
  pyrit \
  hashcat \
  hcxdumptool \
  hcxtools || true

echo "[*] Installing Wifite2 - Created by @CyberDanish..."
python3 setup.py install

echo "[+] Done. Run: sudo wifite2"
