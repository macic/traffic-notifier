import mock
from unittest import TestCase
from playhouse.test_utils import test_database
from peewee import *
from main import fill_inputs
from database.models import Input

test_db = SqliteDatabase(':memory:')


class TestInput(TestCase):
    def create_test_data(self):
        for i in range(10):
            Input.create(name='user-%d' % i, number=i)

    def test_create_test_data(self):
        with test_database(test_db, (Input,)):
            self.create_test_data()
            self.assertEqual(Input.select().count(), 10)

    @mock.patch('main.get_name', return_value='val')
    def test_fill_inputs(self, mocked):
        with test_database(test_db, (Input,)):
            fill_inputs(1)
            self.assertEqual(Input.select().count(), 1)
            self.assertIsNotNone(Input.get(Input.name=='val'))

    @mock.patch('main.get_name', return_value='')
    def test_input_with_empty_name_doesnt_get_saved(self, mocked):
        with test_database(test_db, (Input,)):
            fill_inputs(1)
            self.assertEqual(Input.select().count(), 0)
