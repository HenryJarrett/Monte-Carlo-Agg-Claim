# Description
Try the program: https://henry-jarrett-portfolio-monte-carlo.streamlit.app/

This program simulates aggregate claim amounts based on user-specified frequency and severity distributions. The user may select either a Poisson or Negative Binomial distribution for claim counts. For claim severity, the program supports Weibull, Pareto, and Lognormal distributions.

The program then runs a user-specified number of trials. Each trial begins by generating a random claim count from the chosen frequency distribution. For each claim, a random severity value is then generated from the specified severity distribution. All of the claim amounts are added together, and logged in a dictionary. 

Upon completion, the program summarizes the simulated portfolio by reporting the mean, mode, Value at Risk (VaR), and Tail Value at Risk (TVaR) at several selected percentiles. It also produces a scatter plot and a bar chart illustrating the distribution and frequency of aggregate claim amounts.

# Distribution Classes
Every distribution is represented by a class. These classes can be found in the 'distributions.py' file. The primary distribution function used is random(), random() is the function used when simulating claim counts or claim amounts. The function works by generating a decimal value between 0 and 1, it then uses the distribtuions inverse cdf to match a value of x to that uniform value.

# Set Up Guide
If you wish to run an unlimited version of this program on your home computer you will need to install pandas, streamlit, and python3. 

If you do not have python3 installed on your computer, please follow this guide: https://www.geeksforgeeks.org/python/download-and-install-python-3-latest-version/

The additional libraries can be installed using the following commands in your terminal(linux) or powershell(windows):
'pip install pandas'
'pip install streamlit'

Finally, download the program, enter the terminal/powershell in the directory with the downloaded files, and run it with it 'streamlit run app.py'
