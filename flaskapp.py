from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
import math 
from waitress import serve

app = Flask(__name__)

def calculateVolatility(file):
    niftyDf = pd.read_excel(file)
    niftyDf.columns = niftyDf.columns.str.strip()
    niftyDf["Returns"] = niftyDf["Close"].pct_change(1)
    niftyDf = niftyDf.set_index("Date")

    valDic = {}

    import json
    valDic['Daily Returns'] = json.loads(niftyDf[["Returns"]].to_json(date_format='iso'))
    sd = niftyDf["Returns"].std()
    valDic['Daily Volatility'] = sd
    valDic['Annualized Volatility'] = sd * math.sqrt(niftyDf.shape[0])

    return valDic


@app.route('/details', methods = ['POST'])
def details():

    print(request)
    
    print(request.files['file'].filename)
    print(request.form['path'])

    if request.method == 'POST' and request.form['path'] == "" and request.files['file'].filename != "":
        file = request.files['file']
        print("Test", file)
        calVal = calculateVolatility(file)
        return render_template("show.html", valueBundle=calVal)
    
    elif request.method == 'POST' and request.form['path'] != "":
        file = request.form['path']
        calVal = calculateVolatility(file)
        return render_template("show.html", valueBundle=calVal)
    
    else:
        return render_template("error.html")
    
    

@app.route('/')
def home():
    return render_template("upload.html")


if __name__ == '__main__':   
    app.run(debug=True)