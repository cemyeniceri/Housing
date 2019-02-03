import numpy
import pandas
from keras.layers import Dense
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# load dataset
dataFrame = pandas.read_csv("housing.csv", delim_whitespace=True, header=None)
dataset = dataFrame.values
# split into input (X) and output (Y) variables
X = dataset[:, 0:13]
Y = dataset[:, 13]


# define base model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)

kFold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kFold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# evaluate model with standardized dataset
numpy.random.seed(seed)
estimators = [('standardize', StandardScaler()),
              ('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0))]
pipeline = Pipeline(estimators)
kFold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kFold)
print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# define the model
def larger_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


numpy.random.seed(seed)
estimators = [('standardize', StandardScaler()),
              ('mlp', KerasRegressor(build_fn=larger_model, epochs=50, batch_size=5, verbose=0))]
pipeline = Pipeline(estimators)
kFold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kFold)
print("Larger: %.2f (%.2f) MSE" % (results.mean(), results.std()))


def wider_model():
    # create model
    model = Sequential()
    model.add(Dense(20, input_dim=13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


numpy.random.seed(seed)
estimators = [('standardize', StandardScaler()),
              ('mlp', KerasRegressor(build_fn=wider_model, epochs=100, batch_size=5, verbose=0))]
pipeline = Pipeline(estimators)
kFold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kFold)
print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# housing :  0.04741   0.00  11.930  0  0.5730  6.0300  80.80  2.5050   1  273.0  21.00 396.90   7.88  11.90
Xnew = numpy.array([[0.04741, 0.00, 11.930, 0, 0.5730, 6.0300, 80.80, 2.5050, 1, 273.0, 21.00, 396.90, 7.88]])
ynew = wider_model().predict(Xnew)
print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
