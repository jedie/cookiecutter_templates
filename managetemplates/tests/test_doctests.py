from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import managetemplates


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(managetemplates,),
        )
