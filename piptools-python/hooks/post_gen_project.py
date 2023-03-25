import sys
from pathlib import Path

from manageprojects.utilities.subprocess_utils import verbose_check_call


# current working directory is the root of the generated cookiecutter project
generated_path = Path().cwd()

# Update requirements:
verbose_check_call(sys.executable, 'cli.py', 'update', cwd=generated_path, env=dict())
