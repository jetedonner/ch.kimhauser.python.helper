#!/usr/bin/env python3

from enum import Enum

from PyQt6.QtGui import *
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtWidgets

class SwitchSize(Enum):
	Small = 1
	Medium = 2
	Large = 3
	

class SwitchPrivate(QObject):
	
	currentColor = QColor("blue")
	
	def __init__(self, q, parent=None):
		QObject.__init__(self, parent=parent)
		self.mPointer = q
		self.mPosition = 0.0
		self.mGradient = QLinearGradient()
		self.mGradient.setSpread(QGradient.Spread.PadSpread)
		
		self.animation = QPropertyAnimation(self)
		self.animation.setTargetObject(self)
		self.animation.setPropertyName(b'position')
		self.animation.setStartValue(0.0)
		self.animation.setEndValue(1.0)
		self.animation.setDuration(200)
		self.animation.setEasingCurve(QEasingCurve.Type.InOutExpo)
		
		self.animation.finished.connect(self.mPointer.update)
		
	@pyqtProperty(float)
	def position(self):
		return self.mPosition
	
	@position.setter
	def position(self, value):
		self.mPosition = value
		self.mPointer.update()
		
	def draw(self, painter):
		r = self.mPointer.rect()
		margin = (r.height()/10)
		self.shadow = self.mPointer.palette().color(QPalette.ColorRole.Dark)
		self.light = self.mPointer.palette().color(QPalette.ColorRole.Light)
		self.button = self.mPointer.palette().color(QPalette.ColorRole.Button)
		painter.setPen(Qt.PenStyle.NoPen)
#		painter.setPen(PyQt6.QtGui.NoPen)
		
		self.mGradient.setColorAt(0, self.currentColor.darker(30))
		self.mGradient.setColorAt(1, self.currentColor.darker(30))
		self.mGradient.setStart(0, r.height())
		self.mGradient.setFinalStop(0, 0)
		painter.setBrush(self.mGradient)
		painter.drawRoundedRect(r, r.height()/2, r.height()/2)
		
		self.mGradient.setColorAt(0, self.shadow.darker(40))
		self.mGradient.setColorAt(1, self.light.darker(60))
		self.mGradient.setStart(0, 0)
		self.mGradient.setFinalStop(0, r.height())
		painter.setBrush(self.mGradient)
		painter.drawRoundedRect(r.adjusted(int(margin), int(margin), int(-margin), int(-margin)), r.height()/2, r.height()/2)
		
		self.mGradient.setColorAt(0, self.button.lighter(80))
		self.mGradient.setColorAt(1, self.currentColor)
		
		painter.setBrush(self.mGradient)
		
		marginInner = margin + 2
		x = r.height()/2.0 + self.mPosition*(r.width()-r.height())
		painter.drawEllipse(QPointF(x, r.height()/2), (r.height()/2)-marginInner, (r.height()/2)-marginInner)
		
	@pyqtSlot(bool, name='animate')
	def animate(self, checked):
		if checked:
			self.currentColor = QColor("green")
		else:
			self.currentColor = QColor("blue")
			
		self.animation.setDirection(QPropertyAnimation.Direction.Forward if checked else QPropertyAnimation.Direction.Backward)
		self.animation.start()
		
		
class Switch(QAbstractButton):
	
	checked = pyqtSignal(bool)
	switchSize:SwitchSize = SwitchSize.Small
	
	def __init__(self, switchSize:SwitchSize = SwitchSize.Small, parent=None):
		QAbstractButton.__init__(self, parent=parent)
		self.dPtr = SwitchPrivate(self)
		self.switchSize = switchSize
		self.setCheckable(True)
		self.clicked.connect(self.dPtr.animate)
		self.clicked.connect(self.animate)
		
		fixedSize = QSize(48, 29)
		if self.switchSize == SwitchSize.Small:
			fixedSize = QSize(36, 21)
		elif self.switchSize == SwitchSize.Large:
			fixedSize = QSize(84, 42)
		self.setFixedSize(fixedSize)
#		self.setMaximumSize(QSize(36, 21))
	
	@pyqtSlot(bool) #, name='animate')
	def animate(self, checked):
		self.dPtr.animate(checked)
		self.checked.emit(checked)
		
	def setCheckedNG(self, checked):
		self.setChecked(checked)
		self.dPtr.animate(checked)
		
#	def sizeHint(self):
#		if self.switchSize == SwitchSize.Small:
#			return QSize(36, 21)
#		elif self.switchSize == SwitchSize.Medium:
#			return QSize(48, 29)
#		return QSize(84, 42)
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		self.dPtr.draw(painter)
		
	def resizeEvent(self, event):
		self.update()
		
class QSwitch(QWidget):
	
	checked = pyqtSignal(bool)
	switchSize:SwitchSize = SwitchSize.Small
	
	def __init__(self, descTxt:str, switchSize:SwitchSize = SwitchSize.Small, parent=None):
		QWidget.__init__(self, parent=parent)
		self.switch = Switch(switchSize)
		self.switch.checked.connect(self.checked_changed)
		self.switch.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.setLayout(QHBoxLayout())
		self.layout().addWidget(self.switch)
		self.lblDesc = QLabel(descTxt)
		self.lblDesc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.layout().addWidget(self.lblDesc)
		
	def setChecked(self, checked):
		self.switch.setCheckedNG(checked)
		
	@pyqtSlot(bool)
	def checked_changed(self, checked):
		self.checked.emit(checked)
		
class QSwitchDemoWindow(QMainWindow):
	"""PyMobiledevice3GUI's main window (GUI or view)."""
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QSwitch - Demo app v0.0.1")
		
		self.setLayout(QVBoxLayout())
		
		swtSmallAbove = QSwitch("QSwitch-Small, label above", SwitchSize.Small)
		swtSmallBelow = QSwitch("QSwitch-Medium, label below", SwitchSize.Medium)
		swtSmallBefore = QSwitch("QSwitch-Large, label before", SwitchSize.Large)
		swtSmallAfter = QSwitch("QSwitch-Small, label after", SwitchSize.Small)
		
		self.layout().addWidget(swtSmallAbove)
#		self.layout().addWidget(swtSmallBelow)

		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
#	w = QSwitch("HELLO QSwitch", SwitchSize.Large)
#	w.show()
	win = QSwitchDemoWindow()
	win.show()
	sys.exit(app.exec())