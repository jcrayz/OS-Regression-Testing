import unittest
from allamericanregress import database_engine


class TestDatabaseEngine (unittest.TestCase):

    def test_empty_name_registered(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('', 'C:\\temp\\path', 'fake execution $1', 'Blake')

    def test_empty_path_registerd(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('Fake Program', '', 'Fake Exe $1', 'Blake')

    def test_empty_command_registered(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('Fake Program', 'C:\\fake\\path.exe', '')

if __name__ == '__main__':
    unittest.main()