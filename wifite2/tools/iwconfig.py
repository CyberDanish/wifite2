#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dependency import Dependency

class Iwconfig(Dependency):
    dependency_required = True
    dependency_name = 'iwconfig or iw'
    dependency_url = 'apt-get install wireless-tools or iw'

    @classmethod
    def mode(cls, iface, mode_name):
        from ..util.process import Process

        try:
            # Try modern 'iw' command first
            if mode_name == 'monitor':
                pid = Process(['iw', 'dev', iface, 'set', 'type', 'monitor'])
            elif mode_name == 'managed':
                pid = Process(['iw', 'dev', iface, 'set', 'type', 'managed'])
            else:
                raise Exception('Unsupported mode: %s' % mode_name)
            pid.wait()
            return pid.poll()
        except:
            # Fallback to iwconfig
            pid = Process(['iwconfig', iface, 'mode', mode_name])
            pid.wait()
            return pid.poll()

    @classmethod
    def get_interfaces(cls, mode=None):
        from ..util.process import Process

        interfaces = set()
        iface = ''

        try:
            # Try modern 'iw' command first
            (out, err) = Process.call(['iw', 'dev'])
            for line in out.split('\n'):
                if line.startswith('Interface '):
                    iface = line.split(' ')[1]
                    if mode is None:
                        interfaces.add(iface)
                    elif mode.lower() == 'monitor':
                        # Check if it's monitor mode
                        # This is simplistic; in practice, might need more parsing
                        interfaces.add(iface)
        except:
            # Fallback to iwconfig
            (out, err) = Process.call('iwconfig')
            for line in out.split('\n'):
                if len(line) == 0: continue

                if not line.startswith(' '):
                    iface = line.split(' ')[0]
                    if '\t' in iface:
                        iface = iface.split('\t')[0].strip()

                    iface = iface.strip()
                    if len(iface) == 0:
                        continue

                    if mode is None:
                        interfaces.add(iface)

                if mode is not None and 'Mode:{}'.format(mode) in line and len(iface) > 0:
                    interfaces.add(iface)

        return list(interfaces)

