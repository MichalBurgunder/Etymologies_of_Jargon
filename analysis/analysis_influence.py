import numpy as np
# import 

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
        

def recursive_influ(matrix, resulting_matrix, i, adder=0):
    # additional_here = 0
    for j in range(0,len(matrix[i])):
        if matrix[i][j] == 1:
            resulting_matrix[j] += 1
            adder += 1
            recursive_influ(matrix, resulting_matrix, j, adder)
            # print(i, additional)
            # additional_here += additional
    # print(additional_here)
    resulting_matrix[i] += adder
    # print(str(resulting_matrix))
    
    # return additional_here + 1
    return 0
    
def influence(matrix):
    n = matrix.shape[0]
    resulting_matrix = np.zeros(n)
    # arrival_matrix = np.zeros((n,n))
    # print(" A  B  C  D  E  F  G  H")
    for i in range(0,len(matrix)):
        recursive_influ(matrix, resulting_matrix, i) 
        
    return resulting_matrix
