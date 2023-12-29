#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
	QHEXTextEdit v.0.0.1 - 2023-12-28 (Python3 / PyQt6 GUI extension)

	This is a new Python 3 / PyQt6 Widget that shows only hex values in a specialized QTextEdit namely QHEXTextEdit to represent the string as HEX value.
	The widget aims to follow the PyQt6 coding guidelines and has - beside PyQt6 - no dependensies.
	The drawing of the widget is completely done with PyQt6 functionality

	Author:		DaVe inc. Kim-David Hauser
	License:	MIT
	Git:		https://github.com/jetedonner/ch.kimhauser.python.helper
	Website:	https://kimhauser.ch
"""

import array
from enum import Enum

from PyQt6.QtGui import *
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtWidgets

from pyqtSwitch import *

class QHEXTextEdit(QTextEdit):
	
	doUpdateHexString:bool = True
	
	@property
	def insertSpace(self):
		return self._insertSpace
	
	@insertSpace.setter
	def insertSpace(self, new_insertSpace):
		self._insertSpace = new_insertSpace
		self.formatHexString()
		
	@property
	def onlyUpperCase(self):
		return self._onlyUpperCase
	
	@onlyUpperCase.setter
	def onlyUpperCase(self, new_onlyUpperCase):
		self._onlyUpperCase = new_onlyUpperCase
		self.formatHexString()
		
	def __init__(self, parent=None):
		QTextEdit.__init__(self, parent=parent)
		self.doUpdateHexString = True
		self._insertSpace = True
		self._onlyUpperCase = True
		
		cf = QTextCharFormat()
		cf.setFontCapitalization(QFont.Capitalization.MixedCase)
		self.setCurrentCharFormat(cf)
		self.textChanged.connect(self.self_textchanged)
		
	def keyPressEvent(self, event):
		key = event.key()
		cmd_modifier = (event.modifiers() == Qt.KeyboardModifier.ControlModifier)
		if cmd_modifier:
#			print(f"cmd_modifier: {cmd_modifier} / key: {key}")
			if key in (Qt.Key.Key_C, Qt.Key.Key_X, Qt.Key.Key_V, Qt.Key.Key_A):
				super().keyPressEvent(event)
				return
			
		if key in (Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4, Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9, Qt.Key.Key_A, Qt.Key.Key_B, Qt.Key.Key_C, Qt.Key.Key_D, Qt.Key.Key_E, Qt.Key.Key_F, Qt.Key.Key_Space, Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
			super().keyPressEvent(event)
		else:
			event.ignore()
			
	def self_textchanged(self):
		if not self.doUpdateHexString:
			return
		self.checkIsHexString()
		self.formatHexString()
		pass
		
	def checkIsHexString(self):
		try:
			int(self.toPlainText(), 16)
		except Exception as e:
			pass
			
	def formatHexString(self):
		self.doUpdateHexString = False
		cur = self.textCursor()
		origString = self.toPlainText()
		newString = ""
		self.setText("")
		idx = 0
		for c in origString:
			idx += 1
#			print(f"Char: {c}")
			if self.insertSpace and ((idx % 3 == 0) or idx == 3) and c != " ":
				newString += " "
				idx += 1
			elif not self.insertSpace and c == " ":
				continue
			
			if self.onlyUpperCase:
				newString += str(c).upper()
			else:
				newString += str(c)

		self.setText(newString)
		self.setTextCursor(cur)
		self.doUpdateHexString = True
		pass
		
		
class QHEXTextEditWindow(QMainWindow):
	"""PyMobiledevice3GUI's main window (GUI or view)."""
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QHEXTextEdit - Demo app v0.0.1")
		self.setMinimumSize(512, 320)
		
		self.layMain = QVBoxLayout()
		self.wdtMain = QWidget()
		self.wdtMain.setLayout(self.layMain)
		
		self.lblDesc = QLabel(f"This is a rought demo of the usage of QHEXTextEdit")
		self.layMain.addWidget(self.lblDesc)
		
		self.layOpt = QHBoxLayout()
		self.wdtOpt = QWidget()
		self.wdtOpt.setLayout(self.layOpt)
		
		self.swtInsertSpace = QSwitch("Insert Space", SwitchSize.Small, SwitchLabelPos.Trailing)
		self.swtInsertSpace.checked.connect(self.swtInsertSpace_checked)
		self.layOpt.addWidget(self.swtInsertSpace)
		
		self.swtUpper = QSwitch("Only UpperCase", SwitchSize.Small, SwitchLabelPos.Trailing)
		self.swtUpper.checked.connect(self.swtUpper_checked)
		self.layOpt.addWidget(self.swtUpper)
		
		self.layMain.addWidget(self.wdtOpt)
		
		self.txtHex = QHEXTextEdit()
		self.layMain.addWidget(self.txtHex)
		self.setCentralWidget(self.wdtMain)
		
	def swtInsertSpace_checked(self, checked):
		self.txtHex.insertSpace = checked
		pass
		
	def swtUpper_checked(self, checked):
		self.txtHex.onlyUpperCase = checked
		pass
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	win = QHEXTextEditWindow()
	win.show()
	sys.exit(app.exec())