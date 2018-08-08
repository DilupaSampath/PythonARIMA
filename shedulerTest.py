import schedule
import requests
import json
from pandas import Series
from statsmodels.tsa.arima_model import ARIMA
import modelSelectionPatientCount as im
import withArimaPost as ap
from datetime import datetime
import warnings
from pandas import read_csv
from math import sqrt
from sklearn.metrics import mean_squared_error
datetime.today()
datetime(2012, 3, 23, 23, 24, 55, 173504)

def parser(x):
	return datetime.strptime(x, '%d/%m/%Y')    

def ARIMA_model():
    print("I'm working...")
    print(datetime.today().weekday()+1)
    series = read_csv('E:/SLIIT/4th-Year/CDAP/Research/researchFinalDataset/colomboRain.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    p_values = [0, 1, 2, 3, 4, 5, 6]
    d_values = range(0, 3)
    q_values = range(0, 3)
    warnings.filterwarnings("ignore")
    im.evaluate_models(series.values, p_values, d_values, q_values)
    
    
def useArima():
    print("I'm working...")
    array=list()
    count=0
    series = Series.from_csv('E:/SLIIT/4th-Year/CDAP/Research/researchFinalDataset/colomboRain.csv', header=0)
    X = series.values
    size = len(X) + 48
    train, test = X[0:size], X[size:]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(0,1,2))
        model_fit = model.fit(trend='nc', disp=False)
        ar_coef, ma_coef = model_fit.arparams, model_fit.maparams
        resid = model_fit.resid
        diff = ap.difference(history)
        yhat = history[-1] + ap.predict(ar_coef, diff) + ap.predict(ma_coef, resid)
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        array.append(str(obs))
        print('>predicted=%d' % (yhat))
    rmse = sqrt(mean_squared_error(test, predictions))
    
    print('Test RMSE: %.3f' % rmse)
    
    json_mylist = json.dumps(array, separators=(',',':'))
    
    datastore = json.loads(json_mylist)
    r=requests.post('http://127.0.0.1:4000/weekModel/idhNextWeek',data=json.dumps({'count': str(datastore),"algorithmType":"ARIMA"}),headers={'Content-Type': 'application/json'})
    #r=requests.post("http://172.22.220.14:5000/arimaPost/", {'number': '12524'})
    print(r.status_code, r.reason) 

schedule.every().sunday.at("23:59").do(ARIMA_model)
schedule.every().wednesday.at("23:17").do(useArima)

            
while True:
    schedule.run_pending()