#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by @CyberDanish
import sys
import time
import os

class Color(object):
    ''' Helper object for easily printing colored text to the terminal. '''

    # Basic console colors
    colors = {
        'W' : '\033[0m',  # white (normal)
        'R' : '\033[91m', # bright red
        'G' : '\033[92m', # bright green
        'O' : '\033[93m', # bright yellow
        'B' : '\033[94m', # bright blue
        'P' : '\033[95m', # bright magenta
        'C' : '\033[96m', # bright cyan
        'GR': '\033[90m', # bright gray
        'D' : '\033[2m'   # dims current color. {W} resets.
    }

    # Helper string replacements (hacker-style)
    replacements = {
        '{+}': ' {W}{D}[{W}{G}>>{W}{D}]{W}',
        '{!}': ' {W}{D}[{R}!!{W}{D}]{W}',
        '{?}': ' {W}{D}[{C}??{W}{D}]{W}'
    }

    last_sameline_length = 0
    _term_size = (24, 80)
    _term_size_ts = 0.0

    @staticmethod
    def p(text):
        '''
        Prints text using colored format on same line.
        Example:
            Color.p('{R}This text is red. {W} This text is white')
        '''
        sys.stdout.write(Color.s(text))
        sys.stdout.flush()
        if '\r' in text:
            text = text[text.rfind('\r')+1:]
            Color.last_sameline_length = len(text)
        else:
            Color.last_sameline_length += len(text)

    @staticmethod
    def pl(text):
        '''Prints text using colored format with trailing new line.'''
        Color.p('%s\n' % text)
        Color.last_sameline_length = 0

    @staticmethod
    def pe(text):
        '''Prints text using colored format with leading and trailing new line to STDERR.'''
        sys.stderr.write(Color.s('%s\n' % text))
        Color.last_sameline_length = 0

    @staticmethod
    def s(text):
        ''' Returns colored string '''
        if '{' not in text:
            return text
        output = text
        for (key,value) in Color.replacements.items():
            output = output.replace(key, value)
        for (key,value) in Color.colors.items():
            output = output.replace('{%s}' % key, value)
        return output

    @staticmethod
    def clear_line():
        spaces = ' ' * Color.last_sameline_length
        sys.stdout.write('\r%s\r' % spaces)
        sys.stdout.flush()
        Color.last_sameline_length = 0

    @staticmethod
    def clear_entire_line():
        rows, columns = Color.terminal_size()
        Color.p('\r' + (' ' * int(columns)) + '\r')

    @staticmethod
    def terminal_size(cache_seconds=0.5):
        '''
        Returns (rows, columns) with a small cache to avoid frequent system calls.
        '''
        now = time.time()
        if now - Color._term_size_ts < cache_seconds:
            return Color._term_size

        rows, columns = 24, 80
        try:
            import shutil
            size = shutil.get_terminal_size(fallback=(80, 24))
            columns, rows = size.columns, size.lines
        except Exception:
            try:
                rows_s, columns_s = os.popen('stty size', 'r').read().split()
                rows, columns = int(rows_s), int(columns_s)
            except Exception:
                pass

        Color._term_size = (rows, columns)
        Color._term_size_ts = now
        return Color._term_size


    @staticmethod
    def pattack(attack_type, target, attack_name, progress):
        '''
        Prints a one-liner for an attack.
        Includes attack type (WEP/WPA), target ESSID & power, attack type, and progress.
        ESSID (Pwr) Attack_Type: Progress
        e.g.: Router2G (23db) WEP replay attack: 102 IVs
        '''
        essid = '{C}%s{W}' % target.essid if target.essid_known else '{O}unknown{W}'
        Color.p('\r{+} {G}%s{W} ({C}%sdb{W}) {G}%s {C}%s{W}: %s ' % (
            essid, target.power, attack_type, attack_name, progress))


    @staticmethod
    def pexception(exception):
        '''Prints an exception. Includes stack trace if necessary.'''
        Color.pl('\n{!} {R}Error: {O}%s' % str(exception))

        # Don't dump trace for the "no targets found" case.
        if 'No targets found' in str(exception):
            return

        from ..config import Configuration
        if Configuration.verbose > 0 or Configuration.print_stack_traces:
            Color.pl('\n{!} {O}Full stack trace below')
            from traceback import format_exc
            Color.p('\n{!}    ')
            err = format_exc().strip()
            err = err.replace('\n', '\n{!} {C}   ')
            err = err.replace('  File', '{W}File')
            err = err.replace('  Exception: ', '{R}Exception: {O}')
            Color.pl(err)
        # Always log exceptions for diagnostics (if possible)
        Configuration.log_exception()


if __name__ == '__main__':
    Color.pl('{R}Testing{G}One{C}Two{P}Three{W}Done')
    print(Color.s('{C}Testing{P}String{W}'))
    Color.pl('{+} Good line')
    Color.pl('{!} Danger')

