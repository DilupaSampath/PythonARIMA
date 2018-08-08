# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:38:16 2018

@author: Nipunika
"""

from pandas import read_csv
from matplotlib import pyplot
from pandas import concat
from pandas import DataFrame
from pandas import Series
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
import numpy
from keras.models import load_model

# frame a sequence as a supervised learning problem
def timeseries_to_supervised(data, lag=1):
	df = DataFrame(data)
	columns = [df.shift(i) for i in range(1, lag+1)]
	columns.append(df)
	df = concat(columns, axis=1)
	df.fillna(0, inplace=True)
	return df

# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return Series(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

# scale train and test data to [-1, 1]
def scale(train, test):
	# fit scaler
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled

# inverse scaling for a forecasted value
def invert_scale(scaler, X, value):
	new_row = [x for x in X] + [value]
	array = numpy.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]

# make a one-step forecast
def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]

def predict():
    # load dataset
    series = read_csv('PatientData2.csv', header=0, parse_dates=True, index_col=0, squeeze=True)
    # summarize first few rows
    print(series.head())
    
    # transform data to be stationary
    raw_values = series.values
    diff_values = difference(raw_values, 1)
    print(diff_values.head())
    
    # transform data to be supervised learning
    supervised = timeseries_to_supervised(diff_values, 1)
    supervised_values = supervised.values
    print(supervised_values[:4])
    
    # split data into train and test-sets
    train, test = supervised_values[0:-156], supervised_values[-156:]
    
    # transform the scale of the data
    scaler, train_scaled, test_scaled = scale(train, test)
    
    # fit the model
    lstm_model = load_model('lstm_model.h5')
    # forecast the entire training dataset to build up state for forecasting
    train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
    lstm_model.predict(train_reshaped, batch_size=1)
    print(lstm_model)
    # walk-forward validation on the test data
    predictions = list()
    for i in range(len(test_scaled)):
    	# make one-step forecast
    	X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
    	yhat = forecast_lstm(lstm_model, 1, X)
    	# invert scaling
    	yhat = invert_scale(scaler, X, yhat)
    	# invert differencing
    	yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
    	# store forecast
    	predictions.append(yhat)
    	expected = raw_values[len(train) + i + 1]
    	print('Case=%d, Predicted=%f, Expected=%f' % (i+1, yhat, expected))
        
    # report performance
    rmse = sqrt(mean_squared_error(raw_values[-156:], predictions))
    print('Test RMSE: %.3f' % rmse)
    # line plot of observed vs predicted
    #pyplot.plot(raw_values[-156:])
    #pyplot.plot(predictions)
    #pyplot.show()
    return predictions
print(predict())
