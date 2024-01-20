import pandas as pd
import math 

#Read File from the location
niftyDf = pd.read_excel('C:/Users/user/Downloads/NIFTY_50.xlsx')

#Remove extra whitespaces
niftyDf.columns = niftyDf.columns.str.strip()

#Calculate daily returns and store it in new column named 'Returns'
niftyDf["Returns"] = niftyDf["Close"].pct_change(1)

print("Daily returns: ")
print(niftyDf[["Date","Returns"]])

#Calculate Daily Volatility (standard deviation)
sd = niftyDf["Returns"].std()
print("Daily Volatility is", sd)

#Calculate Annualized Volatility
av = sd * math.sqrt(niftyDf.shape[0])
print("Annualized Volatility is",av)