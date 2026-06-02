"""
Unit tests for Reading Notes Management API
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'flask'))

from main import app, notes_db


class TestNotesAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        notes_db.clear()

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertIn('timestamp', data)

    def test_add_note(self):
        note_data = {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'genre': 'Fiction',
            'rating': 5,
            'notes': 'A masterpiece of American literature.'
        }
        response = self.app.post('/notes', data=json.dumps(note_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['status'], 'created')

    def test_add_note_missing_field(self):
        note_data = {'title': 'Test Book', 'author': 'Test Author'}
        response = self.app.post('/notes', data=json.dumps(note_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_note_invalid_rating(self):
        note_data = {
            'title': 'Test', 'author': 'Author', 'genre': 'Fiction',
            'rating': 6, 'notes': 'Test notes'
        }
        response = self.app.post('/notes', data=json.dumps(note_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_note_invalid_genre(self):
        note_data = {
            'title': 'Test', 'author': 'Author', 'genre': 'InvalidGenre',
            'rating': 3, 'notes': 'Test notes'
        }
        response = self.app.post('/notes', data=json.dumps(note_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_notes(self):
        self._add_sample_note()
        response = self.app.get('/notes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_note_by_id(self):
        note_id = self._add_sample_note()
        response = self.app.get(f'/notes/{note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'The Great Gatsby')

    def test_get_note_not_found(self):
        response = self.app.get('/notes/non-existent-id')
        self.assertEqual(response.status_code, 404)

    def test_filter_notes_by_genre(self):
        self._add_sample_note(genre='Fiction')
        self._add_sample_note(title='Sapiens', author='Yuval Harari', genre='Non-Fiction')

        response = self.app.get('/notes?genre=Fiction')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['genre'], 'Fiction')

    def test_update_note(self):
        note_id = self._add_sample_note()
        update_data = {'rating': 3, 'reading_status': 'reading'}
        response = self.app.patch(f'/notes/{note_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['rating'], 3)
        self.assertEqual(data['reading_status'], 'reading')

    def test_delete_note(self):
        note_id = self._add_sample_note()
        response = self.app.delete(f'/notes/{note_id}')
        self.assertEqual(response.status_code, 200)
        # Verify deleted
        response = self.app.get('/notes')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_add_quote(self):
        note_id = self._add_sample_note()
        quote_data = {'quote': 'So we beat on, boats against the current.', 'page': 180}
        response = self.app.post(f'/notes/{note_id}/quotes', data=json.dumps(quote_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['quotes']), 1)
        self.assertEqual(data['quotes'][0]['quote'], 'So we beat on, boats against the current.')

    def test_get_stats(self):
        self._add_sample_note(rating=5)
        self._add_sample_note(title='Sapiens', author='Yuval Harari', genre='Non-Fiction', rating=4)

        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_books'], 2)
        self.assertEqual(data['average_rating'], 4.5)

    def test_search_notes(self):
        self._add_sample_note()
        self._add_sample_note(title='Sapiens', author='Yuval Harari', genre='Non-Fiction')

        response = self.app.get('/search?q=gatsby')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_genres(self):
        response = self.app.get('/genres')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Fiction', data['genres'])
        self.assertIn('Non-Fiction', data['genres'])

    # Helper
    def _add_sample_note(self, title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Fiction', rating=5):
        note_data = {
            'title': title, 'author': author, 'genre': genre,
            'rating': rating, 'notes': 'A great book about the American Dream.'
        }
        response = self.app.post('/notes', data=json.dumps(note_data), content_type='application/json')
        data = json.loads(response.data)
        return data['id']


if __name__ == '__main__':
    unittest.main()