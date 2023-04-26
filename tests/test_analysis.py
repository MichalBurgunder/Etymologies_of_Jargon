import unittest
import numpy as np
import copy
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.analysis_influence import create_pagerank_matrix, is_recursive, remove_cycles

"""
Most of these are sanity checks
"""

class PageRank(unittest.TestCase):

    @unittest.skip('')
    def test_create_pagerank_matrix1(self):
        headers = ['Cleaned Name', '1', '2', '3', '4']
        the_hashmap = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        cs = {'jargon_entry_positions': [1,2,3,4]}
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
        final_matrix = np.array(final_matrix).T
        
        # print(final_matrix)
        # print(np.asarray(pg_matrix))
        
        pg_matrix = create_pagerank_matrix(the_matrix, the_hashmap, headers, cs)
        self.assertEqual((final_matrix == pg_matrix).all(), True)
        # for i in range(0, 8):
        #     for j in range(0, 8):
        #         if final_matrix[i,j] != pg_matrix[i,j]:
        #             print(i, j, final_matrix[i,j], pg_matrix[i,j])
        
    @unittest.skip('')
    def test_create_pagerank_matrix1_recursion_removal(self):
        headers = ['Cleaned Name', '1', '2', '3', '4']
        the_hashmap = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        cs = {'jargon_entry_positions': [1,2,3,4]}
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
        
        final_matrix[0][3] = 1
        # final_matrix[1][3] = 0.5
        # final_matrix[1][4] = 0.5
        final_matrix[2][4] = 1
        final_matrix[3][5] = 1
        final_matrix[4][5] = 0.3333333333333333
        final_matrix[4][6] = 0.3333333333333333
        final_matrix[4][7] = 0.3333333333333333
        final_matrix[7][1] = 1
        final_matrix = np.array(final_matrix).T
        
        pg_matrix = create_pagerank_matrix(the_matrix, the_hashmap, headers, cs)
         
        for i in range(0, len(final_matrix)):
            for j in range(0, len(final_matrix)):
                print(i, j, final_matrix[i][j], pg_matrix[i][j])
                
        self.assertEqual((final_matrix == pg_matrix).all(), True)
        
    @unittest.skip('')
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
        
    @unittest.skip('')
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
        
    def test_prepare_influence_data__reinserts_data():
        # TODO
        return
    
if __name__ == '__main__':
    unittest.main()