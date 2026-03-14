#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .dependency import Dependency

class Ifconfig(Dependency):
    dependency_required = True
    dependency_name = 'ifconfig or ip'
    dependency_url = 'apt-get install net-tools or iproute2'

    @classmethod
    def _run_command(cls, command):
        from ..util.process import Process
        pid = Process(command)
        pid.wait()
        if pid.poll() != 0:
            raise Exception('Error running command %s:\n%s\n%s' % (command, pid.stdout(), pid.stderr()))
        return pid

    @classmethod
    def up(cls, interface, args=[]):
        '''Put interface up'''
        try:
            # Try modern 'ip' command first
            command = ['ip', 'link', 'set', 'dev', interface, 'up']
            cls._run_command(command)
        except:
            # Fallback to ifconfig
            command = ['ifconfig', interface]
            if type(args) is list:
                command.extend(args)
            elif type(args) == 'str':
                command.append(args)
            command.append('up')
            cls._run_command(command)

    @classmethod
    def down(cls, interface):
        '''Put interface down'''
        try:
            # Try modern 'ip' command first
            cls._run_command(['ip', 'link', 'set', 'dev', interface, 'down'])
        except:
            # Fallback to ifconfig
            cls._run_command(['ifconfig', interface, 'down'])

    @classmethod
    def get_mac(cls, interface):
        from ..util.process import Process

        try:
            # Try modern 'ip' command first
            output = Process(['ip', 'addr', 'show', interface]).stdout()
            match = re.search(r'ether\s+([a-fA-F0-9:]{17})', output)
        except:
            # Fallback to ifconfig
            output = Process(['ifconfig', interface]).stdout()
            # Mac address separated by dashes or colons
            mac_dash_regex = ('[a-zA-Z0-9]{2}-' * 6)[:-1]
            mac_colon_regex = ('[a-zA-Z0-9]{2}:' * 6)[:-1]
            match = re.search(' ({})'.format(mac_dash_regex), output) or re.search(' ({})'.format(mac_colon_regex), output)

        if match:
            return match.group(1).replace('-', ':').lower()
        else:
            raise Exception('Could not find MAC address for interface %s' % interface)

