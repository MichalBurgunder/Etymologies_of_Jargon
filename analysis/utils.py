
def concatenate(a1, a2):
    for e in a2:
        a1.append(e)
    return a1

def copy_array(arr):
    new = []
    for el in arr:
        new.append(el)
    return new