import unittest


class PerformPassingTests(unittest.TestCase):
    def test1(self):
        self.assertEqual(True, True)

    def test2(self):
        self.assertEqual('lol', 'lol')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
