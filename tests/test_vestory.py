import json
import os
import sys

sys.path.insert(0, './')

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

        # create file to ignore
        with open('./tests/test_files/iamignored', 'w') as file_w:
            file_w.write('Ignore my existence...')

        # create .ignoreme
        with open('./tests/test_files/.ignoreme', 'w') as file_w:
            file_w.write('./tests/test_files/iamignored\n')

    def test_init_repo(self):
        vestory.init_repo('Jaedson', 'test@mail.com')
        self.is_true(os.path.isdir('./.vestory'), 'Repo is not created')
        self.is_true(os.path.isfile('./.vestory/vestory.json'), 'Vestory file not found')

    def test_get_repo_key(self):
        key = vestory.get_repo_key()
        self.is_true(len(key) == 32, msg_error='Invalid repo key')

    def test_get_author(self):
        author, author_email = vestory.get_author_info()
        self.is_true(author == 'Jaedson', 'Author incorrect')
        self.is_true(author_email == 'test@mail.com', 'Author email incorrect')

    def test_add_files(self):
        vestory.add_files(self.files)
        with open('./.vestory/vestory.json', 'r') as config:
            vestory_config: dict = json.load(config)

        tracked_files = len(vestory_config['tracking_files'])
        self.check_any_value(tracked_files, len(self.files), 'File not added')

    def test_submit(self):
        self.change_id = vestory.submit_change(self.files, 'first submit')
        change_info = vestory.get_change_info_by_id(self.change_id)
        self.is_true(isinstance(change_info, dict), msg_error='Change info not found')

    def test_change_file(self):
        for file in self.files:
            with open(file, 'a') as file_u:
                file_u.write('More lines here!')

    def test_check_diff(self):
        file_changes = vestory.get_file_changes(self.files[0])
        joined_changes = vestory.join_file_changes(file_changes)

        change = {'1': 'Change', '2': 'Test diff'}
        diff = vestory.check_diff(joined_changes, change)
        self.is_true(change == diff, msg_error='Incorrect difference')

    def test_check_file_has_changed(self):
        for file in self.files:
            self.is_true(vestory.check_file_has_changed(file), 'Change not detected')

    def test_get_files_changed(self):
        changed_files = vestory.get_files_changed()
        self.is_true(len(changed_files) == 10, 'Error getting files changed')

    def test_submit_change(self):
        change_id = vestory.submit_change(self.files, 'add more lines')
        change_info = vestory.get_change_info_by_id(change_id)
        changed_files = list(change_info['changed_files'].keys())

        self.is_true(isinstance(change_info, dict), msg_error='Change not found')        
        self.is_true(len(changed_files) == len(self.files), msg_error='Some files were not found')

    def test_check_file_has_changed_2(self):
        for file in self.files:
            self.is_false(vestory.check_file_has_changed(file), 'Change detected')

    def test_count_changes(self):
        changes = vestory.get_changes()
        len_changes = len(changes.keys())
        self.is_true(len_changes == 2, msg_error='Number of incorrect changes')

    def test_join_file_changes(self):
        file_changes = vestory.get_file_changes(self.files[0])
        joined_changes = vestory.join_file_changes(file_changes)

        self.is_true(
            {'0': 'Welcome to my file!\n', '1': 'More lines here!'} == joined_changes,
            msg_error='Incorrect change join'
        )

    def test_join_changes(self):
        joined_changes = vestory.join_changes()
        first_file = joined_changes[self.files[0]]

        self.is_true(
            {'0': 'Welcome to my file!\n', '1': 'More lines here!'} == first_file,
            msg_error='Incorrect change join'
        )

    def test_get_changes_by_author(self):
        author_changes = vestory.get_changes_by_author('test@mail.com')
        self.is_true(len(author_changes) == 2, msg_error='Author changes incorrect')

    def test_invalidating_change(self):
        with open('./.vestory/vestory.json') as file_r:
            vestory_file = json.load(file_r)

        vestory_file['changes'][self.change_id] = 'eyJhdXRob3JfZW1haWwiOiAidGVzdEBtYWlsLmNvbSJ9.82dad4de27db35733865b972745659f1'
        with open('./.vestory/vestory.json', 'w') as file_w:
            json.dump(vestory_file, file_w, ensure_ascii=False)

    def test_get_changes_by_author_2(self):
        try:
            vestory.get_changes_by_author('test@mail.com')
        except vestory.InvalidChangeError:
            self.is_true(True)
        else:
            self.is_true(False, msg_error='Invalid change not detected')

if __name__ == '__main__':
    TestVestory().run()
