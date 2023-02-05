import re
import shutil
from pathlib import Path

from bx_py_utils.path import assert_is_file
from manageprojects.git import Git
from manageprojects.utilities.temp_path import TemporaryDirectory


def filesystem_template_var_syntax(path: Path) -> int:
    print(f'Fix Cookiecutter variable name syntax in filesystem path: {path}')
    git = Git(cwd=path, detect_root=True)
    git_root_path = git.cwd
    rename_count = 0
    with TemporaryDirectory(prefix=f'{git_root_path.name}_') as temp_dir:
        # Collect information about file/directory renaming
        # copy all renamed files into TEMP

        rename_map = {}
        for path in git.ls_files(verbose=False):
            assert_is_file(path)

            origin_path_str = str(path)
            new_path_str = re.sub(r'{{(\S+?)}}', r'{{ \1 }}', origin_path_str)
            if new_path_str != origin_path_str:
                new_path = Path(new_path_str)
                rel_new_path = new_path.relative_to(git_root_path)
                print(path.relative_to(git_root_path), '->', rel_new_path)

                new_tmp_path = temp_dir / rel_new_path
                new_tmp_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, new_tmp_path)

                rename_map[path] = new_tmp_path

        # Replace all old files with renamed one, from TEMP:

        for old_path, tmp_path in rename_map.items():
            rel_tmp_path = tmp_path.relative_to(temp_dir)
            new_path = git_root_path / rel_tmp_path
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_path, new_path)
            old_path.unlink()
            try:
                old_path.parent.rmdir()
            except OSError:  # e.g.: [Errno 39] Directory not empty
                pass
            rename_count += 1

        if not rename_count:
            print('Nothing to rename, ok.')
        else:
            print(f'{rename_count} files/directories renamed')

        return rename_count
