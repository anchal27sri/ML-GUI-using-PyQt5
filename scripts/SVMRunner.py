import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")


from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import svm

class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = "SVM application"
        self.top = 300
        self.left = 600
        self.width = 400
        self.height = 300
        self.iconName = "C:/Users/user/Documents/pythonprog/ML/MLGUI/assets/python.png"
        self.initUI()
        
        
    def initUI(self):               
        
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.setDefault()        
        self.drawBrowser()
        self.drawSplit()                
        self.drawKernel()        
        self.drawRegParam()        
        self.drawDegree()        
        self.drawTolerance()        
        
        self.svmButton = self.createButton("Run",self.runSVM,330, 240,60, 30)
        
        self.show()
        
        
    def setDefault(self):
        # self.fileName = ""
        self.splitSize = 20
        self.regParam = 1.0
        self.kernelType = 'rbf'
        self.degree = 3
        self.tol = 0.001
        
    
    def drawBrowser(self):
        self.centralwidget = QWidget(self) 
        self.csv_label = QLabel(self.centralwidget) 
        self.csv_label.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.csv_label.setText("csv file: ")
        
        self.csv_lineEdit = QLineEdit(self)
        self.csv_lineEdit.setGeometry(QtCore.QRect(90,10,300,30))
        self.svmButton = self.createButton("Browse",self.getFileName,330, 50,60, 30)
        
    
        
    def drawSplit(self):
        self.split_label = QLabel("test_data size(%): ",self)
        self.split_label.setStyleSheet('background-color: yellow')              
        self.split_label.setGeometry(QtCore.QRect(40,80, 110, 30))
        
        self.split_lineEdit = QLineEdit(self)
        self.split_lineEdit.setGeometry(QtCore.QRect(160,80,50,30))
        self.split_lineEdit.setText(str(self.splitSize))
        
    def drawKernel(self):
        self.kernel_label = QLabel("kernel type: ",self)
        self.kernel_label.setStyleSheet('background-color: yellow')
        self.kernel_label.setGeometry(QtCore.QRect(40,120, 110, 30))
        
        self.kernel_cb = QComboBox(self)
        self.kernel_cb.setGeometry(QtCore.QRect(160,120,80,30))
        self.kernel_cb.addItems(["rbf", "linear", "poly","sigmoid"])
        self.kernel_cb.currentIndexChanged.connect(self.selectionChange)
        
    def drawRegParam(self):
        self.regParam_label = QLabel("regularizaiton\nparameter: ",self)
        self.regParam_label.setStyleSheet('background-color: yellow')
        self.regParam_label.setGeometry(QtCore.QRect(40,160, 110, 30))
        
        self.regParam_lineEdit = QLineEdit(self)
        self.regParam_lineEdit.setGeometry(QtCore.QRect(160,160,50,30))
        self.regParam_lineEdit.setText(str(self.regParam))
        
    def drawDegree(self):
        self.degree_label = QLabel("degree: ",self)
        self.degree_label.setStyleSheet('background-color: yellow')              
        self.degree_label.setGeometry(QtCore.QRect(40,200, 110, 30))
        
        self.degree_lineEdit = QLineEdit(self)
        self.degree_lineEdit.setGeometry(QtCore.QRect(160,200,50,30))
        self.degree_lineEdit.setText(str(self.degree))
        
        
    def drawTolerance(self):
        self.tol_label = QLabel("tol val: ",self)
        self.tol_label.setStyleSheet('background-color: yellow')              
        self.tol_label.setGeometry(QtCore.QRect(40,240, 110, 30))
        
        self.tol_lineEdit = QLineEdit(self)
        self.tol_lineEdit.setGeometry(QtCore.QRect(160,240,50,30))
        self.tol_lineEdit.setText(str(self.tol))
        
    
    def selectionChange(self):
        # print (self.kernel_cb.currentText())
        self.kernelType = self.kernel_cb.currentText()
    
    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:/Users/user/Documents/pythonprog/ML/MLGUI/scripts' , '*.csv')
        self.csv_lineEdit.setText(fileName)
        self.fileName = self.csv_lineEdit.text()
        #print(self.fileName)

    def runSVM(self):
        # print("--------TRAINING--------")
        if self.fileName != "":
            self.splitSize = int(self.split_lineEdit.text())
            self.kernelType = self.kernel_cb.currentText()
            self.degree = int(self.degree_lineEdit.text())
            self.regParam = float(self.regParam_lineEdit.text())
            self.tol = float(self.tol_lineEdit.text())
            if self.splitSize <=40:
                # print("test size =",self.splitSize,"%")
                # print("kernel:",self.kernelType)
                # print("degree:",self.degree)
                # print("tolerance value:",self.tol)
                # print("regularization parameter:",self.regParam)
                self.results = svm.run(self.fileName,self.splitSize,self.kernelType,self.degree,self.tol,self.regParam)
            else:
                pass# print("cannot train on such small dataset")
        else: 
            pass# print("incorrect file name!")            
        # print("--------SUCCESSFUL--------")
        

        QMessageBox.about(self,"Results:", self.results)
        

    def createButton(self, text, fun, x, y, l, w):
        pushButton = QPushButton(text, self) 
        pushButton.setGeometry(QtCore.QRect(x, y, l, w))
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