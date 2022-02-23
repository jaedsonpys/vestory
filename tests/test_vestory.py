import os
import sys

sys.path.insert(0, './')

import vestory
from pyseqtest import SeqTest


class TestVestory(SeqTest):
    def __init__(self):
        super().__init__()

    def test_init_repo(self):
        vestory.init_repo()

        # verify
        self.is_true(os.path.isdir('./.vestory'), 'Repo is not created')
        self.is_true(os.path.isdir('./.vestory/changes'), 'Diretory "changes" not found')
        self.is_true(os.path.isfile('./.vestory/vestory.config.json'), 'Config file not found')


if __name__ == '__main__':
    TestVestory().run()
