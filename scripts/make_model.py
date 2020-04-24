import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")


from random import randint
from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import print_summary
import DecesionTree

class mainWindow(QMainWindow):
    
    def __init__(self,parent=None,nol=4,category='classification',no_of_output=2,no_of_features=4,optimizer='adam'):
        super().__init__()

        self.parent = parent
        self.title = 'Layer Information'
        self.top = 300 + randint(1,20)
        self.left = 600 +  randint(1,20)
        self.width = 400
        self.height = nol * 40 + 90
        self.nol = nol
        self.category = category
        self.output_size = no_of_output
        self.input_size = no_of_features
        self.optimizer = optimizer
        self.temp_model = Sequential()
        self.build = 0
        self.iconName = "C:/Users/user/Documents/pythonprog/ML/MLGUI/assets/python.png"
        self.initUI()
        
        
    def initUI(self):               
        
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        

        # self.nol_lineEdit = QLineEdit(self)
        # self.nol_lineEdit.setGeometry(QtCore.QRect(90,10,50,30))
        # self.nol_lineEdit.setText(str(self.nol))
        self.draw_layers()
        self.nol_button = self.createButton("Build Model",self.build_model,300,20,100,60)
        
        self.show()
        
    def draw_layers(self):

        #draw input layer info
        self.split_label = QLabel('Input Layer :   '+str(self.input_size),self)
        self.split_label.setGeometry(QtCore.QRect(20,10, 100, 30))
        
        #draw and enter hidden layer
        # print(self.nol)
        self.lt = []
        for i in range(self.nol):
            # print(i)
            a,b = self.create_layer_ui(i)
            self.lt.append([a,b])
            
        #draw output layer info
        if self.category=='classification':
            self.output_layer_activation = 'category'
        self.output_label = QLabel('Output Layer :   '+str(self.output_size),self)
        self.output_label.setGeometry(QtCore.QRect(20,50+self.nol*40, 100, 30))


    def create_layer_ui(self,y):

        #Label
        self.hidden_label = QLabel('layer '+str(y)+' :',self)
        self.hidden_label.setStyleSheet('background-color: yellow')              
        self.hidden_label.setGeometry(QtCore.QRect(20,50+y*40, 80, 30))

        #no_on_units
        self.nol_lineEdit = QLineEdit(self)
        self.nol_lineEdit.setGeometry(QtCore.QRect(110,50+y*40,50,30))
        self.nol_lineEdit.setText('4')

        #activation
        self.activation_cb = QComboBox(self)
        self.activation_cb.setGeometry(QtCore.QRect(180,50+y*40,80,30))
        self.activation_cb.addItems(["relu", "tanh", "softmax","sigmoid","linear"])

        return self.nol_lineEdit,self.activation_cb
    
    def build_model(self):
        self.temp_model = Sequential()
        for i in range(len(self.lt)):
            nou = int(self.lt[i][0].text())
            act = self.lt[i][1].currentText()
            if i==0:
                self.temp_model.add(Dense(units=nou,activation = act,input_dim=self.input_size))
            else:
                self.temp_model.add(Dense(units=nou,activation = act))

        if self.category=='classification':
            self.temp_model.add(Dense(units=self.output_size,activation='softmax'))
        else:
            self.temp_model.add(Dense(units=1,activation='linear'))
        if self.category == 'classification':    
            self.temp_model.compile(optimizer=self.optimizer,loss='categorical_crossentropy',metrics=['accuracy'])
        else:
            self.temp_model.compile(optimizer=self.optimizer,loss='mean_squared_error',metrics=['accuracy'])

        self.build =  self.build + 1

        QMessageBox.about(self,'Message','Model built!')
        
        self.close()
        self.parent.setDisabled(False)
        

    def createButton(self,text,fun,x,y,l,w):
        pushButton = QPushButton(text,self) 
        pushButton.setGeometry(QtCore.QRect(x,y,l,w))
        pushButton.clicked.connect(fun)
        return pushButton

               
def Main(parent=None,noh=4,category='classification',no_of_output=2,no_of_features=4,optimizer = 'adam'):
    m = mainWindow(parent,noh,category,no_of_output,no_of_features,optimizer)
    m.show()
    return m