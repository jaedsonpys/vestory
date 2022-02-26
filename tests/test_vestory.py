import json
import os
import sys

sys.path.insert(0, './')

from hashlib import md5
from shutil import rmtree

import vestory
from pyseqtest import SeqTest

# The test should run in the root directory,
# for example:
# 
# python3 tests/test_vestory.py


class TestVestory(SeqTest):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.files = []

        # delete .vestory dir
        if os.path.isdir('./.vestory'):
            rmtree('./.vestory')

        if os.path.isdir('./tests/test_files'):
            rmtree('./tests/test_files')

        os.mkdir('tests/test_files')

        # create tests files
        for i in range(10):
            with open(f'./tests/test_files/file-{i}', 'w') as file_w:
                file_w.write('Welcome to my file!\n')
                self.files.append(f'./tests/test_files/file-{i}')

    def test_init_repo(self):
        vestory.init_repo('Jaedson', 'test@mail.com')

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

    def test_submit(self):
        vestory.submit_change(self.files, 'first submit')

        self.check_any_value(
            len(os.listdir('./.vestory/changes/')),
            len(self.files),
            msg_error='Changes not found'
        )

    def test_change_file(self):
        for file in self.files:
            with open(file, 'a') as file_u:
                file_u.write('More lines here!')

    def test_check_file_has_changed(self):
        for file in self.files:
            self.is_true(vestory.check_file_has_changed(file), 'Change not detected')

    def test_submit_change(self):
        vestory.submit_change(self.files, 'add more lines')

        for file_history in os.listdir('./.vestory/changes'):
            with open(os.path.join('./.vestory/changes', file_history)) as file_r:
                lines_count = len(file_r.readlines())
        
            self.check_any_value(lines_count, 2, msg_error='Unrealized change')

    def test_check_file_has_changed_2(self):
        for file in self.files:
            self.is_false(vestory.check_file_has_changed(file), 'Change detected')

    def test_count_changes(self):
        file_id = md5(self.files[0].encode()).hexdigest()

        file_changes = vestory.get_changes(file_id)
        self.is_true(len(file_changes) == 2, 'Number of incorrect changes')

    def test_join_changes(self):
        file_id = md5(self.files[0].encode()).hexdigest()
        file_changes = vestory.get_changes(file_id)

        joined_changes = vestory.join_changes(file_changes)
        self.is_true(
            {'0': 'Welcome to my file!\n', '1': 'More lines here!'} == joined_changes,
            msg_error='Incorrect change join'
        )


if __name__ == '__main__':
    TestVestory().run()
