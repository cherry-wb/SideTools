# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wb/workspace/pyside/Tools/life/ui/plotWidget.ui'
#
# Created: Mon Jun 30 17:08:57 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_plotWidget(object):
    def setupUi(self, plotWidget):
        plotWidget.setObjectName("plotWidget")
        plotWidget.resize(800, 600)
        self.centralwidget = QtGui.QWidget(plotWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot_canvas = QtGui.QWidget(self.centralwidget)
        self.plot_canvas.setObjectName("plot_canvas")
        self.verticalLayout.addWidget(self.plot_canvas)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        plotWidget.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(plotWidget)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtGui.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtGui.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        plotWidget.setMenuBar(self.menuBar)
        self.action_about = QtGui.QAction(plotWidget)
        self.action_about.setObjectName("action_about")
        self.action_animation_1 = QtGui.QAction(plotWidget)
        self.action_animation_1.setObjectName("action_animation_1")
        self.action_animation_2 = QtGui.QAction(plotWidget)
        self.action_animation_2.setObjectName("action_animation_2")
        self.action_exit = QtGui.QAction(plotWidget)
        self.action_exit.setObjectName("action_exit")
        self.action_normalplot_1 = QtGui.QAction(plotWidget)
        self.action_normalplot_1.setObjectName("action_normalplot_1")
        self.menu.addAction(self.action_exit)
        self.menu_2.addAction(self.action_animation_1)
        self.menu_2.addAction(self.action_animation_2)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_normalplot_1)
        self.menu_3.addAction(self.action_about)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())

        self.retranslateUi(plotWidget)
        QtCore.QMetaObject.connectSlotsByName(plotWidget)

    def retranslateUi(self, plotWidget):
        plotWidget.setWindowTitle(QtGui.QApplication.translate("plotWidget", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("plotWidget", "系统", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("plotWidget", "绘图", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_3.setTitle(QtGui.QApplication.translate("plotWidget", "帮助", None, QtGui.QApplication.UnicodeUTF8))
        self.action_about.setText(QtGui.QApplication.translate("plotWidget", "关于", None, QtGui.QApplication.UnicodeUTF8))
        self.action_animation_1.setText(QtGui.QApplication.translate("plotWidget", "动态图表(1)", None, QtGui.QApplication.UnicodeUTF8))
        self.action_animation_2.setText(QtGui.QApplication.translate("plotWidget", "动态图表(2)", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("plotWidget", "退出", None, QtGui.QApplication.UnicodeUTF8))
        self.action_normalplot_1.setText(QtGui.QApplication.translate("plotWidget", "普通绘图(1)", None, QtGui.QApplication.UnicodeUTF8))

