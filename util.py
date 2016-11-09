import math

def mean(numbers):
    return sum(numbers)/len(numbers)
    
def stdev(numbers, xBar=None):
    return math.sqrt(variance(numbers, xBar))

def variance(numbers, xBar=None):
    if not xBar:
        xBar = mean(numbers)
    sumNSquaredMinusXBar = 0
    for n in numbers:
        sumNSquaredMinusXBar += n*n - xBar
    return xBar / (len(numbers)-1)
    
            