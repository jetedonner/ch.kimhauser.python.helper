#!/usr/bin/env python3

from PyQt6.QtCore import QObject, QSize, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSlot, Qt, pyqtSignal
from PyQt6.QtGui import  QPainter, QPalette, QLinearGradient, QGradient
from PyQt6.QtWidgets import QAbstractButton, QApplication, QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QColor

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
		margin = r.height()/10
		shadow = self.mPointer.palette().color(QPalette.ColorRole.Dark)
		light = self.mPointer.palette().color(QPalette.ColorRole.Light)
		button = self.mPointer.palette().color(QPalette.ColorRole.Button)
#		painter.setPen(PyQt6.QtGui.NoPen)
		
		self.mGradient.setColorAt(0, shadow.darker(30))
		self.mGradient.setColorAt(1, light.darker(30))
		self.mGradient.setStart(0, r.height())
		self.mGradient.setFinalStop(0, 0)
		painter.setBrush(self.mGradient)
		painter.drawRoundedRect(r, r.height()/2, r.height()/2)
		
		self.mGradient.setColorAt(0, self.currentColor.darker(40))
		self.mGradient.setColorAt(1, self.currentColor.darker(60))
		self.mGradient.setStart(0, 0)
		self.mGradient.setFinalStop(0, r.height())
		painter.setBrush(self.mGradient)
		painter.drawRoundedRect(r.adjusted(int(margin), int(margin), int(-margin), int(-margin)), r.height()/2, r.height()/2)
		
		self.mGradient.setColorAt(0, button.darker(30))
		self.mGradient.setColorAt(1, self.currentColor)
		
		painter.setBrush(self.mGradient)
		
		x = r.height()/2.0 + self.mPosition*(r.width()-r.height())
		painter.drawEllipse(QPointF(x, r.height()/2), r.height()/2-margin, r.height()/2-margin)
		
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
	
	def __init__(self, parent=None):
		QAbstractButton.__init__(self, parent=parent)
		self.dPtr = SwitchPrivate(self)
		self.setCheckable(True)
		self.clicked.connect(self.dPtr.animate)
		self.clicked.connect(self.animate)
		self.setMaximumSize(QSize(36, 21))
	
	@pyqtSlot(bool) #, name='animate')
	def animate(self, checked):
		self.dPtr.animate(checked)
		self.checked.emit(checked)
		
	def setCheckedNG(self, checked):
		self.setChecked(checked)
		self.dPtr.animate(checked)
		
	def sizeHint(self):
		return QSize(84, 42)
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		self.dPtr.draw(painter)
		
	def resizeEvent(self, event):
		self.update()
		
class QSwitch(QWidget):
	
	checked = pyqtSignal(bool)
	
	def __init__(self, descTxt:str, parent=None):
		QWidget.__init__(self, parent=parent)
		self.switch = Switch()
		self.switch.checked.connect(self.checked_changed)
		self.setLayout(QHBoxLayout())
		self.layout().addWidget(self.switch)
		self.lblDesc = QLabel(descTxt)
		self.layout().addWidget(self.lblDesc)
	
	def setChecked(self, checked):
		self.switch.setCheckedNG(checked)
		
	@pyqtSlot(bool)
	def checked_changed(self, checked):
		self.checked.emit(checked)		
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	w = Switch()
	w.show()
	sys.exit(app.exec())