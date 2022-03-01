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
        self.is_true(os.path.isfile('./.vestory/vestory.config.json'), 'Config file not found')

    def test_get_author(self):
        author, author_email = vestory.get_author_info()
        self.is_true(author == 'Jaedson', 'Author incorrect')
        self.is_true(author_email == 'test@mail.com', 'Author email incorrect')

    def test_add_files(self):
        vestory.add_files(self.files)

        # verify
        with open('./.vestory/vestory.config.json', 'r') as config:
            vestory_config: dict = json.load(config)

        tracked_files = len(vestory_config['tracking_files'])
        self.check_any_value(tracked_files, len(self.files), 'File not added')

    def test_submit(self):
        change_id = vestory.submit_change(self.files, 'first submit')
        change_info = vestory.get_change_info_by_id(change_id)
        self.is_true(isinstance(change_info, dict), msg_error='Change info not found')

    def test_change_file(self):
        for file in self.files:
            with open(file, 'a') as file_u:
                file_u.write('More lines here!')

    def test_check_file_has_changed(self):
        for file in self.files:
            self.is_true(vestory.check_file_has_changed(file), 'Change not detected')

    def test_get_files_changed(self):
        changed_files = vestory.get_files_changed()
        self.is_true(len(changed_files) == 10, 'Error getting files changed')

    def test_submit_change(self):
        vestory.submit_change(self.files, 'add more lines')

        for file_history in os.listdir('./.vestory/changes'):
            with open(os.path.join('./.vestory/changes', file_history)) as file_r:
                lines_count = len(file_r.readlines())
        
            self.check_any_value(lines_count, 2, msg_error='Unrealized change')

    def test_get_filepath_by_id(self):
        file_id = md5(self.files[0].encode()).hexdigest()
        filepath = vestory.get_filepath_by_id(file_id)
        self.is_true(filepath == self.files[0], 'Incorrect file path')

    def test_check_file_has_changed_2(self):
        for file in self.files:
            self.is_false(vestory.check_file_has_changed(file), 'Change detected')

    def test_count_changes(self):
        file_id = md5(self.files[0].encode()).hexdigest()

        file_changes = vestory.get_file_changes(file_id)
        self.is_true(len(file_changes) == 2, 'Number of incorrect changes')

    def test_join_file_changes(self):
        file_id = md5(self.files[0].encode()).hexdigest()
        file_changes = vestory.get_file_changes(file_id)

        joined_changes = vestory.join_file_changes(file_changes)
        self.is_true(
            {'0': 'Welcome to my file!\n', '1': 'More lines here!'} == joined_changes,
            msg_error='Incorrect change join'
        )

    def test_join_changes(self):
        joined_changes = vestory.join_changes()
        filepath = list(joined_changes.keys())[0]
        first_file = joined_changes[filepath]

        self.is_true(
            {'0': 'Welcome to my file!\n', '1': 'More lines here!'} == first_file,
            msg_error='Incorrect change join'
        )

    def test_get_all_changes(self):
        changes = vestory.get_all_changes()
        self.is_true(len(changes.keys()) == 10, 'Some changes are missing')


if __name__ == '__main__':
    TestVestory().run()
