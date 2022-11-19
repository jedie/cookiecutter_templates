import shlex
import subprocess
import sys
from pathlib import Path


def executable_which(file_name: str) -> Path:
    file_path = Path(file_name)
    if file_path.is_absolute():
        if not file_path.is_file():
            raise FileNotFoundError(f'File {file_name}!r does not exists!')
        return file_path

    venv_bin_path = Path(sys.executable).parent
    assert venv_bin_path.is_dir()
    bin_path = venv_bin_path / file_name
    if not bin_path.is_file():
        raise FileNotFoundError(f'File {file_name}!r not found in {venv_bin_path}')

    return bin_path


def print_info(popenargs, call_kwargs):
    print('\n')
    print('_' * 100)
    cwd = call_kwargs.get('cwd', Path.cwd())
    print(f'{cwd}$ {shlex.join(str(part) for part in popenargs)}')


def verbose_check_call(
    prog,
    *popenargs,
    verbose: bool = True,
    exit_on_error: bool = False,
    **kwargs,
):
    prog = executable_which(prog)
    final_args = [prog] + list(popenargs)

    if verbose:
        print_info(final_args, call_kwargs=kwargs)

    try:
        subprocess.check_call(final_args, **kwargs)
    except subprocess.CalledProcessError as err:
        if verbose:
            print(f'Process "{prog}" finished with exit code {err.returncode!r}')
        if exit_on_error:
            sys.exit(err.returncode)
        raise


def verbose_check_output(
    prog,
    *popenargs,
    verbose: bool = True,
    exit_on_error: bool = False,
    **kwargs,
):
    prog = executable_which(prog)
    final_args = [prog] + list(popenargs)

    if verbose:
        print_info(final_args, call_kwargs=kwargs)

    try:
        output = subprocess.check_output(final_args, **kwargs)
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
