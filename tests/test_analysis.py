import unittest
import numpy as np
import copy
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.analysis_influence import create_pagerank_matrix, is_recursive, remove_cycles, create_data_set_specific_pg_matrices

"""
Most of these are sanity checks
"""

class PageRank(unittest.TestCase):

    # @unittest.skip('')
    def test_create_pagerank_matrix1(self):
        headers = ['Cleaned Name', '1', '2', '3', '4']
        the_hashmap = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        cs = {'jargon_entry_positions': [1,2,3,4], 'clean_name_pos': 0}
        the_matrix = np.array([
            ['A', 'D',  '',  '', ''],
            ['B', 'D', 'E',  '', ''],
            ['C', 'E',  '',  '', ''],
            ['D', 'F',  '',  '', ''],
            ['E', 'F', 'G', 'H', ''],
            ['F',  '',  '',  '', ''],
            ['G',  '',  '',  '', ''],
            ['H',  '',  '',  '', ''], 
        ])

        final_matrix = np.zeros((8,8))
        
        final_matrix[0][3] = 1
        final_matrix[1][3] = 0.5
        final_matrix[1][4] = 0.5
        final_matrix[2][4] = 1
        final_matrix[3][5] = 1
        final_matrix[4][5] = 0.3333333333333333
        final_matrix[4][6] = 0.3333333333333333
        final_matrix[4][7] = 0.3333333333333333
        final_matrix = np.round(np.array(final_matrix).T, 2)
        
        
        
        pg_matrix, edges_removed = create_pagerank_matrix(the_matrix, the_hashmap, cs)

        self.assertEqual(np.array_equal(final_matrix, np.round(pg_matrix, 2)), True)

        
    # @unittest.skip('')
    def test_create_pagerank_matrix1_recursion_removal(self):
        headers = ['Cleaned Name', '1', '2', '3', '4']
        the_hashmap = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        cs = {'jargon_entry_positions': [1,2,3,4], 'clean_name_pos': 0}
        the_matrix = np.array([
            ['A', 'A',  '',  '', ''], # 1-recursion
            ['B', 'D',  '',  '', ''], # 3-recursion
            ['C', 'E',  '',  '', ''],
            ['D', 'H',  '',  '', ''], # 3-recursion
            ['E', 'F', 'G', 'H', ''],
            ['F',  '',  '',  '', ''],
            ['G',  '',  '',  '', ''],
            ['H',  '', 'B',  '', ''],  # 3-recursion
        ])

        final_matrix = np.zeros((8,8))
        
        final_matrix[1][3] = 1
        final_matrix[2][4] = 1
        final_matrix[3][7] = 1
        final_matrix[4][5] = 0.3333333333333333
        final_matrix[4][6] = 0.3333333333333333
        final_matrix[4][7] = 0.3333333333333333

        final_matrix = np.array(final_matrix).T
        
        pg_matrix, edges_removed = create_pagerank_matrix(the_matrix, the_hashmap, cs)
         
        for i in range(0, len(final_matrix)):
            for j in range(0, len(final_matrix)):
                self.assertEqual(final_matrix[i][j], pg_matrix[i][j])
        
        
    # @unittest.skip('')
    def test_is_recursive(self):
        
        jargon_poss = [1,2,3]
        the_hm = {"test1": 0, "test2": 1, "test3": 2}
        matrix = [
            ["test1", "test1", 0, 0], 
            ["test2", 0, 0, 0], 
            ["test3", 0, 0, 0],
        ]
        
        edge = is_recursive(matrix, 0, jargon_poss, the_hm, "test1")
        self.assertEqual(edge[0], 0)
        self.assertEqual(edge[1], 1)
    
    # @unittest.skip('')
    def test_remove_cycles1(self):
        cs = {'jargon_entry_positions': [1,2,3], "clean_name_pos": 0}
        the_hm = {"test1": 0, "test2": 1, "test3": 2}
        matrix = [
            ["test1", "test1", "", ""], 
            ["test2", "",      "", ""], 
            ["test3", "",      "", ""],
        ]
        
        remove_cycles(matrix, the_hm, cs)
        
        self.assertEqual(matrix[0][1], "")
        self.assertEqual(matrix[0][2], "")
        self.assertEqual(matrix[0][3], "")
        
        self.assertEqual(matrix[1][1], "")
        self.assertEqual(matrix[1][2], "")
        self.assertEqual(matrix[1][3], "")
        
        self.assertEqual(matrix[2][1], "")
        self.assertEqual(matrix[2][2], "")
        self.assertEqual(matrix[2][3], "")
    
    # @unittest.skip('')
    def test_remove_cycles2(self):
        cs = {'jargon_entry_positions': [1,2,3], "clean_name_pos": 0}
        the_hm = {"test1": 0, "test2": 1, "test3": 2}
        matrix = [
            ["test1", "test2", "",      ""], 
            ["test2", "",      "",      "test3"], 
            ["test3", "",      "test1", ""],
        ]
        
        edges_removed = remove_cycles(matrix, the_hm, cs)
        
        self.assertEqual(matrix[0][1], "test2")
        self.assertEqual(matrix[0][2], "")
        self.assertEqual(matrix[0][3], "")
        
        self.assertEqual(matrix[1][1], "")
        self.assertEqual(matrix[1][2], "")
        self.assertEqual(matrix[1][3], "test3")
        
        self.assertEqual(matrix[2][1], "")
        self.assertEqual(matrix[2][2], "")
        self.assertEqual(matrix[2][3], "")
        
        self.assertEqual(len(edges_removed), 1)
        self.assertEqual(edges_removed[0][0], 2)
        self.assertEqual(edges_removed[0][1], 2)
        self.assertEqual(edges_removed[0][2], "test1")
        
    @unittest.skip('') 
    def test_prepare_pagerank_data__reinserts_data(self):
        # TODO
        placeholder = 0
    
    # @unittest.skip('') 
    def test_prepare_dynamic_pg_matricies(self):
        elem_entry_hm = {
            "all1": 0,
            "all2": 1,
            "test1": 2,
            "test2": 3,
            "test3": 4
        }
        data = [
            ["all1" , "ALL"  ,      "", "all2",      "", ""],
            ["all2" , "ALL"  ,      "",     "",      "", ""],
            ["test1", "TEST" , "test2",     "",      "", "test3"],
            ["test2", "TEST" ,      "",     "", "test3", ""],
            ["test3", "OTHER",      "",     "",      "", ""],
        ]
        cs = {"clean_name_pos": 0, "scrape_identifier_pos": 1, "jargon_entry_positions": [2,3,4] }
        
        matricies = create_data_set_specific_pg_matrices(data, elem_entry_hm, cs)
        # print(matricies[0][0])
        self.assertEqual(matricies[0][0][0][0], 0)
        self.assertEqual(matricies[0][0][0][1], 0)
        self.assertEqual(matricies[0][0][0][2], 0)
        
        self.assertEqual(matricies[0][0][1][0], 1)
        self.assertEqual(matricies[0][0][1][1], 0)
        self.assertEqual(matricies[0][0][1][2], 0)
        
        self.assertEqual(matricies[0][0][2][0], 0)
        self.assertEqual(matricies[0][0][2][1], 1)
        self.assertEqual(matricies[0][0][2][2], 0)
    
    
    def test_prepare_dynamic_pg_matricies(self):
        elem_entry_hm = {
            "all1": 0,
            "all2": 1,
            "test1": 2,
            "test2": 3,
            "test3": 4
        }
        data = [
            ["all1" , "ALL"  ,      "", "all2",      "", ""],
            ["all2" , "ALL"  ,      "",     "",      "", ""],
            ["test1", "TEST" , "test2",     "",      "", "test3"],
            ["test2", "TEST" ,      "",     "", "test3", ""],
            ["test3", "OTHER",      "",     "",      "", ""],
        ]
        cs = {"clean_name_pos": 0, "scrape_identifier_pos": 1, "jargon_entry_positions": [2,3,4,5] }
        
        matricies = create_data_set_specific_pg_matrices(data, elem_entry_hm, cs)
        # print(matricies[0][0])
        print(matricies[0])
        
        
if __name__ == '__main__':
    unittest.main()