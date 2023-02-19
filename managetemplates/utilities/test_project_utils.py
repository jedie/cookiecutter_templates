import os
from pathlib import Path

from bx_py_utils.path import assert_is_dir
from manageprojects.utilities.subprocess_utils import verbose_check_call, verbose_check_output


class TestProject:
    def __init__(self, pkg_path: Path):
        assert_is_dir(pkg_path)
        self.pkg_path = pkg_path

    def check_call(
        self,
        *popenargs,
        verbose: bool = True,
        exit_on_error: bool = False,
        extra_env: dict | None = None,
        **kwargs,
    ) -> str:
        env = dict(os.environ)
        if extra_env:
            env.update(extra_env)

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
        extra_env: dict | None = None,
        **kwargs,
    ) -> str:
        env = dict(PATH=os.environ['PATH'])  # Use a clean environment
        if extra_env:
            env.update(extra_env)

        return verbose_check_output(
            *popenargs,
            verbose=verbose,
            exit_on_error=exit_on_error,
            cwd=self.pkg_path,
            env=env,
            **kwargs,
        )
