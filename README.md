# Wifite2

**Automated Wireless Network Auditor**

Created by [@CyberDanish](https://github.com/CyberDanish)

Wifite2 is a powerful Python script for auditing wireless networks. It automates the process of capturing and cracking WEP, WPA, and WPS encrypted networks using various attack methods.

## Features

- **WPS Attacks**: Pixie-Dust offline attack and PIN brute-force attack
- **WPA Attacks**: Handshake capture and PMKID hash capture with offline cracking
- **WEP Attacks**: Multiple methods including fragmentation, chop-chop, and replay attacks
- **Fast Scanning**: Real-time target discovery with power levels
- **Optimized Performance**: Reduced timeouts for quicker attack cycles
- **Cross-Platform**: Works on Kali Linux and other penetration testing distributions
- **Educational**: Verbose mode shows executed commands for learning

## Requirements

### Hardware
- Wireless card supporting Monitor Mode and packet injection
- Compatible cards: [Check compatibility](http://www.aircrack-ng.org/doku.php?id=compatible_cards)

### Software
**Required:**
- Python 2.7+ or 3.x
- Aircrack-ng suite (airmon-ng, airodump-ng, aireplay-ng, aircrack-ng, packetforge-ng)
- iw or iwconfig, ip or ifconfig

**Recommended:**
- tshark (Wireshark) for WPS detection
- reaver or bully for WPS attacks
- cowpatty or pyrit for handshake validation
- hashcat for PMKID cracking
- hcxdumptool and hcxpcaptool for PMKID capture

## Installation

### Quick Install
```bash
git clone https://github.com/CyberDanish/wifite2.git
cd wifite2
sudo python setup.py install
sudo wifite2
```

### Alternative Installation
```bash
pip install .
```

## Usage

### Basic Usage
```bash
sudo wifite2
```

### Advanced Options
```bash
sudo wifite2 --help
```

### Common Commands
- Scan for WPS networks: `sudo wifite2 --wps`
- Target specific channel: `sudo wifite2 -c 6`
- Use PMKID only: `sudo wifite2 --pmkid`
- Crack existing handshake: `sudo wifite2 --crack`

## Attack Methods

1. **WPS Pixie-Dust**: Fast offline attack against vulnerable WPS implementations
2. **WPS PIN Attack**: Brute-force WPS PIN with optimized timing
3. **PMKID Capture**: Capture PMKID hashes for offline cracking
4. **Handshake Capture**: Deauthenticate clients to capture WPA handshakes
5. **WEP Attacks**: Various injection-based attacks

## Performance Optimizations

- Pixie-Dust timeout: 60 seconds (vs 300s)
- Failure thresholds reduced for faster failure detection
- Real-time target refresh every second
- Parallel attack validation

## Troubleshooting

- Ensure wireless card supports injection
- Run as root/sudo
- Update Aircrack-ng to latest version
- Check dependencies with verbose mode: `wifite2 -v`

## Disclaimer

This tool is for educational and authorized testing purposes only. Use responsibly and in compliance with local laws.

## License

GNU GPLv2
