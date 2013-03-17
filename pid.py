#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program listens to events from Supervisor, and writes/removes the PID
# of the processes managed by Supervisor to/from files.

import argparse
import os
import sys
import traceback


def write_stdout(s):
    """
    Write and flush immediately to stdout, as per Supervisor requirement.
    """
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    """
    Write and flush immediately to stderr, as per Supervisor requirement.
    """
    sys.stderr.write(s)
    sys.stderr.flush()


def write_pid_file(location, pid):
    """
    Write pid to the file
    """
    pid_file = open(location, 'w')
    pid_file.write(pid)
    pid_file.close()


def remove_pid_file(location):
    """
    Remove the file containing the pid
    """
    os.remove(location)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location',
                        default='/var/run/supervisor/{processname}.pid')
    args = parser.parse_args()
    while 1:
        write_stdout('READY\n')  # transition from ACKNOWLEDGED to READY
        # Catches all exceptions and redirect stacktraces to stderr so that the
        # event listener keeps running.
        try:
            line = sys.stdin.readline()  # read header line from stdin
            headers = dict([x.split(':') for x in line.split()])
            data = sys.stdin.read(int(headers['len']))  # read the event
            payload = dict(item.split(":") for item in data.split())
            if headers['eventname'] == 'PROCESS_STATE_RUNNING':
                location = args.location.format(**payload)
                write_pid_file(location, payload['pid'])
            elif headers['eventname'] == 'PROCESS_STATE_STOPPED':
                location = args.location.format(**payload)
                remove_pid_file(location)
        except Exception:
            write_stderr(traceback.format_exc())
        write_stdout('RESULT 2\nOK')  # transition from READY to ACKNOWLEDGED


if __name__ == '__main__':
    main()
