# Wifite2 - Advanced Wireless Network Auditor & WiFi Cracking Tool
**Created & Maintained by @CyberDanish**

> **Wifite2** is a professional-grade, open-source wireless network auditing tool and automated WiFi penetration testing platform. Designed for security professionals, penetration testers, and network administrators who need to audit wireless network security and crack WEP, WPA, WPA2, and WPS encrypted networks efficiently.

## Overview

Wifite2 is a complete modernization of the original [`wifite`](https://github.com/derv82/wifite) wireless auditing framework, now enhanced and actively maintained by @CyberDanish. This powerful WiFi hacking and penetration testing tool automates wireless security testing, eliminating the need to memorize complex command-line arguments and switches. 

**Wifite2** runs existing wireless-auditing tools for you with an intuitive interface. Whether you're performing WiFi security assessments, wireless penetration testing, or network vulnerability scanning, Wifite2 streamlines the entire process.

## Key Features

Wifite2 is engineered to use all known methods for retrieving the password of a wireless access point (router). This includes comprehensive support for:

## Attack Methods & Supported Encryption Standards

Wifite2 supports multiple wireless security cracking techniques:

1. **WPS Attacks**
   - [Offline Pixie-Dust attack](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Offline_brute-force_attack) - Exploits WPS PIN vulnerabilities
   - [Online Brute-Force PIN attack](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Online_brute-force_attack) - Iterative WPS PIN cracking

2. **WPA/WPA2 Attacks**
   - [WPA Handshake Capture](https://hashcat.net/forum/thread-7717.html) + offline dictionary/brute-force cracking
   - [PMKID Hash Capture](https://hashcat.net/forum/thread-7717.html) + offline crack using hashcat

3. **WEP Attacks**
   - Multiple known WEP cracking techniques including fragmentation, chop-chop, aireplay, and other legacy wireless security exploits

**Result**: Select your targets, and Wifite2 will automatically start trying to capture and crack WiFi passwords using the most effective attack vectors for each network.

## System Requirements & Hardware

### Wireless Adapter Requirements
To use Wifite2 effectively, you need a wireless card capable of **Monitor Mode** and **packet injection**. This is essential for WiFi penetration testing and network auditing. 

- **Monitor Mode**: Allows sniffing wireless frames
- **Packet Injection**: Enables deauthentication attacks and testing

Resources:
- [Aircrack-ng Compatible Wireless Card List](http://www.aircrack-ng.org/doku.php?id=compatible_cards)
- [Affordable USB WiFi adapters](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Offline_brute-force_attack) are widely available

### Software Dependencies & Required Tools

**Required:**

* `python`: Wifite2 is compatible with both `python2` and `python3`.
* [`iwconfig`](https://wiki.debian.org/iwconfig): For identifying wireless devices already in Monitor Mode.
* [`ifconfig`](https://en.wikipedia.org/wiki/Ifconfig): For starting/stopping wireless devices.
* [`Aircrack-ng`](http://aircrack-ng.org/) suite, includes:
   * [`airmon-ng`](https://tools.kali.org/wireless-attacks/airmon-ng): For enumerating and enabling Monitor Mode on wireless devices.
   * [`aircrack-ng`](https://tools.kali.org/wireless-attacks/aircrack-ng): For cracking WEP .cap files and WPA handshake captures.
   * [`aireplay-ng`](https://tools.kali.org/wireless-attacks/aireplay-ng): For deauthing access points, replaying capture files, various WEP attacks.
   * [`airodump-ng`](https://tools.kali.org/wireless-attacks/airodump-ng): For target scanning & capture file generation.
   * [`packetforge-ng`](https://tools.kali.org/wireless-attacks/packetforge-ng): For forging capture files.

**Optional, but Recommended:**

* [`tshark`](https://www.wireshark.org/docs/man-pages/tshark.html): For detecting WPS networks and inspecting handshake capture files.
* [`reaver`](https://github.com/t6x/reaver-wps-fork-t6x): For WPS Pixie-Dust & brute-force attacks.
   * Note: Reaver's `wash` tool can be used to detect WPS networks if `tshark` is not found.
* [`bully`](https://github.com/aanarchyy/bully): For WPS Pixie-Dust & brute-force attacks.
   * Alternative to Reaver. Specify `--bully` to use Bully instead of Reaver.
   * Bully is also used to fetch PSK if `reaver` cannot after cracking WPS PIN.
* [`coWPAtty`](https://tools.kali.org/wireless-attacks/cowpatty): For detecting handshake captures.
* [`pyrit`](https://github.com/JPaulMora/Pyrit): For detecting handshake captures.
* [`hashcat`](https://hashcat.net/): For cracking PMKID hashes.
   * [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool): For capturing PMKID hashes.
   * [`hcxpcaptool`](https://github.com/ZerBea/hcxtools): For converting PMKID packet captures into `hashcat`'s format.


## Quick Start Guide - Running Wifite2

### Method 1: Direct Execution (From Git Repository)

```bash
git clone https://github.com/derv82/wifite2.git
cd wifite2
sudo python3 Wifite2.py
```

### Method 2: Install as System Command

To install Wifite2 as a system-wide command (available from any terminal):

```bash
sudo python3 setup.py install
```

This will install Wifite2 to `/usr/sbin/wifite2`, making it accessible system-wide as the `wifite2` command.

**Note**: For legacy support, backward-compatible `wifite` symlinks may be created.

### Uninstalling Wifite2

The standard Python setup.py uninstall process is complex. To cleanly remove Wifite2:

```bash
# Record installation
sudo python3 setup.py install --record files.txt

# Remove all files
cat files.txt | xargs sudo rm

# Cleanup
rm -f files.txt
```

## Advanced Features & Capabilities
* **PMKID Hash Cracking** - Capture and crack PMKID hashes using hashcat (`--pmkid`)
* **WPS Pixie-Dust Attack** - Offline WPS PIN cracking using Pixie-Dust vulnerability (`--wps-only --pixie`)
* **WPS PIN Brute-Force** - Online WPS brute-force PIN attack (`--wps-only --no-pixie`)
* **WPA/WPA2 4-Way Handshake** - Capture and offline dictionary/brute-force crack WPA handshakes (`--no-wps`)
* **Handshake Validation** - Validates captures against multiple tools (pyrit, tshark, cowpatty, aircrack-ng)
* **WEP Attacks** - Multiple WEP cracking techniques (replay, chopchop, fragment, hirte, p0841, caffe-latte)
* **Hidden Network Decloaking** - Automatically decloaks and targets hidden/cloaked WiFi networks
* **5GHz Support** - Extended support for 802.11ac (5GHz) wireless networks (`-5` option)
* **Persistent Storage** - Automatically saves cracked passwords and handshakes locally
* **Dictionary Cracking** - Easy integration with wordlists and offline cracking (`--crack`)
* **Real-time Monitoring** - Live display of signal strength and attack progress
* **Python 3 Support** - Modern Python 3 compatibility with legacy Python 2.7 support
* **Verbose Logging** - Detailed command execution and output for debugging (`--verbose`, `-vv`, `-vvv`)

## What Makes Wifite2 Better Than Wifite

## Improvements Over Original Wifite

### Stability & Reliability
- **Better Process Management** - No stray background processes left running
- **Modular Architecture** - Clean separation of concerns with unit tests
- **Easier Maintenance** - Pull requests and contributions are streamlined

### Performance
- **Faster Scanning** - Target refresh rate improved from 5 seconds to 1 second
- **Real-time Feedback** - Live signal strength and attack progress display
- **Detailed Reporting** - Enhanced attack information (progress percentages, step indices, etc.)

### Usability & Learning
- **Verbose Logging** - Execute commands with full transparency (`--verbose`, `-vv`, `-vvv`)
- **Better Help** - Try `wifite2 -h -v` for comprehensive option documentation
- **Cleaner Interface** - Improved ASCII banner and user experience

### Modern Development
- **Python 3 First** - Full Python 3 support with Python 2.7 compatibility
- **Active Maintenance** - Regular updates and improvements by @CyberDanish
- **Community-Driven** - Easier contributions and bug fixes

## Command-Line Usage Examples

### Basic WiFi Network Scanning
```bash
sudo wifite2
```

### WPS Pixie-Dust Attack Only
```bash
sudo wifite2 --wps-only --pixie
```

### WPA Handshake & Dictionary Crack
```bash
sudo wifite2 --no-wps --crack --wordlist wordlist2.txt
```

### PMKID Hash Attack
```bash
sudo wifite2 --pmkid
```

### Verbose Debugging Mode
```bash
sudo wifite2 -vvv
```

### Target Specific Channel
```bash
sudo wifite2 -c 6
```

### Check Captured Handshake
```bash
sudo wifite2 --check-handshake
```

## Screenshots & Visual Demonstrations
![Pixie-Dust with Reaver to get PIN and Bully to get PSK](https://i.imgur.com/Q5KSDbg.gif)

-------------

Cracking WPA key using PMKID attack:
![PMKID attack](https://i.imgur.com/CR8oOp0.gif)

-------------

Decloaking & cracking a hidden access point (via the WPA Handshake attack):
![Decloaking and Cracking a hidden access point](https://i.imgur.com/F6VPhbm.gif)

-------------

Cracking a weak WEP password (using the WEP Replay attack):
![Cracking a weak WEP password](https://i.imgur.com/jP72rVo.gif)

-------------

Cracking a pre-captured handshake using John The Ripper (via the `--crack` option):
![--crack option](https://i.imgur.com/iHcfCjp.gif)

---

## Frequently Asked Questions (FAQ)

### Q: Is Wifite2 legal to use?
**A:** Wifite2 is a legitimate security auditing and penetration testing tool. It's legal to use on networks you own or have explicit permission to test. Unauthorized network access is illegal; always ensure you have proper authorization before testing any wireless network.

### Q: What's the difference between Wifite2 and Wifite?
**A:** Wifite2 is a modernized rebuild with better stability, faster performance, improved process management, Python 3 support, and active maintenance by the community.

### Q: Which Linux distributions are supported?
**A:** Wifite2 is optimized for Kali Linux and ParrotSec. Other penetration testing distributions may work but require the latest versions of all dependencies and proper wireless driver support.

### Q: Can Wifite2 crack WiFi passwords?
**A:** Wifite2 automates the process of capturing WiFi handshakes and password hashes. It doesn't directly crack passwords but simplifies using cracking tools like hashcat and aircrack-ng.

### Q: What wireless cards are compatible?
**A:** Wifite2 requires cards supporting Monitor Mode and packet injection. See the [Aircrack-ng compatible cards list](http://www.aircrack-ng.org/doku.php?id=compatible_cards).

### Q: Is Python 2 still supported?
**A:** Yes, Wifite2 maintains backward compatibility with Python 2.7, but Python 3 is recommended and receives primary support.

## SEO Keywords & Search Terms

This tool is indexed under: **WiFi cracking**, **wireless security auditing**, **WPA cracking**, **WEP attack**, **WPS penetration testing**, **WiFi penetration tester**, **wireless network auditor**, **aircrack-ng automation**, **WiFi password cracker**, **802.11 security testing**, **Kali Linux WiFi tools**, **PMKID attack**, **Pixie-Dust attack**, **WPA2 handshake**, **network penetration testing**, **wireless vulnerability scanner**, **WiFi security assessment**, **Wifite fork**, **CyberDanish security tools**

## Credits & Attribution

- **Original Author**: derv82 (original [Wifite project](https://github.com/derv82/wifite))
- **Wifite2 Maintainer**: @CyberDanish
- **Dependencies**: Aircrack-ng suite, Hashcat, Reaver, Bully, and other open-source wireless tools
- **Community**: Thanks to all contributors and testers

## License

Wifite2 is licensed under **GNU General Public License v2.0**. See LICENSE file for full details.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or pull request on the GitHub repository.

---

**Maintained by @CyberDanish** | [GitHub Repository](https://github.com/derv82/wifite2) | WiFi Security Auditing Made Easy
