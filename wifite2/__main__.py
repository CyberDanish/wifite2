#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by @CyberDanish
try:
    from .config import Configuration
except (ValueError, ImportError) as e:
    raise Exception('You may need to run wifite2 from the root directory (which includes README.md)', e)

from .util.color import Color

import os
import sys


class Wifite2(object):

    def __init__(self):
        '''
        Initializes Wifite2. Checks for root permissions and ensures dependencies are installed.
        '''

        self.print_banner()

        Configuration.initialize(load_interface=False)
        Configuration.log('Wifite2 starting (version %s)' % Configuration.version)

        if os.getuid() != 0:
            Color.pl('{!} {R}error: {O}wifite2{R} must be run as {O}root{W}')
            Color.pl('{!} {R}re-run with {O}sudo{W}')
            Color.pl('{!}')
            Color.pl('{!} {G}On Kali Linux:{W}')
            Color.pl('{!} {C}sudo python3 Wifite2.py{W}')
            Color.pl('{!} {C}or: sudo wifite2{W}')
            Configuration.exit_gracefully(0)

        # Early dependency check for aircrack-ng
        from .util.process import Process
        Color.pl('{+} Checking for aircrack-ng...{W}')
        if not Process.exists('aircrack-ng'):
            Color.pl('{!} {R}ERROR: aircrack-ng not found!{W}')
            Color.pl('{!} {O}This is REQUIRED to run Wifite2{W}')
            Color.pl('{!}')
            Color.pl('{!} {G}Fix on Kali Linux:{W}')
            Color.pl('{!} {C}sudo apt update && sudo apt install -y aircrack-ng{W}')
            Color.pl('{!}')
            Color.pl('{!} {O}Debug: Checking common paths...{W}')
            import os
            paths = ['/usr/bin/aircrack-ng', '/usr/sbin/aircrack-ng', '/opt/aircrack-ng/bin/aircrack-ng']
            for p in paths:
                exists = os.path.exists(p)
                Color.pl('{!} {O}  %s: %s{W}' % (p, '{G}OK{W}' if exists else '{R}NOT FOUND{W}'))
            Configuration.exit_gracefully(1)
        Color.pl('{+} Found aircrack-ng {G}OK{W}')

        from .tools.dependency import Dependency
        Color.pl('{+} Running dependency check...{W}')
        Dependency.run_dependency_check()
        Color.pl('{+} All dependencies {G}OK{W}')


    def start(self):
        '''
        Starts target-scan + attack loop, or launches utilities dpeending on user input.
        '''
        from .model.result import CrackResult
        from .model.handshake import Handshake
        from .util.crack import CrackHelper

        if Configuration.show_cracked:
            CrackResult.display()

        elif Configuration.check_handshake:
            Handshake.check()

        elif Configuration.crack_handshake:
            CrackHelper.run()

        else:
            Configuration.get_monitor_mode_interface()
            self.scan_and_attack()


    def print_banner(self):
        '''Displays ASCII art of the highest caliber.'''
        Color.pl(r' {G}=============================================={W}')
        Color.pl(r' {G}  ____ _   _ ____  ____  ____  _  __')
        Color.pl(r' {G} / ___| | | |  _ \|  _ \|  _ \| |/ /')
        Color.pl(r' {G}| |   | |_| | |_) | |_) | | | | \' / ')
        Color.pl(r' {G}| |___|  _  |  __/|  __/| |_| | . \ ')
        Color.pl(r' {G} \____|_| |_|_|   |_|   |____/|_|\_\ ')
        Color.pl(r' {C}        WIFITE2  {D}%s{W}' % Configuration.version)
        Color.pl(r' {GR}{D} created by {C}@CyberDanish{W}')
        Color.pl(r' {G}=============================================={W}')
        Color.pl('')
        Color.pl(' {D}Python %s' % sys.version.split()[0])
        Color.pl(' {D}Platform: %s' % sys.platform)
        Color.pl('')


    def scan_and_attack(self):
        '''
        1) Scans for targets, asks user to select targets
        2) Attacks each target
        '''
        from .util.scanner import Scanner
        from .attack.all import AttackAll

        Color.pl('')

        # Scan
        s = Scanner()
        targets = s.select_targets()

        # Attack
        attacked_targets = AttackAll.attack_multiple(targets)

        Color.pl('{+} Finished attacking {C}%d{W} target(s), exiting' % attacked_targets)


##############################################################


def entry_point():
    try:
        wifite2 = Wifite2()
        wifite2.start()
    except KeyboardInterrupt:
        Color.pl('\n{!} {O}Interrupted, Shutting down...{W}')
    except Exception as e:
        import traceback
        Color.pl('\n{!} {R}ERROR: {W}%s' % str(e))
        if Configuration.verbose > 0:
            Color.pl('{!} {O}Traceback:{W}')
            traceback.print_exc()
    
    Configuration.exit_gracefully(0)


if __name__ == '__main__':
    entry_point()

