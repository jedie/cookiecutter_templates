import shutil
from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file
from cli_base.cli_tools.rich_utils import EncloseRuleContext
from rich import print

from managetemplates.constants import PACKAGE_ROOT


@EncloseRuleContext('Copy file+meta:')
def verbose_copy2(*, src: Path, dst: Path):
    assert_is_file(src)
    assert_is_dir(dst.parent)

    print(f'from: [magenta]{src.relative_to(PACKAGE_ROOT)}')
    print(f'to: [magenta]{dst.relative_to(PACKAGE_ROOT)}')

    shutil.copy2(
        src=src,
        dst=dst,
    )
