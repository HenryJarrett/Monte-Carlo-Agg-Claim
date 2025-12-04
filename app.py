import streamlit as st
#import matplotlib.pyplot as plt
import distributions
import montecarlo
import pandas as pd

# Title
st.title("Monte Carlo Aggregate Claim Simulator\nBy Henry Jarrett")

# Get claim count distribution
st.subheader("Claim Count Distribution")
count_dist_name = st.selectbox(
        "Choose a distribution for the number of claims:",
        ["Poisson", "Negative Binomial"]
    )

#st.subheader("Claim Count Distribution Parameters")
if count_dist_name == "Poisson":
    mean = st.number_input("Mean (λ)", value=7, step=1)
if count_dist_name == "Negative Binomial":
    beta = st.number_input("Beta", value=3, step=.5)
    r = st.number_input("r", value=8, step=.5)

# Subheader
st.subheader("Claim Severity Distribution") 
# Get severity distribution from user
sev_dist_name = st.selectbox(
        "Choose a severity distribution:",
        ["Weibull", "Pareto", "Lognormal"]
    )
if sev_dist_name == "Weibull":
    shape = st.number_input("Shape (k)", value=2.0, step =1.0)
    scale = st.number_input("Scale (λ)", value=1000.0, step = 100.0)
elif sev_dist_name == "Pareto":
    shape = st.number_input("Shape (α)", value=2.5, step=.1)
    scale = st.number_input("Scale (xm)", value=500.0, step=100.0)
elif sev_dist_name == "Lognormal":
    mu = st.number_input("Mean", value=7.0, step=.5)
    sd = st.number_input("Standard Deviation", value=0.4, step=.1)

# SampleSize
SampleSize = st.number_input("Number of simulated losses", value=100000, min_value=1, step=50000)

# Run simulation button
if st.button("Run Simulation"):
    # Establish claim count distribution class
    if count_dist_name == "Poisson":
        count = distributions.Poisson(mean)
    if count_dist_name == "Negative Binomial":
        count = distributions.NegativeBinomial(beta, r)
    
    # Establish claim severity distribution class
    if sev_dist_name == "Weibull":
        sev = distributions.Weibull(shape, scale)
    if sev_dist_name == "Pareto":
        sev = distributions.Pareto(shape, scale)
    if sev_dist_name == "Lognormal":
        sev = distributions.Lognormal(mu, sd)
        
    # Run the Simulation
    aggClaimDict = {}
    
    with st.spinner("Running simulation..."):
        progress = st.progress(0)
        for i in range(SampleSize):
            tempClaims = montecarlo.aggregateClaims(count, sev)
            if tempClaims in aggClaimDict:
                aggClaimDict[tempClaims] += 1
            else:
                aggClaimDict[tempClaims] = 1
            if i % 1000 == 0:
                progress.progress(i / SampleSize)
        aggClaimDict = dict(sorted(aggClaimDict.items()))
        progress.progress(100)
    st.success("Simulation Complete")
    
    # Calculate and display mean and mode
    mean, mode = montecarlo.calculateMeanMode(aggClaimDict, SampleSize)


    st.write("Mean Aggregate Claim: " + str(round(mean,4)))
    st.write("Mode: " + str(mode))

    VaR_data = {}
    with st.spinner("Calculating value at risk..."):
        # Calculate VaR for p = 0.9
        p_90, VaR_90, TVaR_90 = montecarlo.calculateTVaR(aggClaimDict, SampleSize, 0.90)

        # Calculate VaR for p = 0.95
        p_95, VaR_95, TVaR_95 = montecarlo.calculateTVaR(aggClaimDict, SampleSize, 0.95)

        # Calculate VaR for p = 0.99
        p_99, VaR_99, TVaR_99 = montecarlo.calculateTVaR(aggClaimDict, SampleSize, 0.99)

        # Calculate VaR for p = 0.995
        p_995, VaR_995, TVaR_995 = montecarlo.calculateTVaR(aggClaimDict, SampleSize, 0.995)
        VaR_data = {
                "Percentile": [
                    str(round(p_90*100,2)) + "%",
                    str(round(p_95*100,2)) + "%",
                    str(round(p_99*100,2)) + "%",
                    str(round(p_995*100,2)) + "%"
                ],
                # Convert values to strings because then they sit on the left of the cell
                "VaR":[str(VaR_90),str(VaR_95),str(VaR_99),str(VaR_995)],
                "TVaR":[str(round(TVaR_90,2)),str(round(TVaR_95,2)),str(round(TVaR_99,2)),str(round(TVaR_995,2))]
            }
    st.success("Calculations Complete")
    st.table(VaR_data)

    # Display Graph
    x = aggClaimDict.keys()
    y = [y/SampleSize for y in aggClaimDict.values()]
    
    data = pd.DataFrame({
        'x': x,
        'y': y
        })
    st.write("Scatter Plot")
    st.scatter_chart(data, x='x', y='y', x_label="Aggregate Claim Amount", y_label="Frequency")
    st.write("Bar Chart")
    st.bar_chart(data, x='x', y='y', x_label="Aggregate Claim Amount", y_label="Frequency", stack=True)
    #fig, ax = plt.subplots()
    #ax.plot(x, y)
    #ax.set_title("Plot of aggregate losses by frequency")
    #ax.set_xlabel("Aggregate Claim Amount")
    #ax.set_ylabel("Frequency")
    
    #st.pyplot(fig)

