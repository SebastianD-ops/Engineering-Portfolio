#First Order Reaction simulation to determine final concentration of all species
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#model is ln(A) = -kt + ln(A_0)
#examined reaction is CaCO3 + Heat -> CaO + CO2

data = pd.read_csv('sample_data.csv')


def calc_least_squares(data):
    m = (data.iloc[-1].Amount - data.iloc[0].Amount) / (data.iloc[-1].Time - data.iloc[0].Time)
    b = data.iloc[0].Amount
    residuals = [data.loc[data['Time'] == i, 'Amount'] - (m * i + b) for i in data.Time]
    
    return residuals, m, b

residuals, m, b = calc_least_squares(data)

for i in residuals: print(i)
print(m)
print(b)

plt.scatter(data.Time, data.Amount)
plt.scatter(data.Time, residuals)
plt.plot(range(0,30),m*range(0,30) + b)
plt.show()