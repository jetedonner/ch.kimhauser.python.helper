#!/usr/bin/env python3

import psutil
import os
import os.path
import sys
import sre_constants
import re
import binascii
import webbrowser
import ctypes
import time

from PyQt6.QtGui import *
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtWidgets

APP_NAME = "ConsoleTextEditWindow-TEST"
WINDOW_SIZE = 720

APP_VERSION = "v0.0.1"

class QConsoleTextEdit(QTextEdit):
	
#	Black: \u001b[30m
#	Red: \u001b[31m
#	Green: \u001b[32m
#	Yellow: \u001b[33m
#	Blue: \u001b[34m
#	Magenta: \u001b[35m
#	Cyan: \u001b[36m
#	White: \u001b[37m
#	Reset: \u001b[0m
	
	ansi_dict = {"\x1b[30m": "black", "\x1b[31m": "red", "\x1b[32m": "green", "\x1b[33m": "yellow", "\x1b[34m": "blue", "\x1b[35m": "magenta", "\x1b[36m": "cyan", "\x1b[37m": "white", "\x1b[0m": "white"}
	
	patternEscaped = re.compile(r"\x1b\[\d{1,}[m]")
	
	def __init__(self):
		super().__init__()
		self.setAcceptRichText(True)
		
	def setEscapedText(self, text):
		self.setHtml(self.formatText(text))
	
	def appendEscapedText(self, text):
		self.append(self.formatText(text))
		
	def formatText(self, text):
		text = text.replace("\r\n", "<br/>")
		text = text.replace("\n", "<br/>")
		ansi_colors = self.patternEscaped.finditer(text)
		formatedText = "<span color='white'>"
		currPos = 0
		for ansi_color in ansi_colors:
#			print(f"-> Single ansi_color: {ansi_color} ({ansi_color.start()} / {ansi_color.end()})")
			formatedText += text[currPos:(ansi_color.start())]
			formatedText += "</span><span style='color: " + self.ansi_dict[ansi_color.group(0)] + "'>"
			currPos = ansi_color.end()
		formatedText += text[currPos:]
		formatedText += "</span>"
		return formatedText
	
class QConsoleTextEditWindow(QMainWindow):
	
	mytext = "thread #1: tid = 0xa8f62d, 0x0000000100003f40 hello_world_test_loop`main, queue = \x1b[32m'com.apple.main-thread'\x1b[0m, stop reason = \x1b[31mbreakpoint 1.1\x1b[0m\nthread #2: tid = 0xa8f62d, 0x0000000100003f40 hello_world_test_loop`main, queue = \x1b[35m'com.apple.main-thread'\x1b[0m, stop reason = \x1b[36mbreakpoint 1.1\x1b[0m"
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle(APP_NAME + " " + APP_VERSION)
		self.setBaseSize(WINDOW_SIZE * 2, WINDOW_SIZE)
		self.setMinimumSize(WINDOW_SIZE * 2, WINDOW_SIZE + 72)
		
		self.layout = QHBoxLayout()
		
		self.centralWidget = QWidget(self)
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)
		self.txtConsole = QConsoleTextEdit()
		self.layout.addWidget(self.txtConsole)
		self.txtConsole.setEscapedText(self.mytext)
		self.txtConsole.appendEscapedText(self.mytext)
		
		

#def close_application():
#	pass
	
#global pymobiledevice3GUIApp
#pymobiledevice3GUIApp = QApplication([])
#pymobiledevice3GUIApp.aboutToQuit.connect(close_application)
#
#pymobiledevice3GUIWindow = QConsoleTextEditWindow()
#pymobiledevice3GUIWindow.show()
#
#sys.exit(pymobiledevice3GUIApp.exec())