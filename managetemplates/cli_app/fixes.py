# no:vars_cleanup

import sys

from rich import print  # noqa

from managetemplates import constants
from managetemplates.cli_app import app
from managetemplates.utilities.template_var_syntax import content_template_var_syntax, filesystem_template_var_syntax


@app.command
def fix_filesystem():
    """
    Unify cookiecutter variables in the file/directory paths.
    e.g.: "/{{foo}}/{{bar}}.txt" -> "/{{ foo }}/{{ bar }}.txt"
    """
    rename_count = filesystem_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(rename_count)


@app.command
def fix_file_content():
    """
    Unify cookiecutter variables in file content.
    e.g.: "{{foo}}" -> "{{ foo }}"
    """
    fixed_files = content_template_var_syntax(path=constants.PACKAGE_ROOT)
    sys.exit(fixed_files)
