import unittest
import json

from math_project import create_app
from exts import db


class TestAPP(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # AdminView.py
    def add_staff(self, username, pwd, email):
        params = {"user_name": username,
                  "pwd": pwd,
                  "email": email}
        return self.client.post('/admin/addstaff', data=params, follow_redirects=True)

    def test_add_staff(self):
        ret = self.add_staff('testaddstaff', 'testaddstaff', 'testaddstaff@')
        return self.assertIsNotNone(json.loads(ret.data)['users_list'])


if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [TestAPP('test_add_staff')]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
