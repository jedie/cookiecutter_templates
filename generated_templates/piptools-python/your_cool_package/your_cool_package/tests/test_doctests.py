from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import your_cool_package


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(your_cool_package,),
        )
