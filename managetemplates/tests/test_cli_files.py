import os
from pathlib import Path
from unittest import TestCase

from managetemplates.constants import PACKAGE_ROOT


def iter_files(root: Path):
    for entry in root.iterdir():
        if entry.name.startswith('.'):
            continue
        if entry.is_dir():
            yield from iter_files(entry)
        elif entry.is_file():
            yield entry


CLI_FILENAMES = frozenset(
    {
        'cli.py',
        'dev-cli.py',
        'manage.py',
        'manage_local_test.py',
    }
)


class CliFilesTestCase(TestCase):
    def test_cli_files_are_executable(self):
        found_file_names = set()
        for file_path in iter_files(PACKAGE_ROOT):
            file_name = file_path.name
            if file_name in CLI_FILENAMES:
                found_file_names.add(file_name)
                if not os.access(file_path, os.R_OK | os.X_OK):
                    file_path.chmod(0o775)  # rwxrwxr-x
            else:
                file_path.chmod(0o664)  # rw-rw-r--

        self.assertEqual(CLI_FILENAMES, found_file_names)
