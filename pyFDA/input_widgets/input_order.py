# -*- coding: utf-8 -*-
"""
Widget for selecting / entering manual or minimum filter order

@author: juliabeike, Christian Muenker
Datum: 20.01.2015
"""
from __future__ import print_function, division, unicode_literals
import sys, os
from PyQt4 import QtGui

# import filterbroker from one level above if this file is run as __main__
# for test purposes
if __name__ == "__main__": 
    __cwd__ = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(__cwd__ + '/..')

import filterbroker as fb

class InputOrder(QtGui.QFrame):
    """
    Build and update widget for selecting either 
    - manual filter order, specified by an integer 
    - minimum ('min') filter order
    """
    
    def __init__(self, DEBUG = False):
        super(InputOrder, self).__init__()
        self.DEBUG = DEBUG        
        self.initUI()

        
    def initUI(self):
  
        title = "Filter Order"
        
        bfont = QtGui.QFont()
        ifont = QtGui.QFont()
  #      font.setPointSize(11)
        bfont.setBold(True)
        bfont.setWeight(75)
        ifont.setItalic(True)
        
        # Print subwidget title
        self.titleLabel = QtGui.QLabel(title)
        self.titleLabel.setFont(bfont)

        self.chkMin = QtGui.QRadioButton("Minimum",self)          
        self.spacer = QtGui.QSpacerItem(20,0,
                        QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.txtLabel = QtGui.QLabel("N = ")
        self.txtLabel.setFont(ifont)
        self.txtManual=QtGui.QLineEdit(str(fb.gD['selFilter']['N']),self)
 #       self.txtManual.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        #----------------------------------------------------------------------
        # Construct widget layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.chkMin)
        hbox.addItem(self.spacer)
        hbox.addWidget(self.txtLabel)
        hbox.addWidget(self.txtManual)
       
        foFrame = QtGui.QFrame()
        foFrame.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        foFrame.setLayout(hbox)        
        foFrame.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                 QtGui.QSizePolicy.Minimum)
        
        mainLayout = QtGui.QVBoxLayout() # widget main layout
        mainLayout.addWidget(self.titleLabel)
        mainLayout.addWidget(foFrame)
        self.setLayout(mainLayout)
#        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        #----------------------------------------------------------------------
        # SIGNALS & SLOTs

        self.chkMin.clicked.connect(self.updateEntries)
        self.txtManual.editingFinished.connect(self.updateEntries)
        
        self.updateEntries() # initialize with default settings
        
    def updateEntries(self):
        """
        Read / write text entries and checkbutton for filter order
        """
        # read list of available filter order methods from filterTree:
        foList = fb.gD['filterTree'][fb.gD['selFilter']['rt']]\
                [fb.gD['selFilter']['ft']][fb.gD['selFilter']['dm']].keys()
        if self.DEBUG: 
            print("=== InputOrder.update() ===")            
            print("foList", foList)

        if fb.gD['selFilter']['fo'] in foList:
            fo = fb.gD['selFilter']['fo'] # keep current setting
        else:
            fo = foList[0] # use first list entry from filterTree
            fb.gD['selFilter']['fo'] = fo # and update 'selFilter'

        # Determine which subwidgets are __visible__
        self.txtLabel.setVisible('man' in foList)
        self.txtManual.setVisible('man' in foList)  
        self.chkMin.setVisible('min' in foList)            

        if self.DEBUG: print("fo[selFilter] =", fo)   

        # Determine which subwidgets are _enabled_
        if 'min' in foList:
            if self.chkMin.isChecked() == True:
                # update in case N has been changed outside this class
                self.txtManual.setText(str(fb.gD['selFilter']['N'])) 
                self.txtManual.setEnabled(False)
                self.txtLabel.setEnabled(False)
                fb.gD['selFilter'].update({'fo' : 'min'})
            else:
                self.txtManual.setEnabled(True)
                self.txtLabel.setEnabled(True)
                fb.gD['selFilter'].update({'fo' : 'man'})
        else:
            self.txtLabel.setEnabled(fo == 'man')
            self.txtManual.setEnabled(fo == 'man')

        ordn = int(self.txtManual.text())
        fb.gD['selFilter'].update({'N' : ordn})
   
#------------------------------------------------------------------------------        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = InputOrder()
    form.show()
    form.chkMin.setChecked(True)
    form.update()
    print(fb.gD['selFilter']['fo'])
    form.chkMin.setChecked(False)
    form.update()
    print(fb.gD['selFilter']['fo'])

    app.exec_()


   
        



 