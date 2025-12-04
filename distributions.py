import mathfuncs
from invNormDict import invNormDict

###################################################################################################
# Poisson Class - Class used to represent the Poisson distribution
# Parameters - mean, any positive number
# Intended Use - Generating random numbers of claims from a Poisson distribution
# Author - Henry Jarrett
###################################################################################################
class Poisson:
    def __init__(self, mean):
        self.lam = mean
 
    def pmf(self, x):
        return mathfuncs.exponential(-self.lam)*(self.lam**x)/mathfuncs.factorial(x)

    def cdf(self, x):
        p = 0
        for i in range(x+1):
            p += self.pmf(i)
        return p

    # Generate a random value
    def random(self):
        percentage = mathfuncs.uniformGen()
        tempPercentage, x = 0, 0
        while tempPercentage < percentage:
            tempPercentage += self.pmf(x)
            x+=1
        return x-1

    # Describe the distribution
    def describe(self):
        return "Poisson(Mean = " + str(self.lam) + ")"


###################################################################################################
# NegativeBinomial Class - Class used to represent the Negative Binomial distribution
# Parameters - beta, r, positive numbers
# Intended Use - Generating random numbers of claims from a Negative Binomial distribution
# Author - Henry Jarrett
###################################################################################################

class NegativeBinomial:
    def __init__(self, beta, r):
        self.beta = beta
        self.r = r
    
    def pmf(self, x):
        if x == 0:
            return (1 + self.beta)**-self.r
        numer = 1
        for i in range(x):
            numer*=(self.r + i)
        numer *= self.beta**x
        denom = mathfuncs.factorial(x)*((1+self.beta)**(self.r + x))
        return numer/denom
    
    def cdf(self, x):
        p = 0
        for i in range(x+1):
            p += self.pmf(i)
        return p
    
    # Generate a random value
    def random(self):
        percentage = mathfuncs.uniformGen()
        tempPercentage, x = 0, 0
        while tempPercentage < percentage:
            tempPercentage += self.pmf(x)
            x += 1
        return x-1

    # Describe the distribution
    def describe(self):
        return "Negative Binomial(r = " + str(self.r) + ", B = " + str(self.beta) + ")"


###################################################################################
# SEVERITY DISTRIBUTIONS 
###################################################################################

###################################################################################################
# Pareto Class - Class used to represent the two-parameter Pareto distribution
# Parameters - alpha, theta, any positive numbers
# Intended Use - Generating random claim severities
# Author - Henry Jarrett
###################################################################################################

class Pareto:
    def __init__(self, alpha, theta):
        self.alpha = alpha
        self.theta = theta
    
    def pdf(self, x):
        numer = self.alpha*(self.theta**self.alpha)
        denom = (x + self.theta)**(self.alpha + 1)
        return numer/denom

    def cdf(self, x):
        return 1 - ((self.theta/(self.theta + self.alpha))**self.alpha)

    def random(self):
        percentage = mathfuncs.uniformGen()
        # Solve for x given F(x)
        return (self.theta/((1-percentage)**(1/self.alpha))) - self.theta
    
    def describe(self):
        return "Pareto(Shape Parameter = " + str(self.theta) + ", Scale Parameter = " + str(self.alpha) + ")"

###################################################################################################
# Weibull Class - Class uesd to represent the Weibull distribution
# Parameters - theta, tau, any positive numbers
# Intended Use - Generating random claim severities
# Author - Henry Jarrett
###################################################################################################

class Weibull:
    def __init__(self, theta, tau):
        self.theta = theta
        self.tau = tau

    def random(self):
        percentage = mathfuncs.uniformGen()
        # Solve for x given F(x)
        return ((-mathfuncs.ln(1-percentage))**(1/self.tau))*self.theta

    def describe(self):
        return "Weibull(Shape Parameter = " + str(self.theta) + ", Scale Parameter = " + str(self.tau) + ")"

###################################################################################################
# Lognormal Class - Class used to represent the Lognormal distribution
# Parameters - mean, standard deviation, any positive numbers
# Intended Use - Generating random claim severities
# Author - Henry Jarrett
###################################################################################################

class Lognormal:
    def __init__(self, mean, sd):
        self.mean = mean
        self.sd = sd
    
    def random(self):
        percentage = mathfuncs.uniformGen()
        coef = 1
        if percentage < 0.5:
            coef = -1
            percentage = 1-percentage
        
        # Use the Dictionary representing the normal distribution to save time. (see /Dictionaries)
        zval = invNormDict[round(percentage,3)]*coef
        
        # Solve for x given z, F(x)
        return mathfuncs.exponential(zval*self.sd + self.mean)
    
    def describe(self):
        return "Lognormal(Mean = " + str(self.mean) + ", SD = " + str(self.sd) + ")"

###################################################################################################
# Gamma Class - Class used to represent the 2-parameter Gamma distribution
# Parameters - alpha, theta, theta can be any positive number, but alpha must be a positive integer
# Intended Use - Generating random claim severities
# Author - Henry Jarrett
###################################################################################################

class Gamma:
    def __init__(self, alpha, theta):
        # alpha must be an integer for the cdf function to work
        self.alpha = alpha
        self.theta = theta
    
    # Helper function for cdf()
    def _cdf(self, x):
        return (x**(self.alpha-1))*mathfuncs.exponential(-x)

    # Use Simpsons Rule to numerically integrate the Gamma function
    def cdf(self,x, n=10):
        # Divide x by theta because the CDF is GammaFunction(a; x/theta)
        lim = x/self.theta
        
        # w represents the difference between xi and xi+1
        w = lim/n

        # Evaluates w*(f(x0) + 4*f(x1) + 2*f(x2) + ...  + 4*f(xn-1) + f(xn))/3
        simpsonSum = self._cdf(0)
        for i in range(n-1):
            tempP = self._cdf(w + w*i)
            if i % 2 == 0:
                simpsonSum += 4*tempP
            else:
                simpsonSum += 2*tempP
        simpsonSum += self._cdf(lim)
        return simpsonSum*w/(3*mathfuncs.factorial(self.alpha-1))

    
    # Find a rough estimate of x given F(x)
    def invCdf(self, p, percision = 3):
        # Initial guess is the mean
        xi = self.theta*self.alpha
        # Represents whether the last iteration reduced or increased xi
        last = 0
        switch = 0
        while switch < percision:
            #print(xi)
            tempP = self.cdf(xi)
            if p > tempP:
                # Increment by a portion of the scale parameter
                xi += (10**(-switch - 2))*self.theta
                if last == -1:
                    switch += 1
                last = 1
            elif p < tempP:
                xi -= (10**(-switch-2))*self.theta
                if last == 1:
                    switch += 1
                last = -1
        return xi

    def random(self):
        percentage = mathfuncs.uniformGen()
        return self.invCdf(percentage)

    def describe(self):
        return "Gamma(Shape Parameter = " + str(self.alpha) + ", Scale Parameter = " + str(self.theta) + ")" 

