import random
import pandas as pd
from file_management import save_as_csv
from config import raw_data_root, root


def sample_from_csv(file_name, resulting_file_name):
    """
    Script for sampling 100 ruby gems from the available +170'000 
    """
    final_data = []

    df = pd.read_csv(f"{raw_data_root}/{file_name}.csv")
    number_rows = len(df.axes[0])
    random_numbers = [random.randrange(0, number_rows) for i in range(0,100)]
    
    for i in range(len(df)):
        if i in random_numbers:
            # lets automatically also clean the data
            word = ""
            for j in range(0,len(df.iloc[i, 0])):
                if df.iloc[i, 0][j] != "(":
                    word += df.iloc[i, 0][j]
                else:  
                    break
            final_data.append([word])

    save_as_csv(final_data, "sampled_gems", False, {"subfolder": "raw_data"})
    return f"{root}/{resulting_file_name}.csv"

sample_from_csv('gems', 'sampled_gems')