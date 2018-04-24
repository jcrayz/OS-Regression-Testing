import unittest
import os
from allamericanregress import testing_framework
from allamericanregress import database_engine
from allamericanregress import models


class TestTestingFramework (unittest.TestCase):
    root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
    fail_test = ['JAR Fail', '{}\executables\Prototype_Tests_Fail.jar'.format(root), 'java -jar $1', 'Blake']
    pass_test = ['JAR Pass', '{}\executables\Prototype_Tests_Pass.jar'.format(root), 'java -jar $1', 'Blake']

    @classmethod
    def setUpClass(self):
        # Delete all the programs in the database
        for registrant in database_engine.all_registrants():
            database_engine.deregister_program(registrant.id)

    def tearDown(self):
        # Delete all the registrants after each testss
        for registrant in database_engine.all_registrants():
            database_engine.deregister_program(registrant.id)

    def test_failing_test_fails(self):
        # Register a testss that will fail
        test = TestTestingFramework.fail_test
        database_engine.register_program(test[0], test[1], test[2], test[3])

        # Execute the testss
        testing_framework.execute_tests()

        # Confirm that the testss fails by checking failure records
        self.assertTrue(database_engine.get_failure_registrants().__contains__(database_engine.get_registrant(1)))

    def test_passing_test_passes(self):
        # Register a testss that will pass
        test = TestTestingFramework.pass_test
        database_engine.register_program(test[0], test[1], test[2], test[3])

        # Execute the testss
        testing_framework.execute_tests()

        # Confirm that the testss passes by checking failure records
        registrants = []
        for tests in database_engine.get_current_results():
            registrants.append(tests[0])
        self.assertTrue(registrants.__contains__(database_engine.get_registrant(1)))
        self.assertFalse(database_engine.get_failure_registrants().__contains__(database_engine.get_registrant(1)))

    def test_multiple_tests(self):
        # Register multiple tests
        failure = TestTestingFramework.fail_test
        passing = TestTestingFramework.pass_test
        database_engine.register_program(failure[0], failure[1], failure[2], failure[3])
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])
        database_engine.register_program(failure[0], failure[1], failure[2], failure[3])

        # Execute all tests
        testing_framework.execute_tests()

        # Get expected results
        results = database_engine.get_current_results()
        if len(results) == 0:
            self.fail('Results should contain something')
        for test in results:
            if test[0].name == passing[0]:
                self.assertTrue(test[1].last_execution_id is test[1].last_successful_execution_id)
            else:
                self.assertTrue(test[1].last_execution_id is not test[1].last_successful_execution_id)

    def test_individual_test(self):
        # Register Multiple tests
        failure = TestTestingFramework.fail_test
        passing = TestTestingFramework.pass_test
        database_engine.register_program(failure[0], failure[1], failure[2], failure[3])
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])

        # Execute only the passing test
        testing_framework.execute_individual_test(2)

        # Expect that only the passing test executed
        results = database_engine.get_current_results()
        if len(results) == 0:
            self.fail('Results should contain something')
        with database_engine.connect() as session:
            exec_rec = session.query(models.ExecutionRecord).order_by(
                models.ExecutionRecord.timestamp.desc())[0]
            for test in results:
                if test[1].last_execution_id == exec_rec.id:
                    self.assertTrue(test[0].name == passing[0])
                elif test[0].name == passing[0]:
                    self.fail('The passing record should be the most recent execution')

    def test_execute_failed_tests(self):
        # Register multiple tests
        failure = TestTestingFramework.fail_test
        passing = TestTestingFramework.pass_test
        database_engine.register_program(failure[0], failure[1], failure[2], failure[3])
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])
        database_engine.register_program(passing[0], passing[1], passing[2], passing[3])
        database_engine.register_program(failure[0], failure[1], failure[2], failure[3])

        # Execute all tests to get the ones that have failed
        testing_framework.execute_tests()

        # Execute only the failed tests
        testing_framework.execute_failed_tests()

        results = database_engine.get_current_results()
        if len(results) == 0:
            self.fail('Results should contain something')
        with database_engine.connect() as session:
            exec_rec = session.query(models.ExecutionRecord).order_by(
                models.ExecutionRecord.timestamp.desc())[0]
            for test in results:
                if test[0].name == passing[0]:
                    self.assertFalse(test[1].last_execution_id == exec_rec.id)
                else:
                    self.assertTrue(test[1].last_execution_id == exec_rec.id)



if __name__ == '__main__':
    unittest.main()