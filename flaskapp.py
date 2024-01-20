from flask import Flask, render_template, request
import pandas as pd
import math 
import json

app = Flask(__name__)

def calculateVolatility(file):
    # Calculate all Volatility values
    niftyDf = pd.read_excel(file)
    niftyDf.columns = niftyDf.columns.str.strip()
    niftyDf["Returns"] = niftyDf["Close"].pct_change(1)
    niftyDf = niftyDf.set_index("Date")

    valDic = {}

    valDic['Daily Returns'] = json.loads(niftyDf[["Returns"]].to_json(date_format='iso'))
    sd = niftyDf["Returns"].std()
    valDic['Daily Volatility'] = sd
    valDic['Annualized Volatility'] = sd * math.sqrt(niftyDf.shape[0])

    return valDic


def checkFile(request):
    #Check if the request has file or file path

    calVal = None
    if request.method == 'POST' and request.form.get('path', '') == '' and request.files['file'].filename != '':
        file = request.files['file']
        calVal = calculateVolatility(file)
        return render_template("show.html", valueBundle=calVal)
    
    elif request.method == 'POST' and request.form.get('path', '') != '':
        file = request.form['path']
        calVal = calculateVolatility(file)
        
    return calVal




@app.route('/showDetails', methods = ['POST'])
def showDetails():
    volatilityVal = checkFile(request)
    if volatilityVal != None:
        return render_template("show.html", valueBundle=volatilityVal)
    else:
        return render_template("error.html")


@app.route('/volatility', methods = ['POST'])
def volatility():
    volatilityVal = checkFile(request)
    if volatilityVal != None:
        return volatilityVal
    else:
        return render_template("error.html")
    
    
@app.route('/')
def home():
    return render_template("upload.html")

if __name__ == '__main__':   
    app.run(debug=True, port=5000)