def nearest_key(dict,target):
    """
    'Given a dict in which all keys are numeric, return the key closest to a
    supplied target.'

    Example:

    >>> testdict = {0:0, 10:0, 'foo':'bar', 20:0, 30:0, 40:0}
    >>> nearest_key(testdict,-1)
    0
    >>> nearest_key(testdict,0)
    0
    >>> nearest_key(testdict,1)
    0
    >>> nearest_key(testdict,5)
    0
    >>> nearest_key(testdict,6)
    10
    >>> nearest_key(testdict,45)
    40
    >>>

    """
    if target in dict.keys():
        return target
    leftneighbour = None
    rightneighbour = None
    for i in dict.keys():
        if not isinstance(i, (int, long, float, complex)): continue
        if i < target:
            if leftneighbour == None:
                leftneighbour = i
            elif leftneighbour < i:
                leftneighbour = i
        elif i > target:
            if rightneighbour == None:
                rightneighbour = i
            elif rightneighbour > i:
                rightneighbour = i            
    if leftneighbour == rightneighbour:
        return leftneighbour
    if leftneighbour == None:
        return rightneighbour
    elif rightneighbour == None:
        return leftneighbour
    elif (target - leftneighbour) <= (rightneighbour - target):
        return leftneighbour
    else:
        return rightneighbour




def _test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
    _test()
