import distributions

def aggregateClaims(count, severity):
    # Generate random number of claims accoriding to count distribution
    num_claims = count.random()
    agg_claims = 0

    # Generate random claim amounts according to severity distribution
    for i in range(num_claims):
        agg_claims += severity.random()
    return round(agg_claims)

def calculateTVaR(aggClaimDict, sampleSize, p):
    numClaims = 0
    i = 0
    # Advance to the p percentile in the claim dictionary
    while numClaims < int(sampleSize*p):
        if i in aggClaimDict:
            numClaims += aggClaimDict[i]
        i += 1
    # Value at risk is the p percentile of the aggregate claim dictionary
    VaR = i-1
    p = numClaims/sampleSize
    TVaR = 0
    cAbove = 0
    # Iterate through the rest of the dictionary to compute Tail Value at Risk
    for j in range(i+1, max(aggClaimDict.keys())+1):
        if j in aggClaimDict:
            cAbove += aggClaimDict[j]
            TVaR += aggClaimDict[j]*j

    # Mean loss given the loss is above the p percentile
    TVaR = TVaR/cAbove
    return p, VaR, TVaR

def calculateMeanMode(aggClaimDict, sampleSize):
    mean = 0
    mode = [0,0]
    for i in aggClaimDict.keys():
        mean += aggClaimDict[i]*i/sampleSize
        # Find the most common value 
        if aggClaimDict[i] > mode[1]:
            mode[0] = i
            mode[1] = aggClaimDict[i]
    return mean, mode[0]

