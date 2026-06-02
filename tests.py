import os
import tempfile
import unittest

from app import app, db
from models import Expense, Budget


class ExpenseTrackerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix='.db')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{cls.db_path}'
        cls.client = app.test_client()

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
            db.engine.dispose()
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def test_home_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_expense_valid(self):
        response = self.client.post('/', data={
            'category': 'Food',
            'amount': '25.50',
            'description': 'Lunch',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            expense = Expense.query.first()
            self.assertIsNotNone(expense)
            self.assertEqual(expense.category, 'Food')
            self.assertAlmostEqual(expense.amount, 25.50)

    def test_add_expense_invalid_amount(self):
        response = self.client.post('/', data={
            'category': 'Food',
            'amount': 'abc',
            'description': 'Test',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Expense.query.count(), 0)

    def test_add_expense_negative_amount(self):
        response = self.client.post('/', data={
            'category': 'Food',
            'amount': '-50',
            'description': 'Test',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Expense.query.count(), 0)

    def test_delete_expense(self):
        with app.app_context():
            expense = Expense(category='Test', amount=10.0, description='')
            db.session.add(expense)
            db.session.commit()
            expense_id = expense.id

        response = self.client.post(
            f'/expenses/{expense_id}/delete',
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            result = db.session.get(Expense, expense_id)
            self.assertIsNone(result)

    def test_reports_loads(self):
        response = self.client.get('/reports')
        self.assertEqual(response.status_code, 200)

    def test_settings_loads(self):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)

    def test_set_budget(self):
        response = self.client.post('/settings', data={
            'budget_amount': '500',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            budget = Budget.query.first()
            self.assertIsNotNone(budget)
            self.assertAlmostEqual(budget.amount, 500.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
