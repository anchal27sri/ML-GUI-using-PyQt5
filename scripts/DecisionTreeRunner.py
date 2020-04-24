import warnings
# ignore all future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")


from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
import DecesionTree

class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = "Decision Tree application"
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
        
        self.splitSize = 20

        self.drawBrowser()
        self.drawSplit()                
        self.drawCriterion()
        self.drawSplitter()        
        self.setDefault()
        
        self.svmButton = self.createButton("Run",self.runSVM,330, 240,60, 30)
        
        self.show()
        
        
    def setDefault(self):
        # self.fileName = ""
        self.crit_button1.setChecked(True)
        self.splitter_button1.setChecked(True)
        self.splitter = 'best'
        self.criterion = 'gini'
        
    
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
        
    def drawCriterion(self):
        self.crit_label = QLabel("Criterion: ",self)
        self.crit_label.setStyleSheet('background-color: yellow')              
        self.crit_label.setGeometry(QtCore.QRect(40,120, 80, 30))
        

        self.crit_group = QButtonGroup(self)
        self.crit_button1 = QRadioButton("gini",self)
        self.crit_button1.setGeometry(QtCore.QRect(160,125,80,20))
        self.crit_group.addButton(self.crit_button1)
        self.crit_button2 = QRadioButton("entropy",self)
        self.crit_button2.setGeometry(QtCore.QRect(250,125,80,20))
        self.crit_group.addButton(self.crit_button2)
        
    def drawSplitter(self):
        self.splitter_label = QLabel("Splitter: ",self)
        self.splitter_label.setStyleSheet('background-color: yellow')              
        self.splitter_label.setGeometry(QtCore.QRect(40,160, 80, 30))
        
        self.splitter_group = QButtonGroup(self)
        self.splitter_button1 = QRadioButton("best",self)
        self.splitter_button1.setGeometry(QtCore.QRect(160,165,80,20))
        self.splitter_group.addButton(self.splitter_button1)
        self.splitter_button2 = QRadioButton("random",self)
        self.splitter_button2.setGeometry(QtCore.QRect(250,165,80,20))
        self.splitter_group.addButton(self.splitter_button2)
    
    
    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:/Users/user/Documents/pythonprog/ML/MLGUI/scripts' , '*.csv')
        self.csv_lineEdit.setText(fileName)
        self.fileName = self.csv_lineEdit.text()
        #print(self.fileName)

    def runSVM(self):
        # print("--------TRAINING--------")
        if self.fileName != "":
            self.splitSize = int(self.split_lineEdit.text())
            
            if self.splitSize <=40:
                if self.splitter_button1.isChecked() is False:
                    self.splitter = 'random'
                if self.crit_button1.isChecked() is False:
                    self.criterion = 'entropy'
                # print("Test percentage: ",self.splitSize)
                # print("Criterion: ",self.criterion)
                # print("Splitter: ",self.splitter)
                self.results = DecesionTree.run(self.fileName,self.splitSize,self.criterion,self.splitter)
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