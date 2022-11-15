import shutil
from pathlib import Path

from bx_py_utils.path import assert_is_dir
from cookiecutter.main import cookiecutter

from managetemplates.cli import PACKAGE_ROOT


def run_cookiecutter(template_name: str, final_name: str, force_recreate=False):
    template_path = PACKAGE_ROOT / template_name
    assert_is_dir(template_path)

    output_dir = PACKAGE_ROOT / '.tests'

    # Create always a fresh checkout:
    final_path = output_dir / final_name
    if final_path.exists():
        if not force_recreate:
            # Reuse existing checkout
            return final_path

        shutil.rmtree(final_path)

    assert final_path.exists() is False

    destination = cookiecutter(
        template=str(PACKAGE_ROOT),
        directory=template_name,
        output_dir=output_dir,
        no_input=True,
    )
    pkg_path = Path(destination)
    assert_is_dir(pkg_path)

    assert pkg_path == final_path

    return pkg_path
