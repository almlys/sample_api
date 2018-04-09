import os
import main
import unittest
import json


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        main.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tmp.sqlite'
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
        main.db = main.SQLAlchemy(main.app)
        user = main.User('test')
        main.db.init_app(main.app)
        main.db.create_all()
        main.db.session.commit()

    def tearDown(self):
        os.unlink('/tmp/tmp.sqlite')

    def test_root(self):
        rv = self.app.get('/')
        assert b'<html' in rv.data

    def test_create(self):
        rv = self.app.post('/user', data={'id': 'unitest',
                                          'password': '123',
                                          'phone': '1234'})
        rvj = json.loads(str(rv.data))
        assert rvj.success


if __name__ == '__main__':
    unittest.main()
