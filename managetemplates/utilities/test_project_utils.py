import dataclasses
import os
import subprocess
from pathlib import Path
from unittest.mock import patch

from bx_py_utils.path import assert_is_dir

from managetemplates.utilities.subprocess_utils import verbose_check_call, verbose_check_output


class TestProject:
    def __init__(self, pkg_path: Path):
        assert_is_dir(pkg_path)
        self.pkg_path = pkg_path

    def check_call(
        self,
        *popenargs,
        verbose: bool = True,
        exit_on_error: bool = False,
        **kwargs,
    ) -> str:
        kwargs.setdefault('text', True)
        env = dict(PATH=os.environ['PATH'])  # Use a clean environment
        return verbose_check_call(
            *popenargs,
            verbose=verbose,
            exit_on_error=exit_on_error,
            cwd=self.pkg_path,
            env=env,
            **kwargs,
        )

    def check_output(
        self,
        *popenargs,
        verbose: bool = True,
        exit_on_error: bool = False,
        **kwargs,
    ) -> str:
        kwargs.setdefault('text', True)
        env = dict(PATH=os.environ['PATH'])  # Use a clean environment
        return verbose_check_output(
            *popenargs,
            verbose=verbose,
            exit_on_error=exit_on_error,
            cwd=self.pkg_path,
            env=env,
            stderr=subprocess.STDOUT,
            **kwargs,
        )


@dataclasses.dataclass
class Call:
    args: tuple
    kwargs: dict


class SubprocessCallMock:
    def __init__(self):
        self.calls = []

    def __enter__(self):
        self.m = patch.object(subprocess, 'call', self)
        self.m.__enter__()
        return self

    def __call__(self, *args, **kwargs):
        self.calls.append(Call(args, kwargs))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.m.__exit__(exc_type, exc_val, exc_tb)
