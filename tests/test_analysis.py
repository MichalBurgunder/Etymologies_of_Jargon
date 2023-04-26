import unittest
import numpy as np
import copy
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.analysis_influence import create_pagerank_matrix

class PageRank(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()