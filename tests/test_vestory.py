import os
import sys

sys.path.insert(0, './')

import vestory
from pyseqtest import SeqTest


class TestVestory(SeqTest):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    TestVestory().run()
