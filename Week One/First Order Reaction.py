#First Order Reaction simulation to determine final concentration of all species
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

#examined reaction is CaCO3 + Heat -> CaO + CO2

data = pd.read_csv('Noisy_First_Order.csv')


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

    residuals = [y.iloc[i] - (m * x.iloc[i] + b) for i in range(n)]
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


class Dataset:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.R_vals = []
        self.sum_r_vals = []
    def test(self,x,y):
        m, b, n, sum_r = calc_least_squares_line(x, y)
        r, R = calc_correlation_coefficient(x, y)

        return m,b,n,sum_r,r,R
    def ZerothTest(self):
        m,b,n,sum_r,r,R = self.test(self.x, self.y)

        self.R_vals.append(R)
        self.sum_r_vals.append(sum_r)
        self.zerothk = m

        plt.scatter(self.x,self.y)
        plt.plot(self.x, [m*self.x[i] + b for i in range(len(self.x))],'r')
        self.ztestline = (f"0th Order Model shows \n --------------------------------- \n  Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R} \n --------------------------------- \n")
        plt.title("Zeroth Order Reaction")
        plt.show()
    def FirstTest(self,y):
        self.lny = np.log(y[y['Amount'] > 0]['Amount'])
        m, b, n, sum_r, r, R = self.test(self.x, self.lny)

        self.R_vals.append(R)
        self.sum_r_vals.append(sum_r)
        self.firstk = m

        plt.scatter([self.x[i] for i in range(len(self.lny))], self.lny)
        plt.plot(self.x, [m * self.x[i] + b for i in range(len(self.x))], 'r')
        self.ftestline = (f"1st Order Model shows \n --------------------------------- \n  Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R} \n --------------------------------- \n")
        plt.title("First Order Reaction")
        plt.show()
    def SecondTest(self,y):
        self.invy = 1/(y[y['Amount'] > 0]['Amount'])
        m, b, n, sum_r, r, R = self.test(self.x,self.invy)

        self.R_vals.append(R)
        self.sum_r_vals.append(sum_r)
        self.secondk = m

        plt.scatter([self.x[i] for i in range(len(self.invy))], self.invy)
        plt.plot(self.x, [m * self.x[i] + b for i in range(len(self.x))], 'r')
        self.stestline = (f"2nd Order Model shows \n --------------------------------- \n Gradient:{m}, y-int:{b}, sum of the residuals:{sum_r}, Coefficient of Determination:{R} \n --------------------------------- \n")
        plt.title("Second Order Reaction")
        plt.show()
    def BestFit(self):
        max_R = max(self.R_vals)
        test_num_r = self.R_vals.index(max_R)
        min_sum_r = min(self.sum_r_vals)
        test_num_sum_r = self.sum_r_vals.index(min_sum_r)

        if test_num_r == test_num_sum_r:
            if test_num_r == 0:
                type = "Zeroth Order Reaction"
                k = abs(self.zerok)
            elif test_num_r == 1:
                type = "First Order Reaction"
                k = f"{abs(self.firstk)}/s"
            elif test_num_r == 2:
                type = "Second Order Reaction"
                k = f"{abs(self.secondk)}L/mol/s"

            self.bestfitline = f"\nPredicted Reaction Order: \n     {type} \nEstimated k: \n     {k}"
        else:
            self.bestfitline = ("\nInconclusive Results\n")
    def TestAll(self,y):
        self.ZerothTest()
        self.FirstTest(y)
        self.SecondTest(y)



if __name__ == "__main__"
    Calcium_Carbonate = Dataset(data["Time"], data["Amount"])
    Calcium_Carbonate.TestAll(data)
    Calcium_Carbonate.BestFit()

    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(file_name, 'w') as file:
        file.write(Calcium_Carbonate.ztestline)
        file.write(Calcium_Carbonate.ftestline)
        file.write(Calcium_Carbonate.stestline)
        file.write(Calcium_Carbonate.bestfitline)


