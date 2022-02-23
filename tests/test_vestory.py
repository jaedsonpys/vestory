import os
import sys

sys.path.insert(0, './')

import vestory
from pyseqtest import SeqTest

# The test should run in the root directory,
# for example:
# 
# python3 tests/test_vestory.py
# 
# A "test_files" directory must be created
# in /tests for the correct execution of
# the tests.#


class TestVestory(SeqTest):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.files = os.listdir('test_files')

    def test_init_repo(self):
        vestory.init_repo()

        # verify
        self.is_true(os.path.isdir('./.vestory'), 'Repo is not created')
        self.is_true(os.path.isdir('./.vestory/changes'), 'Diretory "changes" not found')
        self.is_true(os.path.isfile('./.vestory/vestory.config.json'), 'Config file not found')


if __name__ == '__main__':
    TestVestory().run()
