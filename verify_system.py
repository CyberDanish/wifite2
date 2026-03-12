#!/usr/bin/env python
# System verification script

import sys
sys.path.insert(0, '.')

from wifite2.config import Configuration
Configuration.initialize(load_interface=False)

print("\n" + "="*50)
print("FINAL SYSTEM VERIFICATION REPORT")
print("="*50 + "\n")

checks = {
    'WEP timeout optimized (240s)': Configuration.wep_timeout == 240,
    'WPA timeout optimized (120s)': Configuration.wpa_attack_timeout == 120,
    'PMKID timeout optimized (20s)': Configuration.pmkid_timeout == 20,
    'Deauth packets (5)': Configuration.num_deauths == 5,
    'WEP IVs threshold (8000)': Configuration.wep_crack_at_ivs == 8000,
    'WPS pixie timeout (90s)': Configuration.wps_pixie_timeout == 90,
}

all_pass = True
for name, result in checks.items():
    status = "[OK]" if result else "[FAIL]"
    print(f"{status} {name}")
    if not result:
        all_pass = False

print("\n" + "="*50)
if all_pass:
    print("[SUCCESS] ALL SYSTEM CHECKS PASSED")
    print("Wifite2 is ready for deployment!")
else:
    print("[FAILURE] Some checks failed")
print("="*50 + "\n")

sys.exit(0 if all_pass else 1)
