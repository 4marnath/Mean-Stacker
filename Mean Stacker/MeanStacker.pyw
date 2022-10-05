import numpy as np
from os import listdir
from sys import argv, exit
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont 
from PyQt5.QtWidgets import *
from astropy.io import fits

path = "No folder chosen"
filepaths = []
fileChosen = False

app = QApplication(argv)
widget = QWidget()

width = 400
height = 400

dirText = QLabel(widget)
dirText.setText(path)
dirText.setGeometry(int(width/48),  int(height/3.5), int(width - width/24), int(height/5))

errText = QLabel(widget)
errText.setText("")
errText.setGeometry(int(width/48), 80 + int(height/3), int(width - width/24), int(height/5))


def mean_fits():
    
    if (fileChosen):
        
        data = []
        mn = []

        for i in range(len(filepaths)):
            img = fits.open(filepaths[i])
            dataset = img[0].data
            data.append(dataset)
        data = np.array(data)

        for i in range(len(dataset[:, 0])):
            m = []
            for j in range(len(dataset[0,:])):   
                m.append(np.mean(data[:,j, i]))

            mn.append(m)
        adata =  np.array(mn)
        plt.figure("Stacked Image", figsize= (10, 8))
        plt.imshow(adata.T, cmap=plt.cm.viridis, aspect = "auto")
        plt.show()
        plt.colorbar()
            
    else:
        
        errText.setText("You need to choose a folder containing \nFITS files")

def folder():
        global path, fileChosen, filepaths; 
        path = "C:/"
        path = QFileDialog.getExistingDirectory(None, 'Select a folder', "C:/", QFileDialog.ShowDirsOnly)
        if path != '':
            files = listdir(path)
        else:
            files = []
            path = "C:/"
        
        filepaths = []
        for fname in files:
            if fname.endswith(".fits"):
                filepaths.append(path + "/" + fname)
        
        dirText.setText(path)
        if len(filepaths) > 0:
            fileChosen = True
            errText.setText("")
            
        else:
            fileChosen = False
            errText.setText("Chosen folder does not contain any FITS \nfile")
            path = "No folder chosen"

        return path
        

def window():
    global path
    
    font = QFont("Helvetica", 10)
    widget.setStyleSheet('background-color: #000023; color: white')
    widget.setGeometry(100, 100, width, height)
    widget.setWindowTitle("Stacker")
    widget.setFixedSize(width, height) 
    
    browseButton = QPushButton(widget)
    browseButton.setStyleSheet("""
        QPushButton {
            background-color: #7A0BC0; 
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #6A00AD;
        }
        QPushButton:pressed {
            background-color: #7A0BC0;
            
        }
    """)
    browseButton.setText("Choose Folder")
    browseButton.setGeometry(int(width/48), int(height/26), int(width - width/24), int(height/5))
    browseButton.setFont(font)
    browseButton.clicked.connect(folder)

    dirText.setFont(font)
    errText.setFont(font)
    errText.setStyleSheet('color: red')

    runButton = QPushButton(widget)
    runButton.setStyleSheet("""
        QPushButton {
            background-color: #29C7AC; 
            border-radius: 10px;
            color: black;
        }
        QPushButton:hover {
            background-color: #39D7BC;
        }
        QPushButton:pressed {
            background-color: #29C7AC;
            
        }
    """)
    runButton.setText("STACK")
    runButton.setGeometry(int(width/48), height - 100, int(width - width/24), int(height/5))
    runButton.setFont(font)
    runButton.clicked.connect(mean_fits)
    
    
    widget.show()
    
    exit(app.exec_())

run = True

while(run):
    window()
    
