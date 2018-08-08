from pandas import Series
from flask import jsonify
import requests
import json
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"


def predict(coef, history):
                yhat = 0.0
                for i in range(1, len(coef)+1):
                                yhat += coef[i-1] * history[-i]
                return yhat

def difference(dataset):
                diff = list()
                for i in range(1, len(dataset)):
                                value = dataset[i] - dataset[i - 1]
                                diff.append(value)
                return numpy.array(diff)
            
#def goR():
#    array=list()
#    count=0
#    series = Series.from_csv('E:/SLIIT/4th-Year/CDAP/Research/researchFinalDataset/colomboRain.csv', header=0)
#    X = series.values
#    size = len(X) - 48
#    train, test = X[0:size], X[size:]
#    history = [x for x in train]
#    predictions = list()
#    for t in range(len(test)):
#        model = ARIMA(history, order=(0,1,2))
#        model_fit = model.fit(trend='nc', disp=False)
#        ar_coef, ma_coef = model_fit.arparams, model_fit.maparams
#        resid = model_fit.resid
#        diff = difference(history)
#        yhat = history[-1] + predict(ar_coef, diff) + predict(ma_coef, resid)
#        predictions.append(yhat)
#        obs = test[t]
#        history.append(obs)
#        array.append(str(obs))
#        print('>predicted=%d, expected=%d' % (yhat, obs))
#    rmse = sqrt(mean_squared_error(test, predictions))
#    
#    print('Test RMSE: %.3f' % rmse)
#    
#    json_mylist = json.dumps(array, separators=(',',':'))
#    
#    datastore = json.loads(json_mylist)
#    print(str(datastore))
#    print(datastore)
#    print(type(datastore))
#    
#    r=requests.post('http://127.0.0.1:5000/arimaPost/',data=json.dumps({'month': str(datastore)}),headers={'Content-Type': 'application/json'})
#    #r=requests.post("http://172.22.220.14:5000/arimaPost/", {'number': '12524'})
#    print(r.status_code, r.reason) 