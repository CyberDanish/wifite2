# Wifite2 Kali Linux Installation & Troubleshooting Guide

## 🔴 ISSUE: Tool exits after 2 seconds

If Wifite2 opens but exits immediately (after ~2 seconds), it means there's an error during initialization. Follow these steps:

## ✅ STEP 1: Install Required Dependencies

### On Kali Linux:
```bash
sudo apt update
sudo apt install -y aircrack-ng macchanger tshark
```

### Optional but Recommended:
```bash
sudo apt install -y hashcat-data pyrit reaver bully
```

## ✅ STEP 2: Verify Installation

```bash
# Check if tools are installed
which aircrack-ng
which airmon-ng
which aireplay-ng
which airodump-ng
which tshark

# You should see paths like:
# /usr/bin/aircrack-ng
# /usr/bin/airmon-ng
# etc.
```

## ✅ STEP 3: Install Wifite2

### Option A: Install from current directory
```bash
cd /path/to/wifite2
sudo pip3 install -e .
```

### Option B: Run directly
```bash
sudo python3 Wifite2.py
# or after installation:
sudo wifite2
```

## ✅ STEP 4: Debugging - Run with Verbose Output

If it still exits, run with verbose debugging:

```bash
sudo wifite2 -v
```

This will show detailed error messages including:
- Which dependencies are missing
- Which wireless interfaces were found
- Which tools are installed/missing

## 🔧 Common Issues & Solutions

### Issue 1: "aircrack-ng not found"
**Solution:**
```bash
sudo apt install -y aircrack-ng
# Verify:
which aircrack-ng
aircrack-ng --version
```

### Issue 2: No wireless interfaces found
**Solution:**
```bash
# Check if your wireless device is detected
iwconfig
# or
iw dev

# If not showing, you may need drivers:
# Check: lspci | grep -i wireless
# Then install appropriate drivers
```

### Issue 3: Permission Denied errors
**Solution:**
```bash
# Make sure you're running with sudo
sudo wifite2

# Check user is in sudoers:
groups $USER | grep sudo
```

### Issue 4: Monitor mode setup fails
**Solution:**
```bash
# Manually set up monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0  # Replace wlan0 with your interface
# Now run wifite2 again
```

## 🚀 Quick Start (After Installation)

```bash
# 1. Make sure wireless adapter is connected
sudo airmon-ng check kill

# 2. Start Wifite2
sudo wifite2

# 3. Select your wireless interface when prompted
# 4. Wait for networks to be found
# 5. Select a target to attack
```

## 📋 Device Requirements

- **Wireless Adapter**: Must support monitor mode (Alfa TP-Link, etc.)
- **Linux Kernel**: 4.0+
- **Python**: 3.6+
- **Root Access**: Required for packet injection

## ⚠️ Advanced Debugging

If you want to see exactly what's happening:

```bash
# Run with Python directly to see errors
sudo python3 -c "
import sys
sys.path.insert(0, '.')
from wifite2 import __main__
__main__.entry_point()
" -v
```

Or modify your terminal call:
```bash
sudo wifite2 2>&1 | tee wifite2_debug.log
```

This will save all output to wifite2_debug.log which you can review.

## 🔍 Manual Tool Check Script

```bash
#!/bin/bash
echo "Checking Wifite2 dependencies..."
for tool in aircrack-ng airmon-ng aireplay-ng airodump-ng tshark macchanger; do
    if command -v $tool &> /dev/null; then
        echo "[OK] $tool found at $(which $tool)"
    else
        echo "[MISSING] $tool  - Install with: sudo apt install -y $tool"
    fi
done
```

## 💡 Pro Tips

1. **Performance**: Run on Kali Linux (not WSL or VM if possible) for best results
2. **Stability**: Update regularly: `sudo apt update && sudo apt upgrade`
3. **Speed**: Use SSD for faster handshake processing
4. **Debugging**: Run with `-v` flag to see detailed output
5. **Testing**: Start with known WEP networks before WPA2

---

## 🆘 Still Having Issues?

1. Check that all required tools are installed:
   - `aircrack-ng` (core tool)
   - `airmon-ng` (monitor mode)
   - `aireplay-ng` (packet injection)
   - `airodump-ng` (network scanning)

2. Ensure wireless adapter supports monitor mode

3. Run: `sudo wifite2 -v` to see detailed error messages

4. Check wifite2 logs: `cat ~/.wifite2/wifite2.log`

5. Make sure no other tools are using the wireless interface
   - Kill conflicting processes: `sudo airmon-ng check kill`
