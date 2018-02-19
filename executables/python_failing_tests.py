import unittest


class PerformPassingTests(unittest.TestCase):
    def test1(self):
        self.assertNotEqual(True, True)

    def test2(self):
        self.assertNotEqual('lol', 'lol')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
