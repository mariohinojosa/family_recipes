import unittest
from project import app


class ProjectTests(unittest.TestCase):
    """This class will include functions to setUp() and tearDown() each unit test.
    The setUp() function should specify the key configuration items
    needed for the unit test case.
    The tearDown() function will not
    do anything to start off"""
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Mario\'s Recipes', response.data)
        self.assertIn(b'Breakfast Recipes', response.data)
        self.assertIn(b'Lunch Recipes', response.data)
        self.assertIn(b'Dinner Recipes', response.data)
        self.assertIn(b'Dessert Recipes', response.data)


if __name__ == '__main__':
    unittest.main()
