def timer(method):
    '''
    funtion for timing time elapsed for a given function
    Returns:
        +time elasped
    '''
    import time
    start = time.time()
    method()
    end = time.time()
    return end - start









        




    
