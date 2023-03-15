import unittest
from flask import url_for
from flask_testing import TestCase
from app.models import User, Task

from app import app, db

class TestBase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#routes tests
class TestRoutes(TestBase):

    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to the login page

    def test_login(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)

    def test_kanban_not_logged_in(self):
        response = self.client.get(url_for('kanban'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to the login page


#logged-in user required tests
class TestLoggedInRoutes(TestBase):

    def login(self, username, password):
        return self.client.post(
            url_for('login'),
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_test_user(self):
        user = User(username="testuser", password="testpassword")
        db.session.add(user)
        db.session.commit()

    def setUp(self):
        super().setUp()
        self.create_test_user()
        self.login('testuser', 'testpassword')

    def test_kanban_logged_in(self):
        response = self.client.get(url_for('kanban'))
        self.assertEqual(response.status_code, 200)

class TestTaskOperations(TestLoggedInRoutes):

    def create_test_task(self, description='Test Task', status='todo'):
        task = Task(description=description, status=status, user_id=1)
        db.session.add(task)
        db.session.commit()

    def test_create_task(self):
        response = self.client.post(
            url_for('kanban'),
            data=dict(description='New Task', status='todo'),
            follow_redirects=True
        )
        self.assertIn(b'New Task', response.data)

    def test_create_duplicate_task(self):
        self.create_test_task()
        response = self.client.post(
            url_for('kanban'),
            data=dict(description='Test Task', status='todo'),
            follow_redirects=True
        )
        self.assertIn(b'This is on the board! Try something else.', response.data)

    def test_update_task(self):
        self.create_test_task()
        response = self.client.post(
            url_for('update'),
            data=dict(name='Test Task', newstatus='progress'),
            follow_redirects=True
        )
        self.assertIn(b'progress', response.data)

    def test_delete_task(self):
        self.create_test_task()
        response = self.client.post(
            url_for('delete'),
            data=dict(description='Test Task'),
            follow_redirects=True
        )
        self.assertNotIn(b'Test Task', response.data)

    def test_delete_nonexistent_task(self):
        response = self.client.post(
            url_for('delete'),
            data=dict(description='Nonexistent Task'),
            follow_redirects=True
        )
        self.assertNotIn(b'Nonexistent Task', response.data)



if __name__ == '__main__':
    unittest.main()
