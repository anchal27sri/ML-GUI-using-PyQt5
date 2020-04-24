import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
#import matplotlib.pyplot as plt
#from sklearn.metrics import plot_confusion_matrix



def run(file_name, testing_percentage,crit,split):
    df = pd.read_csv(file_name)
    
    #df2 = df.reindex(np.random.permutation(df.index))
    #print(df)
    
    ts = (testing_percentage)/100
    #print(ts)
    #df = df.sample(frac=1).reset_index(drop=True)
    x = df.drop(columns=['Class'])
    y = pd.DataFrame(df['Class'])
    
    X = x.iloc[:, :].values
    Y = y.iloc[:, :].values
    #print("X shape:",x.shape,"\nY shape",y.shape)
    #Y.ravel()
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=ts,random_state=109)
    
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    #print(X_train)
    #Y_train.ravel()
    clf = DecisionTreeClassifier(criterion = crit,splitter = split)
    clf.fit(X_train,Y_train)
    
    Y_predict = clf.predict(X_test)
    cm = np.array(confusion_matrix(Y_test, Y_predict, labels=[0,1]))
    # print(cm)
    confusion = pd.DataFrame(cm, index = ['actual 0', 'actual 1'],
                                columns = ['predicted 0','predicted 1'])
    
    sns.heatmap(confusion, annot = True)
    plt.show()

    results = classification_report(Y_test, Y_predict)
    # print(results)
    # print(clf.score(X_test, Y_test))
    return results
#run('C:/Users/user/Documents/pythonprog/ML/MLGUI/scripts/bill_authentication.csv',20,'gini','best')
