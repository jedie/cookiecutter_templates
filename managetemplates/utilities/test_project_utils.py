import os
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_dir

from managetemplates.utilities.subprocess_utils import verbose_check_output


class TestProject:
    def __init__(self, pkg_path: Path):
        assert_is_dir(pkg_path)
        self.pkg_path = pkg_path

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
