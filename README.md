Wifite2 - Created by @CyberDanish
======

Maintainer: @CyberDanish (https://github.com/CyberDanish)  
Repo: https://github.com/CyberDanish/wifite2

One command. Full workflow.
Wifite2 orchestrates trusted wireless tools to scan, capture, and crack in a single run with a clean, hacker-style UI.

Badges
------
![OS](https://img.shields.io/badge/OS-Kali%20%7C%20Parrot-00e5ff)
![Python](https://img.shields.io/badge/Python-2%20%7C%203-33ff88)
![License](https://img.shields.io/badge/License-MIT-ff3d3d)

Quick Start
-----------
```bash
git clone https://github.com/CyberDanish/wifite2
cd wifite2
sudo ./Wifite2.py
```

Install
-------
```bash
sudo python setup.py install
```
Then run:
```bash
sudo wifite2
```

Easy Install (Kali/Parrot)
--------------------------
```bash
chmod +x install.sh
sudo ./install.sh
```

Why Wifite2
----------
* Zero-friction workflow: scan -> capture -> validate -> crack
* WPA2 handshake + PMKID flows in one place
* Smart defaults with speed-tuned timeouts
* Clean terminal UX for fast decision-making

Requirements (Short)
--------------------
* Kali Linux (recommended) or Parrot
* Monitor mode + injection-capable Wi-Fi adapter
* Aircrack-ng suite: `airmon-ng`, `airodump-ng`, `aireplay-ng`, `aircrack-ng`
* Python 2 or 3

Optional Tools
--------------
* `tshark`
* `reaver` or `bully`
* `cowpatty`
* `pyrit`
* `hashcat` + `hcxdumptool`/`hcxpcaptool`

Features (Short)
----------------
* WPS Pixie-Dust and PIN attacks
* WPA2 handshake capture + offline crack
* PMKID capture + offline crack
* WEP attacks (replay, chopchop, fragment, hirte, p0841, caffe-latte)
* Handshake validation via multiple tools
* Decloak hidden SSIDs during scans (fixed channel)

Common Flags
------------
* `--pmkid`        PMKID-only capture (skip WPS/WPA2)
* `--wps-only`     WPS-only attacks
* `--no-wps`       Disable WPS attacks
* `--crack`        Crack captured handshakes
* `--wpat`         WPA2 attack timeout
* `--wpadt`        WPA2 deauth interval

Workflow (High-Level)
---------------------
```mermaid
flowchart LR
    A[Scan] --> B[Select Targets]
    B --> C[Capture Handshake/PMKID]
    C --> D[Validate]
    D --> E[Crack Offline]

    classDef neon fill:#0b1f2a,stroke:#00e5ff,color:#e8f8ff,stroke-width:2px;
    classDef ember fill:#1a0f0f,stroke:#ff3d3d,color:#ffecec,stroke-width:2px;
    classDef synth fill:#0f1a14,stroke:#33ff88,color:#eafff3,stroke-width:2px;

    class A neon;
    class B synth;
    class C neon;
    class D synth;
    class E ember;
```

Recent Improvements
-------------------
* Safer, faster subprocess handling
* Smoother UI updates + hacker-style banner
* Brighter, more readable terminal colors
* Faster default timeouts (tunable via flags)

Note
----
Use only on networks you own or have explicit permission to test.
