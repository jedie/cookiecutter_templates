import shlex
import subprocess
import sys
from pathlib import Path


def print_info(popenargs, call_kwargs):
    print('\n')
    print('_' * 100)
    cwd = call_kwargs.get('cwd', Path.cwd())
    print(f'{cwd}$ {shlex.join(str(part) for part in popenargs)}')


def verbose_check_call(*popenargs, verbose: bool = True, exit_on_error: bool = False, **kwargs):
    if verbose:
        print_info(popenargs, call_kwargs=kwargs)

    try:
        subprocess.check_call(popenargs, **kwargs)
    except subprocess.CalledProcessError as err:
        if verbose:
            print(f'Process "{popenargs[0]}" finished with exit code {err.returncode!r}')
        if exit_on_error:
            sys.exit(err.returncode)
        raise


def verbose_check_output(*popenargs, verbose: bool = True, exit_on_error: bool = False, **kwargs):
    if verbose:
        print_info(popenargs, call_kwargs=kwargs)

    try:
        output = subprocess.check_output(popenargs, **kwargs)
    except subprocess.CalledProcessError as err:
        print('-' * 100)
        print(err.output)
        print('-' * 100)
        print(f'Process "{popenargs[0]}" finished with exit code {err.returncode!r}')
        if exit_on_error:
            sys.exit(err.returncode)
        raise
    else:
        return output
