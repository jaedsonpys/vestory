import json
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
        self.files = os.listdir('./tests/test_files')

    def test_init_repo(self):
        vestory.init_repo()

        # verify
        self.is_true(os.path.isdir('./.vestory'), 'Repo is not created')
        self.is_true(os.path.isdir('./.vestory/changes'), 'Diretory "changes" not found')
        self.is_true(os.path.isfile('./.vestory/vestory.config.json'), 'Config file not found')

    def test_add_files(self):
        vestory.add_files(self.files)

        # verify
        with open('./.vestory/vestory.config.json', 'r') as config:
            vestory_config: dict = json.load(config)

        tracked_files = len(vestory_config['tracking_files'])
        self.check_any_value(tracked_files, len(self.files), 'File not added')


if __name__ == '__main__':
    TestVestory().run()
