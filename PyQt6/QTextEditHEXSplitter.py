#!/usr/bin/env python3

from enum import Enum

from PyQt6.QtGui import *
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtWidgets

#class SwitchSize(Enum):
#	Small = 1
#	Medium = 2
#	Large = 3
#	
#class SwitchLabelPos(Enum):
#	Leading = 1
#	Trailing = 2
#	Above = 3
#	Below = 4
		
class QTextEditHEXSplitter(QWidget):
		
	def __init__(self, parent=None): #, descTxt:str, switchSize:SwitchSize = SwitchSize.Small, switchLabelPos:SwitchLabelPos = SwitchLabelPos.Trailing, parent=None):
		QWidget.__init__(self, parent=parent)
		
		self.layMain = QVBoxLayout()
		self.setLayout(self.layMain)
		self.splitter = QSplitter()
		self.splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		
		self.txtMultiline = QTextEdit()
		self.txtMultiline.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
#		self.txtMultiline.textChanged.connect(self.txtMultiline_textchanged)
		self.txtMultiline.selectionChanged.connect(self.txtMultiline_selectionchanged)
		
		self.txtMultilineHex = QTextEdit()
		self.txtMultilineHex.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		
		self.splitter.addWidget(self.txtMultiline)
		self.splitter.addWidget(self.txtMultilineHex)
#		self.layMain.addWidget(self.splitter)
		
		self.showHex = QCheckBox("HEX View")
		self.showHex.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.showHex.setChecked(True)
		self.showHex.stateChanged.connect(self.showHex_changed)
		
		self.cmbEncoding = QComboBox()
		self.cmbEncoding.addItem("utf-8")
		self.cmbEncoding.addItem("utf-16")
		self.cmbEncoding.addItem("ascii")
#		self.cmbEncoding.currentIndexChanged.connect(self.cmbEncoding_changed)
		self.cmbEncoding.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		
		encodingLabel = QLabel(f"Encoding:")
		encodingLabel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		layoutTop = QHBoxLayout()
		widTop = QWidget()
		widTop.setLayout(layoutTop)
		
#		layoutTop.addWidget(self.instructionsLabel)
		layoutTop.addStretch()
		layoutTop.addWidget(encodingLabel)
		layoutTop.addWidget(self.cmbEncoding)
		
		layoutTop.addWidget(self.showHex)
		
		self.layMain.addWidget(widTop)
		self.layMain.addWidget(self.splitter)
		
		self.setText("KIM SAYS: Some amended Text to test the new to HEX function and the save function fix - IT WORKS!!! KIMs amendent ... Some addition!!!")
		
#		layButtons = QHBoxLayout()
#		widButtons = QWidget()
#		widButtons.setLayout(layButtons)
#		
#		layButtons.addStretch()
#		
#		# Add the buttons to the layout
#		layButtons.addWidget(self.confirmButton, Qt.AlignmentFlag.AlignRight)
#		layButtons.addWidget(self.cancelButton, Qt.AlignmentFlag.AlignRight)
#		
#		layButtons.addWidget(self.confirmButton)
#		layButtons.addWidget(self.cancelButton)
#		
#		layout.addWidget(widButtons)
#		
#		# Set the layout of the dialog
#		self.setLayout(layout)
		
	def txtMultiline_selectionchanged(self):
		cursor = self.txtMultiline.textCursor()
		print("Selection start: %d end: %d" % (cursor.selectionStart(), cursor.selectionEnd()))
		
		
#		# Create a text cursor
#		cursorReset = self.txtMultilineHex.textCursor()
#		
#		# Move the cursor to the beginning of the block
#		cursorReset.movePosition(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
#		
#		# Set the cursor to the beginning of the text
##		cursorReset.moveToBlockStart()
#		
#		# Create a text block format
#		formatReset = QTextCharFormat() # QTextBlockFormat()
#		formatReset.setBackground(QColor(0, 0, 0, 0))  # Transparent background color
#		
#		# Apply the format to the text
##		cursorReset.setBlockFormat(formatReset)
#		cursorReset.setCharFormat(formatReset)
#		
#		# Set the text cursor
#		self.txtMultilineHex.setTextCursor(cursorReset)
#		self.txtMultilineHex.ensureCursorVisible()
		
#		self.txtMultilineHex.setTextCursor(QTextCursor())
#		self.txtMultilineHex.ensureCursorVisible()
		
		self.txtMultilineHex.setStyleSheet("background-color: control;")
		
		c = self.txtMultilineHex.textCursor()
		c.clearSelection()
		c.setPosition(cursor.selectionStart() * 3)
		c.setPosition((cursor.selectionEnd() * 3), QTextCursor.MoveMode.KeepAnchor)
		self.txtMultilineHex.setStyleSheet("selection-background-color: #ff0000;")
		
		self.txtMultilineHex.setTextCursor(c)
		self.txtMultilineHex.ensureCursorVisible()
