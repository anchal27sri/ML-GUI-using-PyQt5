import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")


from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
import DecesionTree
import MLP,make_model

class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = "MLP application"
        self.top = 300
        self.left = 600
        self.width = 400
        self.height = 300
        self.isModelReady = False
        self.iconName = "C:/Users/user/Documents/pythonprog/ML/MLGUI/assets/python.png"
        self.initUI()
        
        
    def initUI(self):               
        
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.setDefault()

        self.drawBrowser()
        self.drawSplit()
        self.drawTypeOfPrediction()
        self.drawEpochs()
        self.drawOptimizer()
        self.drawNoh()
           
        self.ModelButton = self.createButton('Make Model',self.call_make_model,270, 170, 120, 60)

        self.RunButton = self.createButton('Run',self.runSVM,330, 250, 60, 30)

        self.show()
        
        
    def setDefault(self):
        self.splitSize = 20
        self.TypeOfPrediction = 'Classification'
        self.epochs = 5
        self.optimizer = 'adam'
        self.hiddenLayers = 3        
        
    
    def drawBrowser(self):
        self.centralwidget = QWidget(self) 
        self.csv_label = QLabel(self.centralwidget) 
        self.csv_label.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.csv_label.setText("csv file: ")
        
        self.csv_lineEdit = QLineEdit(self)
        self.csv_lineEdit.setGeometry(QtCore.QRect(90,10,300,30))
        self.svmButton = self.createButton("Browse",self.getFileName,330, 50,60, 30)
        
    
        
    def drawSplit(self):
        self.split_label = QLabel("Test_data size(%): ",self)
        self.split_label.setStyleSheet('background-color: yellow')              
        self.split_label.setGeometry(QtCore.QRect(40,90, 110, 30))
        
        self.split_lineEdit = QLineEdit(self)
        self.split_lineEdit.setGeometry(QtCore.QRect(160,90,40,30))
        self.split_lineEdit.setText(str(self.splitSize))


    def drawTypeOfPrediction(self):
        self.prediction_label = QLabel("Type of Prediction: ",self)
        self.prediction_label.setStyleSheet('background-color: yellow')              
        self.prediction_label.setGeometry(QtCore.QRect(40,130, 110, 30))
        

        self.prediction_group = QButtonGroup(self)
        self.prediction_button1 = QRadioButton('Classification',self)
        self.prediction_button1.setGeometry(QtCore.QRect(160,135,100,20))
        self.prediction_group.addButton(self.prediction_button1)
        self.prediction_button1.setChecked(True)

        self.prediction_button2 = QRadioButton('Regression',self)
        self.prediction_button2.setGeometry(QtCore.QRect(270,135,85,20))
        self.prediction_group.addButton(self.prediction_button2)

        

    def drawEpochs(self):
        self.epochs_label = QLabel("Epochs: ",self)
        self.epochs_label.setStyleSheet('background-color: yellow')              
        self.epochs_label.setGeometry(QtCore.QRect(105,170, 45, 30))

        self.epochs_lineEdit = QLineEdit(self)
        self.epochs_lineEdit.setGeometry(QtCore.QRect(160,170,40,30))
        self.epochs_lineEdit.setText(str(self.splitSize))


    def drawOptimizer(self):
        self.optimizer_label = QLabel("Optimizer: ",self)
        self.optimizer_label.setStyleSheet('background-color: yellow')              
        self.optimizer_label.setGeometry(QtCore.QRect(90,210, 60, 30))

        self.optimizer_cb = QComboBox(self)
        self.optimizer_cb.setGeometry(QtCore.QRect(160,210,80,30))
        self.optimizer_cb.addItems(['adam', 'rmsprop', 'sgd'])
        

    def drawNoh(self):
        self.noh_label = QLabel("No of hiddel Layers: ",self)
        self.noh_label.setStyleSheet('background-color: yellow')              
        self.noh_label.setGeometry(QtCore.QRect(35,250, 115, 30))

        self.noh_lineEdit = QLineEdit(self)
        self.noh_lineEdit.setGeometry(QtCore.QRect(160,250,40,30))
        self.noh_lineEdit.setText(str(self.splitSize))


    def call_make_model(self):

        self.optimizer = self.optimizer_cb.currentText()    
        self.hiddenLayers = int(self.noh_lineEdit.text())

        if self.prediction_button1.isChecked is True:
            self.TypeOfPrediction = 'Classification'
        else:
            self.TypeOfPrediction = 'Regression'

        self.isModelReady = True
        self.setDisabled(True)
        self.m = make_model.Main(self,noh=self.hiddenLayers,category=self.TypeOfPrediction,optimizer=self.optimizer)

    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:/Users/user/Documents/pythonprog/ML/MLGUI/scripts' , '*.csv')
        self.csv_lineEdit.setText(fileName)
        self.fileName = self.csv_lineEdit.text()
        #print(self.fileName)

    def runSVM(self):

        if self.isModelReady is False:
            QMessageBox.about(self,'Message', 'The model is not made yet!\n Please make the model!')
            return

        # print("--------TRAINING--------")
        if self.fileName != "":
            self.splitSize = int(self.split_lineEdit.text())
            self.fileName = self.csv_lineEdit.text()
            self.epochs = int(self.epochs_lineEdit.text())       

            if self.splitSize <=40:
                # print("Test percentage: ",self.splitSize)
                self.results = MLP.run(file_name=self.fileName,model=self.m.temp_model,testing_percentage=self.splitSize)
            else:
                pass# print("cannot train on such small dataset")
        else: 
            pass# print("incorrect file name!")            
        # print("--------SUCCESSFUL--------")
        

        QMessageBox.about(self,"Results:", self.results)
        

    def createButton(self,text,fun,x,y,l,w):
        pushButton = QPushButton(text,self) 
        pushButton.setGeometry(QtCore.QRect(x,y,l,w))
        pushButton.clicked.connect(fun)
        return pushButton
        
        
def Main():
    m = mainWindow()
    m.show()
    return m
    
if __name__=="__main__":   
    import sys
    app = QApplication(sys.argv)
    mWin = mainWindow()
    sys.exit(app.exec_())