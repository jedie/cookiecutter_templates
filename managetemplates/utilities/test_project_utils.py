from __future__ import annotations

import os
from pathlib import Path

from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call, verbose_check_output


class TestProject:
    def __init__(self, pkg_path: Path, base_extra_env: dict | None = None):
        assert_is_dir(pkg_path)
        self.pkg_path = pkg_path
        self.base_extra_env = base_extra_env

    def _build_env(self, *, extra_env: dict | None):
        # Start with a "clean" environment.
        # This will also disable colored output ;)
        env = dict(PATH=os.environ['PATH'])
        if self.base_extra_env:
            env.update(self.base_extra_env)
        if extra_env:
            env.update(extra_env)
        return env

    def check_call(
        self,
        *popenargs,
        verbose: bool = True,
        exit_on_error: bool = True,
        extra_env: dict | None = None,
        **kwargs,
    ) -> str:
        return verbose_check_call(
            *popenargs,
            verbose=verbose,
            exit_on_error=exit_on_error,
            cwd=self.pkg_path,
            env=self._build_env(extra_env=extra_env),
            **kwargs,
        )

    def check_output(
        self,
        *popenargs,
        verbose: bool = True,
        exit_on_error: bool = True,
        extra_env: dict | None = None,
        **kwargs,
    ) -> str:
        return verbose_check_output(
            *popenargs,
            verbose=verbose,
            exit_on_error=exit_on_error,
            cwd=self.pkg_path,
            env=self._build_env(extra_env=extra_env),
            **kwargs,
        )
