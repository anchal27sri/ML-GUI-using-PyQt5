import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")
#importing math modules
from math import sqrt

# Import required libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sklearn

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical 
import seaborn as sns


def make_model(input_dim,output_dim):
    temp_model = Sequential()
    temp_model.add(Dense(50, activation='relu', input_dim=input_dim))
    temp_model.add(Dense(10, activation='relu'))
    temp_model.add(Dense(5, activation='relu'))
    temp_model.add(Dense(output_dim, activation='softmax'))
    return temp_model



def run(file_name='C:/Users/user/Documents/pythonprog/ML/MLGUI/scripts/bill_authentication.csv',model = None, testing_percentage=20, target_col='Class', optimizer='adam',epochs=5):
    df = pd.read_csv(file_name) 
    # print(df.shape)
    df.describe()

    ts = (testing_percentage)/100
    target_column = [target_col] 
    predictors = list(set(list(df.columns))-set(target_column))
    #df[predictors] = df[predictors]/df[predictors].max()
    df.describe()

    X = df[predictors].values
    y = df[target_column].values

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=ts, random_state=40)
    # print(X_train.shape)
    # print(X_test.shape)

    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)

    Y_train = to_categorical(Y_train)
    Y_test = to_categorical(Y_test)

    count_classes = Y_test.shape[1]
    # print(count_classes)

    model = make_model(len(predictors),count_classes)
    # Compile the model
    model.compile(optimizer=optimizer, 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])

    # print(model.summary())
    history = model.fit(X_train, Y_train, epochs=epochs)
   
    pred_test = model.predict(X_test)

    # RESULTS: precesion, recall, f1score, accuracy
    results = classification_report(Y_test.argmax(axis=1), pred_test.argmax(axis=1))
    #print(results)

    #ploting confusion matrix
    cm = confusion_matrix(Y_test.argmax(axis=1), pred_test.argmax(axis=1),labels=[0,1])
    # print(cm)
    confusion = pd.DataFrame(cm, index = ['actual 0', 'actual 1'], columns = ['predicted 0','predicted 1'])
    sns.heatmap(confusion, annot = True)
    plt.figure()

    #plotting learning curve
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')

    plt.show()

    return results

# run()
