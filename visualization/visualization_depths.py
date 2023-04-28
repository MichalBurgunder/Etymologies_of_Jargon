from visualization_utils import read_csv, create_bar_graph_log_subplots

def number_of_depths(file_name, data_set='ALL'):
    """
    Creates a bar graph/histogram with all the etymological depths of a specific
    file
    """
    rows = read_csv(file_name)
    nums = [] # position of where the depth is located
    max_value = 0
    for row in rows:
        max_value = max(max_value, int(row[1]))
        if data_set == 'ALL' or row[2] == data_set:
            nums.append(int(row[1]))
    
    bars = [nums.count(i) for i in range(0, max_value+1+1)] # +1 to add the last one, +1 to signify the end

    info = {
        "xlabel": "Occurences",
        "ylabel": "No. of Etymology Depths",
        "data_set": data_set
    }
    return create_bar_graph_log_subplots(list(bars), list(range(0, len(bars))), info)
