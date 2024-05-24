import subprocess
import os


def cls():
    """Функция очистки терминала"""
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

