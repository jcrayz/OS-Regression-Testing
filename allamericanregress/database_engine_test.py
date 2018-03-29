import unittest
import os
from allamericanregress import database_engine
from allamericanregress import testing_framework_test


class TestDatabaseEngine (unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Delete all the programs in the database
        for registrant in database_engine.all_registrants():
            database_engine.deregister_program(registrant.id)

    def test_empty_name_registered(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('', 'C:\\temp\\path', 'fake execution $1', 'Blake')

    def test_empty_path_registerd(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('Fake Program', '', 'Fake Exe $1', 'Blake')

    def test_empty_command_registered(self):
        with self.assertRaises(ValueError):
            database_engine.register_program('Fake Program', 'C:\\fake\\path.exe', '')

    def test_get_current_results_returns_nothing_with_no_executed_tests(self):
        self.assertTrue(len(database_engine.get_current_results()) == 0)

    def test_execution_when_registered(self):
        # Register a program
        passing = testing_framework_test.TestTestingFramework.pass_test
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])

        # Check that the program executed
        results = database_engine.get_current_results()
        if len(results) == 0:
            self.fail('Results should contain something')
        for test in results:
            self.assertTrue(test[0].name == passing[0])
            self.assertTrue(test[1].last_execution_id is test[1].last_successful_execution_id)

        # Delete the registrant
        database_engine.deregister_program(1)

if __name__ == '__main__':
    unittest.main()