#		
#		color = QColor(255, 0, 0)  # Red color
#		format = QTextCharFormat()
##		format.setForeground(color)
#		format.setBackground(color)
#		
#		# Apply the format to the text
#		c.setCharFormat(format)
##		# Create a new text block format
##		formatReset = QTextBlockFormat()
##		formatReset.setBackground(QColor(0, 0, 0, 0))  # Transparent background color
##		
##		# Set the text block format to the entire text
##		self.txtMultilineHex.setTextFormat(formatReset)
#		
#		self.txtMultilineHex.setTextCursor(c)
#		self.txtMultilineHex.ensureCursorVisible()
##		self.txtMultilineHex.setTextCursor(QTextCursor())
##		self.txtMultilineHex.ensureCursorVisible()
##		c.setTextColor(color)
##		
##		# Create a text cursor
##		cursor = text_edit.textCursor()
##		
##		# Move the cursor to the beginning of the text
##		cursor.movePosition(QTextCursor.Start)
#		
#		# Set the text color
##		c.setTextColor(color)
#		
##		# Get the cursor position
##		cursor_pos = self.txtMultiline.cursorPosition()
##		
##		print("Cursor position:", cursor_pos)
##		
##		if cursor_pos == 0:
##			print("No text is selected.")
##		else:
##			print("Selected text:", self.txtMultiline.toPlainText()[:cursor_pos])
#		
#		
#		# Get the start and end positions of the selected text
##		start_pos = self.txtMultiline.selectionStart()
##		end_pos = self.txtMultiline.selectionEnd()
##		
##		print("Start position:", start_pos)
##		print("End position:", end_pos)
##		
##		if start_pos == end_pos:
##			print("No text is selected.")
##		else:
##			print("Selected text:", self.txtMultiline.toPlainText()[start_pos:end_pos])
		
	def setText(self, text):
		self.txtMultiline.insertPlainText(text)
		self.setTxtHex(text)
		
	def setTxtHex(self, text:str = None):
		self.txtAsString = text
		if self.txtAsString is None:
			self.txtAsString = self.txtMultiline.toPlainText()
			
		try:
			self.txtInBytes = self.txtAsString.encode("utf-8")
			self.hexData = [format(byte, '02x') for byte in self.txtInBytes] # self.fileContent]
			# Format the hexadecimal data for display
			self.formattedHexData = ' '.join(self.hexData)
			self.txtMultilineHex.setText(str.upper(self.formattedHexData))
		except Exception as e:
			print(f"Exception: '{e}' while converting text '{self.txtAsString}' to HEX string")
			pass
			
	def showHex_changed(self, checked):
		self.splitter.widget(1).setVisible(checked)
#		
#	@pyqtSlot(bool)
#	def checked_changed(self, checked):
#		self.checked.emit(checked)

class QTextEditHEXSplitterWindow(QMainWindow):
	"""PyMobiledevice3GUI's main window (GUI or view)."""
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QTextEditHEXSplitter.py - Demo app v0.0.1")
		self.setFixedSize(1024, 640)
		
		self.layMain = QVBoxLayout()
		self.wdtMain = QWidget()
		self.wdtMain.setLayout(self.layMain)
#		self.setLayout()
		
#		swtSmallAbove = QSwitch("QSwitch-Small, label above", SwitchSize.Small, SwitchLabelPos.Above)
#		
#		swtSmallBelow = QSwitch("QSwitch-Medium, label below", SwitchSize.Medium, SwitchLabelPos.Below)
#		swtSmallBefore = QSwitch("QSwitch-Large, label leading", SwitchSize.Large, SwitchLabelPos.Leading)
#		swtSmallAfter = QSwitch("QSwitch-Small, label trailing", SwitchSize.Small, SwitchLabelPos.Trailing)

		self.lblDesc = QLabel(f"This is a rought demo of the usage of QTextEditHEXSplitter\nwith a mixed matrix of its options")
		self.layMain.addWidget(self.lblDesc)
		
		self.splitter = QTextEditHEXSplitter()
		
		self.layMain.addWidget(self.splitter)
		
		self.setCentralWidget(self.wdtMain)
#		self.setBaseSize(WINDOW_SIZE * 2, WINDOW_SIZE)		
#		self._createMenuBar()
#		self._createToolBars()
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
#	w = QSwitch("HELLO QSwitch", SwitchSize.Small)
#	w.show()
	win = QTextEditHEXSplitterWindow()
	win.show()
	sys.exit(app.exec())