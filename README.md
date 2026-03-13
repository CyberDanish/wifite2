# Wifite2 - Wireless Network Auditor
**Created & Maintained by @CyberDanish**

Professional wireless security auditing tool for penetration testing and WiFi vulnerability assessment. Automates WEP, WPA2, and WPS cracking attacks on Linux.

## Quick Start

### Installation
```bash
git clone https://github.com/derv82/wifite2.git
cd wifite2
sudo python3 setup.py install
```

### Usage
```bash
# Basic scan and attack
sudo wifite2

# WPS Pixie-Dust attack
sudo wifite2 --wps-only --pixie

# WPA handshake + crack
sudo wifite2 --no-wps --crack

# PMKID attack
sudo wifite2 --pmkid

# Verbose output
sudo wifite2 -vvv
```

## Features

- **Automated Attack Selection** - Intelligently chooses optimal cracking method
- **WPS Attacks** - Pixie-Dust and PIN brute-force attacks
- **WPA/WPA2** - Handshake capture and PMKID hash cracking  
- **WEP Attacks** - Multiple legacy wireless security exploits
- **Hidden Network Detection** - Automatic decloaking of hidden SSIDs
- **Real-time Monitoring** - Live signal strength and progress display
- **Persistent Storage** - Saves cracked credentials and handshakes
- **Dictionary/Wordlist Support** - Easy offline cracking integration
- **Python 3 Compatible** - Modern Python with Python 2.7 support
- **Verbose Logging** - Full command transparency with `-vv` / `-vvv`

## Requirements

### Hardware
- Wireless adapter with **Monitor Mode** and **packet injection** support
- See [Aircrack-ng compatible cards](http://www.aircrack-ng.org/doku.php?id=compatible_cards)

### Software (Required)
- `python3` or `python2.7`
- `aircrack-ng` suite (airmon-ng, airodump-ng, aircrack-ng, aireplay-ng)
- `iwconfig` and `ifconfig`

### Dependencies (Recommended)
- `hashcat` - PMKID and WPA cracking
- `reaver` - WPS Pixie-Dust attacks
- `bully` - Alternative WPS attacks
- `cowpatty`, `pyrit`, `tshark` - Handshake validation

## Supported Platforms

- **Kali Linux** (recommended)
- **ParrotSec OS**
- Other Debian-based distributions with latest tool versions

## Attack Methods

| Attack | Target | Time | Success Rate |
|--------|--------|------|--------------|
| WPS Pixie-Dust | WPS Networks | 1-10 min | High |
| WPS PIN Brute-Force | WPS Networks | 2-24 hours | Medium |
| WPA Handshake | WPA2 Networks | 5-30 min | Dict dependent |
| PMKID Capture | WPA2 Networks | <1 min | Medium |
| WEP | Legacy Networks | 5-20 min | High |

## Command Examples

```bash
# Target specific channel
sudo wifite2 -c 6

# 5GHz networks
sudo wifite2 -5

# Check captured handshake
sudo wifite2 --check-handshake /path/to/cap

# Crack from dictionary
sudo wifite2 --crack --wordlist wordlist2.txt
```

## FAQ

**Q: Is this legal?**
A: Yes, for authorized network testing only. Always get permission.

**Q: Which wireless card should I buy?**
A: Look for Realtek RTL88xxau, Mediatek MT7612U, or Atheros cards. USB adapters are convenient.

**Q: What's the difference from original Wifite?**
A: Wifite2 offers better stability, faster scanning, Python 3 support, and active maintenance.

**Q: Does it crack passwords?**
A: No, it captures handshakes and hashes. Use hashcat/aircrack-ng for cracking.

**Q: Can I use this on macOS/Windows?**
A: Wifite2 requires Linux. Use Kali Linux in a VM if needed.

## Troubleshooting

**Issue**: "error: wifite must be run as root"
- **Solution**: Prefix with `sudo` - use `sudo wifite2`

**Issue**: "error: Unable to find wireless interface"
- **Solution**: Your adapter may not support Monitor Mode. Check compatibility list.

**Issue**: No networks appearing
- **Solution**: Try `sudo airmon-ng check kill` and then `sudo wifite2`

## License

GNU General Public License v2.0 - See LICENSE file

## Contributing

Pull requests, bug reports, and feature requests welcome on GitHub.

## Credits

- **Original**: derv82 - [Wifite Project](https://github.com/derv82/wifite)
- **Wifite2**: @CyberDanish & community contributors
- **Dependencies**: Aircrack-ng, Hashcat, Reaver, and related tools

---

**[GitHub](https://github.com/derv82/wifite2)** | **[Issues](https://github.com/derv82/wifite2/issues)** | **Maintained by @CyberDanish**
