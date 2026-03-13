#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by @CyberDanish
import time
import signal
import os
import shlex

from subprocess import Popen, PIPE

from ..util.color import Color
from ..config import Configuration


class Process(object):
    ''' Represents a running/ran process '''

    @staticmethod
    def devnull():
        ''' Helper method for opening devnull '''
        return open('/dev/null', 'w')

    @staticmethod
    def call(command, cwd=None, shell=False):
        '''
            Calls a command (either string or list of args).
            Returns tuple:
                (stdout, stderr)
        '''
        try:
            string_types = (basestring,)  # type: ignore
        except NameError:
            string_types = (str,)

        # Decide whether a shell is needed (pipes, redirects, etc.)
        needs_shell = shell or (
            isinstance(command, string_types) and any(ch in command for ch in ['|', '>', '<', ';', '&'])
        )

        if isinstance(command, string_types) and not needs_shell:
            # Allow string input without forcing a shell
            command = shlex.split(command)

        if needs_shell and not isinstance(command, string_types):
            # Shell expects a string command
            command = ' '.join(command)

        shell = bool(needs_shell)

        if Configuration.verbose > 1:
            if shell:
                Color.pe('\n {C}[?] {W} Executing (Shell): {B}%s{W}' % command)
            else:
                Color.pe('\n {C}[?]{W} Executing: {B}%s{W}' % command)

        pid = Popen(command, cwd=cwd, stdout=PIPE, stderr=PIPE, shell=shell)
        (stdout, stderr) = pid.communicate()

        # Python 3 compatibility
        if type(stdout) is bytes:
            stdout = stdout.decode('utf-8', errors='replace')
        if type(stderr) is bytes:
            stderr = stderr.decode('utf-8', errors='replace')


        if Configuration.verbose > 1 and stdout is not None and stdout.strip() != '':
            Color.pe('{P} [stdout] %s{W}' % '\n [stdout] '.join(stdout.strip().split('\n')))
        if Configuration.verbose > 1 and stderr is not None and stderr.strip() != '':
            Color.pe('{P} [stderr] %s{W}' % '\n [stderr] '.join(stderr.strip().split('\n')))

        return (stdout, stderr)

    @staticmethod
    def exists(program):
        ''' Checks if program is installed on this system '''
        # Try multiple common Kali Linux paths
        common_paths = [
            '/usr/bin/' + program,
            '/usr/local/bin/' + program,
            '/usr/sbin/' + program,
            '/usr/local/sbin/' + program,
            '/opt/aircrack-ng/bin/' + program,
            '/opt/aircrack-ng/sbin/' + program,
        ]
        
        # Check if file exists in common locations
        import os
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True
        
        # Try shutil.which() for PATH lookup
        try:
            import shutil
            if hasattr(shutil, 'which'):
                result = shutil.which(program)
                if result is not None:
                    return True
        except Exception:
            pass

        # Fallback to 'which' command via subprocess
        try:
            from subprocess import call
            import os
            with open(os.devnull, 'w') as devnull:
                result = call(['which', program], stdout=devnull, stderr=devnull)
                if result == 0:
                    return True
        except Exception:
            pass

        return False

    def __init__(self, command, devnull=False, stdout=PIPE, stderr=PIPE, cwd=None, bufsize=0, stdin=PIPE):
        ''' Starts executing command '''

        try:
            string_types = (basestring,)  # type: ignore
        except NameError:
            string_types = (str,)

        if isinstance(command, string_types):
            # Commands have to be a list
            command = shlex.split(command)

        self.command = command

        if Configuration.verbose > 1:
            Color.pe('\n {C}[?] {W} Executing: {B}%s{W}' % ' '.join(command))

        self.out = None
        self.err = None
        self._devnull_handles = []
        if devnull:
            sout = Process.devnull()
            serr = Process.devnull()
            self._devnull_handles = [sout, serr]
        else:
            sout = stdout
            serr = stderr

        self.start_time = time.time()

        self.pid = Popen(command, stdout=sout, stderr=serr, stdin=stdin, cwd=cwd, bufsize=bufsize)

    def __del__(self):
        '''
            Ran when object is GC'd.
            If process is still running at this point, it should die.
        '''
        try:
            if self.pid and self.pid.poll() is None:
                self.interrupt()
        except Exception:
            # Suppress destructor noise on shutdown/GC
            pass

    def stdout(self):
        ''' Waits for process to finish, returns stdout output '''
        self.get_output()
        if Configuration.verbose > 1 and self.out is not None and self.out.strip() != '':
            Color.pe('{P} [stdout] %s{W}' % '\n [stdout] '.join(self.out.strip().split('\n')))
        return self.out

    def stderr(self):
        ''' Waits for process to finish, returns stderr output '''
        self.get_output()
        if Configuration.verbose > 1 and self.err is not None and self.err.strip() != '':
            Color.pe('{P} [stderr] %s{W}' % '\n [stderr] '.join(self.err.strip().split('\n')))
        return self.err

    def stdoutln(self):
        return self.pid.stdout.readline()

    def stderrln(self):
        return self.pid.stderr.readline()

    def stdin(self, text):
        if self.pid.stdin:
            self.pid.stdin.write(text.encode('utf-8'))
            self.pid.stdin.flush()

    def get_output(self):
        ''' Waits for process to finish, sets stdout & stderr '''
        if self.pid.poll() is None:
            self.pid.wait()
        if self.out is None:
            (self.out, self.err) = self.pid.communicate()

        if type(self.out) is bytes:
            self.out = self.out.decode('utf-8', errors='replace')

        if type(self.err) is bytes:
            self.err = self.err.decode('utf-8', errors='replace')

        for h in getattr(self, '_devnull_handles', []):
            try:
                h.close()
            except Exception:
                pass
        self._devnull_handles = []

        return (self.out, self.err)

    def poll(self):
        ''' Returns exit code if process is dead, otherwise 'None' '''
        return self.pid.poll()

    def wait(self):
        self.pid.wait()

    def running_time(self):
        ''' Returns number of seconds since process was started '''
        return int(time.time() - self.start_time)

    def interrupt(self, wait_time=2.0):
        '''
            Send interrupt to current process.
            If process fails to exit within `wait_time` seconds, terminates it.
        '''
        try:
            pid = self.pid.pid
            cmd = self.command
            if type(cmd) is list:
                cmd = ' '.join(cmd)

            if Configuration.verbose > 1:
                Color.pe('\n {C}[?] {W} sending interrupt to PID %d (%s)' % (pid, cmd))

            os.kill(pid, signal.SIGINT)

            start_time = time.time()  # Time since Interrupt was sent
            while self.pid.poll() is None:
                # Process is still running
                time.sleep(0.1)
                if time.time() - start_time > wait_time:
                    # We waited too long for process to die, terminate it.
                    if Configuration.verbose > 1:
                        Color.pe('\n {C}[?] {W} Waited > %0.2f seconds for process to die, killing it' % wait_time)
                    os.kill(pid, signal.SIGTERM)
                    self.pid.terminate()
                    break

        except OSError as e:
            if 'No such process' in e.__str__():
                return
            raise e  # process cannot be killed


if __name__ == '__main__':
    Configuration.initialize(False)
    p = Process('ls')
    print(p.stdout())
    print(p.stderr())
    p.interrupt()

    # Calling as list of arguments
    (out, err) = Process.call(['ls', '-lah'])
    print(out)
    print(err)

    print('\n---------------------\n')

    # Calling as string
    (out, err) = Process.call('ls -l | head -2')
    print(out)
    print(err)

    print('"reaver" exists: %s' % Process.exists('reaver'))

    # Test on never-ending process
    p = Process('yes')
    print('Running yes...')
    time.sleep(1)
    print('yes should stop now')
    # After program loses reference to instance in 'p', process dies.

