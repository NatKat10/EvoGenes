import unittest
import json
from flask import current_app
from app import create_app


# to run the tests paste "python -m unittest discover -s tests" in the terminal

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def print_response(self, response):
        print("Response Status Code:", response.status_code)
        try:
            data = response.get_json()
            if data:
                print("Response Data Keys:", data.keys())
                # Print only part of the data for brevity
                for key in data.keys():
                    if isinstance(data[key], dict):
                        print(f"{key}: {{...}}")  # Indicate that it's a dictionary
                    elif isinstance(data[key], list):
                        print(f"{key}: [list with {len(data[key])} items]")  # Indicate the length of the list
                    else:
                        print(f"{key}: {data[key]}")
            else:
                print("No JSON response data.")
        except Exception as e:
            print(f"Error parsing response JSON: {e}")

    def test_run_evo_genes(self):#test checks if the /run-evo-genes route works correctly when provided with valid gene IDs and a sampling fraction.
        print("\nRunning test_run_evo_genes...")
        response = self.client.post('/run-evo-genes', data={
            'GeneID1': 'ENSMMUG00000002658',
            'GeneID2': 'ENSG00000069696',
            'samplingFraction': '0.1'
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('dotplot_plot', data)
        self.assertIn('gene_structure1_plot', data)
        self.assertIn('gene_structure2_plot', data)

    def test_plot_dotplot_route(self):# test checks if the /dash/dotplot/plot route works correctly when provided with valid dot plot data.
        print("\nRunning test_plot_dotplot_route...")
        response = self.client.post('/dash/dotplot/plot', json={
            'dotplot_data': {
                'directions': [],
                'min_x': 0,
                'max_x': 1000,
                'min_y': 0,
                'max_y': 1000,
                'x_label': 'Gene1',
                'y_label': 'Gene2'
            }
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertIn('layout', data)

    def test_plot_gene_structure(self):#test checks if the /dash/plot route works correctly when provided with valid exon positions
        print("\nRunning test_plot_gene_structure...")
        response = self.client.post('/dash/plot', json={
            'exonsPositions': [(100, 200), (300, 400)]
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertIn('layout', data)

    def test_update_dotplot_data(self):#test checks if the /dash/dotplot/update route works correctly when provided with valid dot plot data.
        print("\nRunning test_update_dotplot_data...")
        response = self.client.post('/dash/dotplot/update', json={
            'dotplot_data': {
                'directions': [],
                'min_x': 0,
                'max_x': 1000,
                'min_y': 0,
                'max_y': 1000,
                'x_label': 'Gene1',
                'y_label': 'Gene2'
            }
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_update_exon_positions(self):# test checks if the /dash/update route works correctly when provided with valid exon positions.
        print("\nRunning test_update_exon_positions...")
        response = self.client.post('/dash/update', json={
            'exonsPositions': [(100, 200), (300, 400)]
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_invalid_gene_ids(self):#test checks how the /run-evo-genes route handles invalid gene IDs.
        print("\nRunning test_invalid_gene_ids...")
        response = self.client.post('/run-evo-genes', data={
            'GeneID1': 'INVALID_ID1',
            'GeneID2': 'INVALID_ID2',
            'samplingFraction': '0.1'
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_missing_gene_ids(self):#test checks how the /run-evo-genes route handles missing gene IDs. It verifies that the response includes an error message and returns a 400 status code.
        print("\nRunning test_missing_gene_ids...")
        response = self.client.post('/run-evo-genes', data={
            'samplingFraction': '0.1'
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_relayout(self):#test checks if the /dash/relayout route works correctly when provided with valid relayout data. 
        print("\nRunning test_relayout...")
        response = self.client.post('/dash/relayout', json={
            'x0': 0,
            'x1': 1000,
            'y0': 0,
            'y1': 1000,
            'exon_intervals1': {'parent1': [(100, 200), (300, 400)]},
            'exon_intervals2': {'parent2': [(500, 600), (700, 800)]},
            'dotplot_data': {
                'layout': {
                    'x_label': 'Gene1',
                    'y_label': 'Gene2'
                }
            }
        })
        self.print_response(response)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('gene_structure1_plot', data)
        self.assertIn('gene_structure2_plot', data)
        self.assertIn('dotplot_plot', data)

if __name__ == '__main__':
    unittest.main()