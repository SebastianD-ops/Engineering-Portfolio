#First Order Reaction simulation to determine final concentration of all species
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#model is ln(A) = -kt + ln(A_0) for first order
# more generall d[A]/dt = -k[A]
#examined reaction is CaCO3 + Heat -> CaO + CO2

#0th order -> 0, 1st -> 1, 2nd -> 2
#0th order linear in A vs t, 1st order linear in ln(A) vs t,

data = pd.read_csv('sample_data.csv')


def calc_least_squares_line(x, y):
    if len(x) > len(y):
        n = len(y)
    else:
        n = len(x)
    x_sum = sum([x[i] for i in range(n)])
    xy_sum = sum(x[i] * y[i] for i in range(n))
    y_sum = sum([y[i] for i in range(n)])
    x2_sum = sum([x[i] ** 2 for i in range(n)])
    m = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum ** 2)
    b = (y_sum - m * x_sum) / n

    residuals = [data.iloc[i]["Amount"] - m * data.iloc[i]["Time"] + b for i in range(n)]
    residuals_sqr = [residuals[i] ** 2 for i in range(n)]
    sum_residuals = sum(residuals_sqr)
    return m, b, n, sum_residuals


def calc_correlation_coefficient(x, y):
    if len(x) > len(y):
        n = len(y)
    else:
        n = len(x)
    x_mean = sum([x[i] for i in range(n)]) / n

    y_mean = sum([y[i] for i in range(n)]) / n

    x_minus_x_mean = [x[i] - x_mean for i in range(n)]

    y_minus_y_mean = [y[i] - y_mean for i in range(n)]

    x_minus_x_mean_y_minus_y_mean = [x_minus_x_mean[i] * y_minus_y_mean[i] for i in range(n)]
    x_minus_x_mean_sqr = [x_minus_x_mean[i] ** 2 for i in range(n)]
    y_minus_y_mean_sqr = [y_minus_y_mean[i] ** 2 for i in range(n)]
    x_minus_x_mean_y_minus_y_mean_sum = sum(x_minus_x_mean_y_minus_y_mean)
    x_minus_x_mean_sqr_sum = sum(x_minus_x_mean_sqr)

    y_minus_y_mean_sqr_sum = sum(y_minus_y_mean_sqr)

    r = x_minus_x_mean_y_minus_y_mean_sum / (x_minus_x_mean_sqr_sum * y_minus_y_mean_sqr_sum) ** (0.5)
    R = r ** 2
    return r, R


def get_k_values(x, y):
    if len(x) > len(y):
        n = len(y)
    else:
        n = len(x)
    # k = -slope
    k = [-(y[i] - y[i - 1]) / (x[i - 1] - x[i]) for i in range(1, n)]
    k_mean = sum(k) / n
    k_minus_mean = [k[i] - k_mean for i in range(len(k))]
    k_minus_mean_sqr = [k_minus_mean[i] ** 2 for i in range(len(k))]
    k_std = np.sqrt(sum(k_minus_mean_sqr) / (len(k_minus_mean_sqr) - 1))

    k_CV = abs(k_std * 100 / k_mean)

    return k, k_CV

class Dataset:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def test(self,x,y):
        m, b, n, sum_r = calc_least_squares_line(x, y)
        r, R = calc_correlation_coefficient(x, y)
        k, k_CV = get_k_values(x, y)

        return m,b,n,sum_r,r,R,k,k_CV
    def ZerothTest(self):
        m,b,n,sum_r,r,R,k,k_CV = self.test(self.x, self.y)
        plt.scatter(self.x,self.y)
        plt.plot(self.x, [m*self.x[i] + b for i in range(len(self.x))],'r')
        print(f"0th Order Model shows Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R}, k_CV:{k_CV}")
        plt.show()
    def FirstTest(self,y):
        self.lny = np.log(y[y['Amount'] > 0]['Amount'])
        m, b, n, sum_r, r, R, k, k_CV = self.test(self.x, self.lny)
        plt.scatter([self.x[i] for i in range(len(self.lny))], self.lny)
        plt.plot(self.x, [m * self.x[i] + b for i in range(len(self.x))], 'r')
        print(f"1st Order Model shows Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R}, k_CV:{k_CV}")
        plt.show()
    def SecondTest(self,y):
        self.invy = 1/(y[y['Amount'] > 0]['Amount'])
        m, b, n, sum_r, r, R, k, k_CV = self.test(self.x,self.invy)
        plt.scatter([self.x[i] for i in range(len(self.invy))], self.invy)
        plt.plot(self.x, [m * self.x[i] + b for i in range(len(self.x))], 'r')
        print(f"2nd Order Model shows Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R}, k_CV:{k_CV}")
        plt.show()


Calcium_Carbonate = Dataset(data["Time"],data["Amount"])
Calcium_Carbonate.ZerothTest()
Calcium_Carbonate.FirstTest(data)
Calcium_Carbonate.SecondTest(data)