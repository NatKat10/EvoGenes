import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import Gene
import warnings
import io

class RoutesTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_blueprint_is_working(self):
        print("\nRunning test_blueprint_is_working")
        response = self.client.get('/generate/test')
        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")
        print("Blueprint is working.")

    def test_get_data(self):
        print("\nRunning test_get_data")
        response = self.client.get('/')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")
        try:
            response_json = response.get_json()
            print(f"Response JSON: {response_json}")
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            response_json = None
        
        self.assertEqual(response.status_code, 200, f"Expected response code 200 but got {response.status_code}")
        self.assertEqual(response_json, {"Hello": "World"}, f"Expected response JSON {{'Hello': 'World'}} but got {response_json}")

    def test_add_gene(self):
        print("\nRunning test_add_gene")
        data = {
            'gene_name': 'BRCA1',
            'sequence': 'ATCG'
        }
        response = self.client.post('/add', json=data)
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")
        self.assertEqual(response.status_code, 201, f"Expected response code 201 but got {response.status_code}")
        self.assertIn('gene_id', response.get_json(), "Response JSON does not contain 'gene_id'")
        print("Gene added successfully.")

    def test_get_genes(self):
        print("\nRunning test_get_genes")
        self.test_add_gene()  # Add a gene first
        response = self.client.get('/genes')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")
        self.assertEqual(response.status_code, 200, f"Expected response code 200 but got {response.status_code}")
        genes = response.get_json()
        print(f"Response JSON: {genes}")
        self.assertIsInstance(genes, list, "Expected a list of genes")

    def test_run_yass(self):
        print("\nRunning test_run_yass")
        # Simulate file upload for the /run-yass endpoint
        data = {
            'fasta1': (io.BytesIO(b'>sequence1\nATCGATCGATCG\n'), 'temp_sequence1.fasta'),
            'fasta2': (io.BytesIO(b'>sequence2\nCGATCGATCGAT\n'), 'temp_sequence2.fasta')
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            response = self.client.post('/run-yass', content_type='multipart/form-data', data=data)
            print(f"Response status code: {response.status_code}")
            self.assertEqual(response.status_code, 200, f"Expected response code 200 but got {response.status_code}")
            print("YASS algorithm executed successfully.")

if __name__ == '__main__':
    unittest.main()
