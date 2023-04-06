import shutil
from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file
from rich import print

from managetemplates.constants import PACKAGE_ROOT


def verbose_copy2(*, src: Path, dst: Path):
    print('[cyan]Copy file+meta:')

    assert_is_file(src)
    assert_is_dir(dst.parent)

    print(f'\tfrom: [magenta]{src.relative_to(PACKAGE_ROOT)}')
    print(f'\tto: [magenta]{dst.relative_to(PACKAGE_ROOT)}')

    shutil.copy2(
        src=src,
        dst=dst,
    )
