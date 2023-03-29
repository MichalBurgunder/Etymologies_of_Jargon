import numpy as np
import 

def pagerank(M, num_iterations: int = 100, d: float = 0.85):
    '''
    copied from wikipedia https://en.wikipedia.org/wiki/PageRank
    '''
    N = M.shape[1]
    v = np.ones(N) / N
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

def create_pagerank_matrix(data, elem_entry_hm, cs):
    n = len(data)
    the_matrix = np.array((n,n))
    
    for i in range(0, len(data)):
        answers = []
        for j in cs['jargon_entries']:
            if data[j] != '':
                answers.append(elem_entry_hm[data[i]])
        
        the_num = len(answers)
        for pos in answers:
            the_matrix[i][pos] = the_num
            
        pagerank(the_matrix)