from unittest import TestCase, skipIf

from cli_base.cli_tools.constants import GITHUB_ACTION
from cli_base.cli_tools.git_history import update_readme_history

from managetemplates.cli_dev import PACKAGE_ROOT


class ReadmeHistoryTestCase(TestCase):
    @skipIf(
        # After a release the history may be "changed" because of version bump.
        # We should not block merge requests because of this.
        GITHUB_ACTION,
        reason='Skip on github actions',
    )
    def test_readme_history(self):
        update_readme_history(base_path=PACKAGE_ROOT, raise_update_error=True)
