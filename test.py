import base64
import unittest

from app import app
from models import User, Todo


class TodoTests(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        q = User.delete().where(User.username == "fred")
        q.execute()

    def test_home(self):
        """Test home page"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<body ng-app="todoListApp">', str(result.data))

    def test_create_user(self):
        """Create a test user and get token"""
        result = self.app.post('/api/v1/users',
                                data ={"username": "fred",
                                       "email": "fred@frog.com",
                                       "password": "fred",
                                       "verify_password": "fred"})
        self.assertEqual(result.status_code, 201)

        headers = {'Authorization': 'Basic ' + base64.b64encode(
                    bytes('fred' + ':' + 'fred', 'ascii')
                    ).decode('ascii')}
        result = self.app.get('/api/v1/users/token', headers=headers)
        self.assertEqual(result.status_code, 200)
        self.token = result.get_data(as_text=True)

    def test_create_bad_user(self):
        """Create a bad users"""
        result = self.app.post('/api/v1/users',
                                data ={"username": "fred",
                                       "email": "fred@frog.com",
                                       "password": "fred",
                                       "verify_password": "derf"})
        self.assertEqual(result.status_code, 400)

    def test_item(self):
        """Post, get, update & delete an item"""
        result = self.app.post('/api/v1/todos', data={'name': 'Test Name',
                                                      'edited': False,
                                                      'completed': False})
        self.assertEqual(result.status_code, 201)
        query = Todo.get(name='Test Name')

        # Item in main list
        result = self.app.get('/api/v1/todos')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test Name', str(result.data))

        # Get item
        result = self.app.get('/api/v1/todos/{}'.format(query.id))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test Name', str(result.data))

        # Edit Item
        result = self.app.put('/api/v1/todos/{}'.format(query.id),
                              data={'name': 'Test Name Changed',
                                    'edited': True,
                                    'completed': False})
        self.assertIn('/api/v1/todos/{}'.format(query.id),
                      result.headers['location'])
        query = Todo.get(name='Test Name Changed')

        #Delete Item
        result = self.app.delete('/api/v1/todos/{}'.format(query.id))
        self.assertEqual(result.status_code, 204)

if __name__ == '__main__':
    unittest.main()
