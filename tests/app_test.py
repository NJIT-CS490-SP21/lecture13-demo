import unittest
import unittest.mock as mock
from unittest.mock import patch, MagicMock, Mock
import os
import sys

sys.path.append(os.path.abspath('../'))
from app import add_user
import models

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

INITIAL_USERNAME = 'user1'

class AddUserTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 'naman',
                KEY_EXPECTED: ['user1', 'naman'],
            },
        ]
        
        initial_person = models.Person(username=INITIAL_USERNAME, email='{0}@stuff.com'.format(INITIAL_USERNAME))
        self.initial_db_list = [initial_person]
    
    def db_session_add_mock(self, person):
        print('add')
        self.initial_db_list.append(person)
    
    def db_session_commit_mock(self):
        print('sessioncommit')
        pass
    
    def models_person_query(self):
        print('in here')
        return self.initial_db_list
        
    def test_success(self):
        for test in self.success_test_params:
            with patch('app.db.session.add', self.db_session_add_mock):
                with patch('app.db.session.commit', self.db_session_commit_mock):
                    with patch('models.Person.query.all', self.models_person_query):
                        actual_result = add_user(test[KEY_INPUT])
                        expected_result = test[KEY_EXPECTED]
                        print(actual_result)
                        print(expected_result)
                        print(self.initial_db_list)
                        
                        self.assertEqual(len(actual_result), len(expected_result))
                        self.assertEqual(actual_result[1], expected_result[1])


if __name__ == '__main__':
    unittest.main()