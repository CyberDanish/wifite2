#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by @CyberDanish
class Dependency(object):
    required_attr_names = ['dependency_name', 'dependency_url', 'dependency_required']

    # https://stackoverflow.com/a/49024227
    def __init_subclass__(cls):
        for attr_name in cls.required_attr_names:
            if not attr_name in cls.__dict__:
                raise NotImplementedError(
                    'Attribute "{}" has not been overridden in class "{}"' \
                    .format(attr_name, cls.__name__)
                )


    @classmethod
    def exists(cls):
        from ..util.process import Process
        return Process.exists(cls.dependency_name)


    @classmethod
    def run_dependency_check(cls):
        from ..util.color import Color
        from ..config import Configuration

        from .airmon import Airmon
        from .airodump import Airodump
        from .aircrack import Aircrack
        from .aireplay import Aireplay
        from .ifconfig import Ifconfig
        from .iwconfig import Iwconfig
        from .bully import Bully
        from .reaver import Reaver
        from .wash import Wash
        from .pyrit import Pyrit
        from .tshark import Tshark
        from .macchanger import Macchanger
        from .hashcat import Hashcat, HcxDumpTool, HcxPcapTool

        apps = [
                # Aircrack - REQUIRED for any attack
                Aircrack, Airodump, Airmon, Aireplay,
                # wireless/net tools
                Iwconfig, Ifconfig,
                # WPS
                Reaver, Bully,
                # Cracking/handshakes
                Pyrit, Tshark,
                # Hashcat
                Hashcat, HcxDumpTool, HcxPcapTool,
                # Misc
                Macchanger
            ]

        missing_required = []
        missing_optional = []

        for app in apps:
            if app.exists():
                continue
            if app.dependency_required:
                missing_required.append(app)
                Color.p('{!} {O}Error: Required app {R}%s{O} was not found' % app.dependency_name)
                Color.pl('. {W}install @ {C}%s{W}' % app.dependency_url)
            else:
                missing_optional.append(app)

        if len(missing_optional) > 0:
            if Configuration.verbose > 0:
                for app in missing_optional:
                    Color.p('{!} {O}Warning: Recommended app {R}%s{O} was not found' % app.dependency_name)
                    Color.pl('. {W}install @ {C}%s{W}' % app.dependency_url)
            else:
                names = ', '.join([app.dependency_name for app in missing_optional])
                Color.pl('{!} {O}Recommended tools missing: {R}%s{W}' % names)
                Color.pl('{!} {O}Tip: run with {C}-v{O} for install links{W}')

        if len(missing_required) > 0:
            Color.pl('{!} {R}=== DEPENDENCY CHECK FAILED ==={W}')
            Color.pl('{!} {O}Fix for Kali Linux:{W}')
            Color.pl('{!} {G}sudo apt update && sudo apt install -y aircrack-ng{W}')
            Color.pl('{!} {O}Or:{W}')
            Color.pl('{!} {G}sudo apt install -y aircrack-ng macchanger tshark{W}')
            Color.pl('{!}')
            Color.pl('{!} {R}At least 1 Required app is missing. Make sure aircrack-ng is installed!{W}')
            import sys
            sys.exit(-1)


    @classmethod
    def fails_dependency_check(cls):
        from ..util.color import Color
        from ..util.process import Process

        if Process.exists(cls.dependency_name):
            return False

        if cls.dependency_required:
            Color.p('{!} {O}Error: Required app {R}%s{O} was not found' % cls.dependency_name)
            Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
            return True

        else:
            Color.p('{!} {O}Warning: Recommended app {R}%s{O} was not found' % cls.dependency_name)
            Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
            return False

