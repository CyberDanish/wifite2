#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "[!] Please run as root: sudo ./install.sh"
  exit 1
fi

echo "[*] Updating package lists..."
apt-get update -y 2>/dev/null || apt-get update -y

echo "[*] Installing REQUIRED packages..."
REQUIRED_PKGS="python3 python3-setuptools aircrack-ng wireless-tools net-tools"
for pkg in $REQUIRED_PKGS; do
  if dpkg -l | grep -q "^ii  $pkg"; then
    echo "[+] $pkg is already installed"
  else
    echo "[*] Installing $pkg..."
    apt-get install -y "$pkg" || true
  done
done

echo ""
echo "[*] Installing optional (recommended) tools for better speed & features..."
apt-get install -y \
  tshark \
  reaver \
  bully \
  cowpatty \
  pyrit \
  hashcat \
  hcxdumptool \
  hcxtools \
  macchanger || true

echo ""
echo "[*] Installing Wifite2 - Created by @CyberDanish..."
python3 setup.py install

echo ""
echo "[+] =========================================="
echo "[+] Installation Complete!"
echo "[+] =========================================="
echo ""
echo "[*] Run Wifite2 with:"
echo "[*]   sudo wifite2"
echo "[*] Or directly:"
echo "[*]   sudo python3 Wifite2.py"
echo ""
echo "[*] Check if aircrack-ng is found:"
echo "[*]   which aircrack-ng"
echo ""
