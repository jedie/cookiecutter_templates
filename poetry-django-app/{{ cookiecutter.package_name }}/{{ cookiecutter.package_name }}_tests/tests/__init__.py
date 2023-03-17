from pathlib import Path

import {{ cookiecutter.package_name }}


PACKAGE_ROOT = Path({{ cookiecutter.package_name }}.__file__).parent.parent
