import distributions
#import matplotlib.pyplot as plt

def aggregateClaims(count, severity):
    num_claims = count.random()
    agg_claims = 0
    for i in range(num_claims):
        agg_claims += severity.random()
    return round(agg_claims)

def calculateTVaR(aggClaimDict, sampleSize, p):
    numClaims = 0
    i = 0
    while numClaims < int(sampleSize*p):
        if i in aggClaimDict:
            numClaims += aggClaimDict[i]
        i += 1
    VaR = i-1
    p = numClaims/sampleSize
    TVaR = 0
    cAbove = 0
    for j in range(i+1, max(aggClaimDict.keys())+1):
        if j in aggClaimDict:
            cAbove += aggClaimDict[j]
            TVaR += aggClaimDict[j]*j
    TVaR = TVaR/cAbove
    # Decrement i to account for i += 1 at the end of each iteration
    return p, VaR, TVaR

def calculateMeanMode(aggClaimDict, sampleSize):
    mean = 0
    mode = [0,0]
    for i in aggClaimDict.keys():
        mean += aggClaimDict[i]*i/sampleSize
        if aggClaimDict[i] > mode[1]:
            mode[0] = i
            mode[1] = aggClaimDict[i]
    return mean, mode[0]

def buildAggClaim(countDist, severityDist, sampleSize):
    aggClaimDict = {}

    # Run and log simulations
    for i in range(sampleSize):
        tempClaims = aggregateClaims(countDist, severityDist)
        if tempClaims in aggClaimDict:
            aggClaimDict[tempClaims] += 1
        else:
            aggClaimDict[tempClaims] = 1
    
    # Sort Dictionary by keys
    return dict(sorted(aggClaimDict.items()))

def sim(countDist, severityDist, sampleSize):
    aggClaimDict = buildAggClaim(countDist, severityDist, sampleSize)
    
    # Calculate mean and mode
    mean, mode = calculateMeanMode(aggClaimDict, sampleSize)
    

    # Calculate VaR for p = 0.9
    p_90, VaR_90, TVaR_90 = calculateTVaR(aggClaimDict, sampleSize, 0.90)

    # Calculate VaR for p = 0.95
    p_95, VaR_95, TVaR_95 = calculateTVaR(aggClaimDict, sampleSize, 0.95)
    
    # Calculate VaR for p = 0.99
    p_99, VaR_99, TVaR_99 = calculateTVaR(aggClaimDict, sampleSize, 0.99)

    # Calculate VaR for p = 0.995
    p_995, VaR_995, TVaR_995 = calculateTVaR(aggClaimDict, sampleSize, 0.995)


    # Display Statistics
    print("MEAN = " + str(mean))
    print("MODE = " + str(mode))
    print(str(p_90*100) + "% VaR = " + str(VaR_90) + " TVaR = " + str(TVaR_90))
    print(str(p_95*100) + "% VaR = " + str(VaR_95) + " TVaR = " + str(TVaR_95))
    print(str(p_99*100) + "% VaR = " + str(VaR_99) + " TVaR = " + str(TVaR_99))
    print(str(p_995*100) + "% VaR = " + str(VaR_995) + " TVaR = " + str(TVaR_995))

'''
    # Plot frequency of aggregate claim amounts
    plt.plot(aggClaimDict.keys(), aggClaimDict.values())
    plt.title("Aggregate Claim Frequency n = " + str(sampleSize))
    plt.xlabel("Aggregate Claim: " + severityDist.describe())
    plt.ylabel("Frequency: " + countDist.describe())
    plt.show()
    #print(aggClaimDict)
   ''' 

#countDist = distributions.Poisson(5)
#sevdist = distributions.Pareto(2, 3)
#sim(countDist, sevdist, 100000)
