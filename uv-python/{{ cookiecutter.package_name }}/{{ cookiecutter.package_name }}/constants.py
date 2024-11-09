from pathlib import Path

import {{ cookiecutter.package_name }}


CLI_EPILOG = 'Project Homepage: {{ cookiecutter.package_url }}'

BASE_PATH = Path({{ cookiecutter.package_name }}.__file__).parent
