# Knapsack implementation
def knapsack(maxcapa : int, weights : list[int], values : list[int]) -> tuple[int,list[int]]:
    """
    Dynamic programming approach to solve the knapsack problem.
    \nArgs : 
        \n- maxcapa : maxcapacity of our knapsack
        \n- weights : list of weights of objects
        \n- values : list of values of each object
    \nReturns : 
        \n- A tuple (capacity,arr) where capacity is the actual used capacity by the next-to-be used items and
         arr[i] == True only if item i belongs to the optimal solution
    """
    n = len(weights)
    m = [[0 for x in range(maxcapa + 1)] for x in range(n + 1)]
    
    # find the maximum amount you can take
    for i in range(n + 1):
        for capa in range(maxcapa + 1):
            if i == 0 or capa == 0:
                m[i][capa] = 0
            elif weights[i - 1] <= capa:
                m[i][capa] = max(values[i - 1] + m[i - 1][capa - weights[i - 1]], m[i - 1][capa])
            else:
                m[i][capa] = m[i - 1][capa]
    max_value = m[n][maxcapa]

    #reconstruct the solution => find the items that are part of the optimal solution
    w = maxcapa
    res = [False for i in range(n)]
    for i in range(n, 0, -1):
        if max_value <= 0: #we already found every element that is part of the optimal solution
            break
        if max_value == m[i - 1][w]: #this item can't be included
            continue
        else:
            res[i - 1] = True
            max_value -= values[i - 1]
            w = w - weights[i - 1]
    return (m[n][maxcapa],res)
