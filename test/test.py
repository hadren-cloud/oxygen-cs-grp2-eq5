import unittest
import os
from src.main import Main

class test(unittest.TestCase):
    def setUp(self):
        # Set up environment variables for testing
        os.environ['HOST'] = 'test_host'
        os.environ['TICKETS'] = 'test_tickets'
        os.environ['T_MAX'] = 'test_max_temp'
        os.environ['T_MIN'] = 'test_min_temp'
        os.environ['DATABASE'] = 'test_database'
        
    def test_token_not_set(self):
        if 'TOKEN' in os.environ:
            del os.environ['TOKEN']
        with self.assertRaises(ValueError):
            Main()

    def test_token_set(self):
        os.environ['TOKEN'] = 'test_token'
        main = Main()
        self.assertEqual(main.TOKEN, 'test_token')

    def tearDown(self):
        if 'TOKEN' in os.environ:
            del os.environ['TOKEN']

if __name__ == '__main__':
    unittest.main()
