import subprocess
import os



def cls():
    """Функция очистки терминала, можно задать время ожидания перед очисткой"""
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

