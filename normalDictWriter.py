import mathfuncs

def standardPdf(x):
    return mathfuncs.exponential(-(x**2)/2)/(2*3.141592653)**0.5

def standardCdf(x):
    n = 10000
    w = x/n
    simpsonSum = standardPdf(0)
    for i in range(n-1):
        tempP = standardPdf(w + w*i)
        if i % 2 == 0:
            simpsonSum += 4*tempP
        else:
            simpsonSum += 2*tempP
    simpsonSum += standardPdf(x)
    return 0.5 + simpsonSum*w/3

def inverseCdf(p):
    # Use bisection
    val = 0
    x0 = 0.5
    x1 = standardCdf(1)
    x2 = standardCdf(2)
    x3 = standardCdf(3)
    if p > x0 and p < x1:
        # val is between 0 and 1
        val = 0
    if p > x1 and p < x2:
        # val is between 1 and 2
        val = 1
    if p > x2 and p < x3:
        # val is between 2 and 3
        val = 2
    if p > x3:
        # val is greater than 3
        val = 3
    deci = 1
    while deci < 10:
        adder = 1*(10**(-deci))
        for i in range(10):
            if adder > 0:
                if p > standardCdf(val) and p < standardCdf(val + i*adder):
                    adder = 0
                else:
                    val += adder*i
        deci += 1
    return round(val, 3)




def standardDictWriter():
    n = 4000
    with open('normDict.py', 'w') as f:
        f.write('normDict = {\n')
        for i in range(n+1):
            x = i/1000
            if x == 4:
                f.write(str(x) + ':' + str(standardCdf(x)) +'}')
            else:
                f.write(str(x) + ':' + str(standardCdf(x)) + ',\n')

def inverseDictWriter():
    n = 500
    with open('invNormDict.py', 'w') as f:
        f.write('invNormDict = {\n')
        for i in range(n+1):
            p = round(0.5 + i/(n*2), 3)
            if p == 1:
                f.write(str(p) + ':' + str(inverseCdf(p)) +'}')
            else:
                f.write(str(p) + ':' + str(inverseCdf(p)) + ',\n')
