#!/usr/bin/env python
import pstats
import os
import sys
import shutil
import subprocess
import tempfile


def _decode(strorbytes):
    if isinstance(strorbytes, str):
        return strorbytes
    return strorbytes.decode()


def _find_pytest():
    p = subprocess.Popen(['which', 'py.test'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    out = _decode(out).strip()
    return out


def _show_profile(profile_path):
    stats = pstats.Stats(profile_path)
    stats.strip_dirs()
    stats.sort_stats('tottime')
    stats.print_stats(50)


def _run_tests(profile_path, pytest_path, args):
    executable = sys.executable
    command = [executable, '-m', 'cProfile', '-o', profile_path, pytest_path]
    command.extend(args)
    print('Running: %s' % ' '.join(command))
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while p.poll() is None:
        print(_decode(p.stdout.readline()).strip())


def main(args):
    tmp = str(tempfile.mkdtemp())
    profile_path = os.path.join(tmp, 'profile')
    pytest_path = _find_pytest()
    _run_tests(profile_path, pytest_path, args)
    _show_profile(profile_path)
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main(sys.argv)
