# -*- coding: utf-8 -*- 
'''
@author:       cherry
@license:      GNU General Public License 2.0 or later
@contact:      chery.wb@gmail.com
'''
import sys,os
import random
import numpy as np

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication
from PySide.QtGui import QMainWindow 
from PySide.QtGui import QWidget, QVBoxLayout, QMessageBox

import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from matplotlib import animation
from matplotlib import pyplot as plt  

zhfont = matplotlib.font_manager.FontProperties(fname='%s/simsun.ttc' % (os.getcwd()))
#plt.xlabel(u"横坐标xlabel",fontproperties=zhfont)

#----------------------------------------------------------------------
def plot_animation_1():
    """"""
    # First set up the figure, the axis, and the plot element we want to animate  
    fig = plt.figure()  
    ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))  
    ax.set_xlabel(u"横坐标x",fontproperties=zhfont)
    line, = ax.plot([], [], lw=2)  
    # initialization function: plot the background of each frame  
    def init():  
        line.set_data([], [])  
        return line,  
    # animation function.  This is called sequentially  
    # note: i is framenumber  
    def animate(i):  
        x = np.linspace(0, 2, 1000)  
        y = np.sin(2 * np.pi * (x - 0.01 * i))  
        line.set_data(x, y)  
        return line,  
      
    # call the animator.  blit=True means only re-draw the parts that have changed.  
    anim = animation.FuncAnimation(fig, animate, init_func=init,  
                                   frames=200, interval=20, blit=True)  
      
    #anim.save('basic_animation.mp4', fps=30)  
      
    plt.show()  

#----------------------------------------------------------------------
def plot_animation_2():
    """"""
    fig = plt.figure()  
    axes1 = fig.add_subplot(111)  
    line, = axes1.plot(np.random.rand(10))  
      
    #因为update的参数是调用函数data_gen,所以第一个默认参数不能是framenum  
    def update(data):  
        line.set_ydata(data)  
        return line,  
    # 每次生成10个随机数据  
    def data_gen():  
        while True:  
            yield np.random.rand(10)  
      
    ani = animation.FuncAnimation(fig, update, data_gen, interval=2*1000)  
    plt.show()

class MatplotinPySide(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setLayout(QVBoxLayout())
        self.canvas = FigureCanvas(Figure())
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
#----------------------------------------------------------------------
def emmbedmatplotintopyside():
    """"""
    app = QApplication(sys.argv)
    m = MatplotinPySide()
    m.show()
    app.exec_()
    



class pyplotUI(QtGui.QMainWindow):  
    def __init__(self, parent=None): 
	from PySide import QtCore, QtGui
	from ui.Ui_plotWidget import Ui_plotWidget
	
	QtGui.QMainWindow.__init__(self)
	self.QtGui=QtGui
	self.ui = Ui_plotWidget()
	self.ui.setupUi(self)   
	
	self.setupCanvas()
	self.setupActions()
        self.center()
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0,0,screen.width(), screen.height())
    
    #----------------------------------------------------------------------
    def setupCanvas(self):
	""""""
	self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
	self.ui.plot_canvas.setLayout(QVBoxLayout())
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.plot_canvas)
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.ui.plot_canvas)
	
	self.ui.plot_canvas.layout().addWidget(self.mpl_toolbar)
	self.ui.plot_canvas.layout().addWidget(self.canvas)		
    #----------------------------------------------------------------------
    def setupActions(self):
	""""""
	self.ui.action_exit.triggered.connect(self.on_exit)
	self.ui.action_animation_1.triggered.connect(self.on_animation_1)
	self.ui.action_animation_2.triggered.connect(self.on_animation_2)
	
	self.ui.action_normalplot_1.triggered.connect(self.on_normalplot_1)
	self.ui.action_about.triggered.connect(self.on_about)
    #----------------------------------------------------------------------
    def on_exit(self):
	""""""
	sys.exit()
    
    #----------------------------------------------------------------------
    def on_about(self):
	""""""
	msg = """ A demo of using PySide with matplotlib:
         * Use the matplotlib navigation bar
         * Show or hide the grid
        """
	QMessageBox.about(self, "About", msg.strip())
	
    #----------------------------------------------------------------------
    def on_normalplot_1(self):
	""""""
        self.data = [1,2,3,4,5]
        x = range(len(self.data))
        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
        self.axes.grid(True)
        self.axes.bar(
            left=x, 
            height=self.data, 
            width=0.35, 
            align='center', 
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()	
    #----------------------------------------------------------------------
    def on_animation_1(self):
	""""""
	self.axes.clear()        
	self.axes.grid(True)
	self.axes.set_xlim(0, 2)
	self.axes.set_ylim(-2, 2)
	
	line, = self.axes.plot([], [], lw=2)  
	def init():  
	    line.set_data([], [])  
	    return line,  
	# animation function.  This is called sequentially  
	# note: i is framenumber  
	def animate(i):  
	    x = np.linspace(0, 2, 1000)  
	    y = np.sin(2 * np.pi * (x - 0.01 * i))  
	    line.set_data(x, y)  
	    return line,  
	  
	# call the animator.  blit=True means only re-draw the parts that have changed.  
	anim = animation.FuncAnimation(self.fig, animate, init_func=init,  
	                               frames=100, interval=20, repeat=False)
	
	#do this step first: sudo apt-get install libav-tools
	anim.save('%s/basic_animation.mp4' % (os.getcwd()), fps=30)  
	self.canvas.draw()
    #----------------------------------------------------------------------
    def on_animation_2(self):
	""""""
	
#----------------------------------------------------------------------
def main():
    """"""
    app = QApplication(sys.argv)
    m = pyplotUI()
    m.show()
    app.exec_()

if __name__ == '__main__':
    main()
    #plot_animation_1()
    #emmbedmatplotintopyside()