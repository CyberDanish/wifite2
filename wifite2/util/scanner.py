#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by @CyberDanish
from ..util.color import Color
from ..tools.airodump import Airodump
from ..util.input import raw_input, xrange
from ..model.target import Target, WPSState
from ..config import Configuration

from time import sleep, time

class Scanner(object):
    ''' Scans wifi networks & provides menu for selecting targets '''

    # Console code for moving up one line
    UP_CHAR = '\x1B[1F'
    BOX_MAX_WIDTH = 100

    def __init__(self):
        '''
        Scans for targets via Airodump.
        Loops until scan is interrupted via user or config.
        Note: Sets this object's `targets` attrbute (list[Target]) upon interruption.
        '''
        self.previous_target_count = 0
        self.targets = []
        self.target = None # Target specified by user (based on ESSID/BSSID)
        self._stop = False

        max_scan_time = Configuration.scan_time

        self.err_msg = None

        # Loads airodump with interface/channel/etc from Configuration
        import signal
        prev_handler = signal.getsignal(signal.SIGINT)
        def _handle_sigint(sig, frame):
            self._stop = True
        signal.signal(signal.SIGINT, _handle_sigint)

        try:
            with Airodump() as airodump:
                # Loop until interrupted (Ctrl+C)
                scan_start_time = time()

                while True:
                    if self._stop:
                        return
                    if airodump.pid.poll() is not None:
                        return  # Airodump process died

                    self.targets = airodump.get_targets(old_targets=self.targets)

                    if self.found_target():
                        return  # We found the target we want

                    if airodump.pid.poll() is not None:
                        return  # Airodump process died

                    for target in self.targets:
                        if target.bssid in airodump.decloaked_bssids:
                            target.decloaked = True

                    self.print_targets()

                    target_count = len(self.targets)
                    client_count = sum(len(t.clients) for t in self.targets)

                    outline = '\r{+} Scanning'
                    if airodump.decloaking:
                        outline += ' & decloaking'
                    outline += '. Found'
                    outline += ' {G}%d{W} target(s),' % target_count
                    outline += ' {G}%d{W} client(s).' % client_count
                    outline += ' {O}Ctrl+C{W} when ready '
                    Color.clear_entire_line()
                    Color.p(outline)

                    if max_scan_time > 0 and time() > scan_start_time + max_scan_time:
                        return

                    sleep(1)

        except KeyboardInterrupt:
            return
        finally:
            signal.signal(signal.SIGINT, prev_handler)


    def found_target(self):
        '''
        Detect if we found a target specified by the user (optional).
        Sets this object's `target` attribute if found.
        Returns: True if target was specified and found, False otherwise.
        '''
        bssid = Configuration.target_bssid
        essid = Configuration.target_essid

        if bssid is None and essid is None:
            return False  # No specific target from user.

        for target in self.targets:
            if Configuration.wps_only and target.wps not in [WPSState.UNLOCKED, WPSState.LOCKED]:
                continue
            if bssid and target.bssid and bssid.lower() == target.bssid.lower():
                self.target = target
                break
            if essid and target.essid and essid.lower() == target.essid.lower():
                self.target = target
                break

        if self.target:
            Color.pl('\n{+} {C}found target{G} %s {W}({G}%s{W})'
                % (self.target.bssid, self.target.essid))
            return True

        return False


    def print_targets(self):
        '''Prints targets selection menu (1 target per row).'''
        if len(self.targets) == 0:
            Color.p('\r')
            return

        box_width = self._box_width()
        header_lines = 5  # top border + title + columns + separator + bottom border

        if self.previous_target_count > 0:
            # We need to 'overwrite' the previous list of targets.
            if Configuration.verbose <= 1:
                # Don't clear screen buffer in verbose mode.
                if self.previous_target_count > len(self.targets) or \
                   Scanner.get_terminal_height() < self.previous_target_count + header_lines + 1:
                    # Either:
                    # 1) We have less targets than before, so we can't overwrite the previous list
                    # 2) The terminal can't display the targets without scrolling.
                    # Clear the screen.
                    # Clear screen without spawning a subprocess
                    Color.p('\033[2J\033[H')
                else:
                    # We can fit the targets in the terminal without scrolling
                    # 'Move' cursor up so we will print over the previous list
                    Color.pl(Scanner.UP_CHAR * (header_lines + self.previous_target_count))

        self.previous_target_count = len(self.targets)

        # Overwrite the current line
        Color.p('\r{W}{D}')

        # Boxed header
        Color.pl('{G}+%s+{W}' % ('-' * (box_width - 2)))
        self._box_line('{C}TARGETS{W} {D}(%d found){W}' % len(self.targets), box_width)

        # First row: columns
        columns = 'NUM'
        columns += '                      ESSID'
        if Configuration.show_bssids:
            columns += '              BSSID'
        columns += '   CH  ENCR  POWER  WPS?  CLIENT'
        self._box_line('{D}%s{W}' % columns, box_width)

        # Second row: separator
        sep = '---'
        sep += '  -------------------------'
        if Configuration.show_bssids:
            sep += '  -----------------'
        sep += '  ---  ----  -----  ----  ------'
        self._box_line('{D}%s{W}' % sep, box_width)

        # Remaining rows: targets
        for idx, target in enumerate(self.targets, start=1):
            Color.clear_entire_line()
            line = '{G}%s{W}  %s' % (str(idx).rjust(3), target.to_str(Configuration.show_bssids))
            self._box_line(line, box_width)

        # Box bottom
        Color.pl('{G}+%s+{W}' % ('-' * (box_width - 2)))

    @staticmethod
    def get_terminal_height():
        rows, _ = Color.terminal_size()
        return int(rows)

    @staticmethod
    def get_terminal_width():
        _, columns = Color.terminal_size()
        return int(columns)

    def _box_width(self):
        width = Scanner.get_terminal_width()
        if width <= 0:
            return 80
        width = min(width, Scanner.BOX_MAX_WIDTH)
        width = max(width, 60)
        return width

    def _visible_len(self, s):
        import re
        # Strip ANSI escapes
        s = re.sub(r'\x1b\\[[0-9;]*m', '', s)
        # Strip color tokens
        s = re.sub(r'\{[A-Z]{1,2}\}', '', s)
        return len(s)

    def _box_line(self, text, width):
        vis = self._visible_len(text)
        pad = ' ' * max(0, width - 4 - vis)
        Color.pl('{G}|{W} %s%s {G}|{W}' % (text, pad))

    def select_targets(self):
        '''
        Returns list(target)
        Either a specific target if user specified -bssid or --essid.
        Otherwise, prompts user to select targets and returns the selection.
        '''

        if self.target:
            # When user specifies a specific target
            return [self.target]

        if len(self.targets) == 0:
            if self.err_msg is not None:
                Color.pl(self.err_msg)

            # TODO Print a more-helpful reason for failure.
            # 1. Link to wireless drivers wiki,
            # 2. How to check if your device supporst monitor mode,
            # 3. Provide airodump-ng command being executed.
            raise Exception('No targets found.'
                + ' You may need to wait longer,'
                + ' or you may have issues with your wifi card')

        # Return all targets if user specified a wait time ('pillage').
        if Configuration.scan_time > 0:
            return self.targets

        # Ask user for targets.
        self.print_targets()
        Color.clear_entire_line()

        # Flush any stray input (e.g., leftover keypresses)
        try:
            import sys, termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            pass

        if self.err_msg is not None:
            Color.pl(self.err_msg)

        input_str  = '{+} select target(s)'
        input_str += ' ({G}1-%d{W})' % len(self.targets)
        input_str += ' separated by commas, dashes'
        input_str += ' or {G}all{W}: '

        chosen_targets = []

        for choice in raw_input(Color.s(input_str)).split(','):
            choice = choice.strip()
            if choice.lower() == 'all':
                chosen_targets = self.targets
                break
            if '-' in choice:
                # User selected a range
                (lower,upper) = [int(x) - 1 for x in choice.split('-')]
                for i in xrange(lower, min(len(self.targets), upper + 1)):
                    chosen_targets.append(self.targets[i])
            elif choice.isdigit():
                choice = int(choice) - 1
                chosen_targets.append(self.targets[choice])

        return chosen_targets


if __name__ == '__main__':
    # 'Test' script will display targets and selects the appropriate one
    Configuration.initialize()
    try:
        s = Scanner()
        targets = s.select_targets()
    except Exception as e:
        Color.pl('\r {!} {R}Error{W}: %s' % str(e))
        Configuration.exit_gracefully(0)
    for t in targets:
        Color.pl('    {W}Selected: %s' % t)
    Configuration.exit_gracefully(0)

