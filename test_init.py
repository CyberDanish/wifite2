#!/usr/bin/env python
# Test script to check initialization

import sys
sys.path.insert(0, '.')

print("[TEST] Testing Wifite2 initialization...")
print("[TEST] Python version:", sys.version)

try:
    from wifite2.config import Configuration
    print("[OK] Configuration module imported")
except Exception as e:
    print("[ERROR] Failed to import Configuration:", e)
    sys.exit(1)

try:
    from wifite2.util.process import Process
    print("[OK] Process module imported")
    
    # Test some tools
    tools = ['aircrack-ng', 'airmon-ng', 'python', 'ls', 'which']
    for tool in tools:
        result = Process.exists(tool)
        status = "[FOUND]" if result else "[NOT FOUND]"
        print("[TEST] %s %s" % (status, tool))
except Exception as e:
    print("[ERROR] Failed Process.exists test:", e)
    import traceback
    traceback.print_exc()

print("\n[TEST] Test complete")
