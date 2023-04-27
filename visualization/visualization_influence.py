import numpy as np

from visualization_utils import get_bargraph_data, key_to_long_title
from visualization_utils import root, read_csv

def print_nice_results(res, scrape_iden=''):
    """
    Prints out a latex appropriate text, to easily insert into the final document
    """
    final_data = []
    j = 0
    while(len(final_data) < 10): # we limit our tables to 10 entries
        if scrape_iden == '' or res[j][2] == scrape_iden:
            multiplier = int(res[j][1][len(res[j][1])-2:])
            first_three_digits = float(res[j][1][:4])
            final_data.append([res[j][0], f"{first_three_digits}e-{multiplier}"])
        j += 1

    print("SCRAPE IDENT : " + scrape_iden)
    final_string = "    \hline\n"
    final_string += f"    {final_data[0][0]}"

    for i in range(1, len(final_data)):
        final_string += f" & {final_data[i][0]}"
        
    final_string += " \\\\\n    \hline"
    
    final_string += f"\n    {final_data[0][1]}"
    
    for i in range(1, len(final_data)):
        final_string += f" & {final_data[i][1]}"
    
    # res = f"\\begin\{tabular\}c\{c\{'|c' * len(final_data)}}"
    final_string += " \\\\\n    \hline\n\n"
    print(final_string)
    
def print_page_rank_data(data_set):
    data = read_csv(f"page_rank_results_{data_set}")
    print_nice_results(data, data_set)
    return