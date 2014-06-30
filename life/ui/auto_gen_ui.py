from PySide import QtCore
import sys, os
########################################################################
class WidgetsGenerator():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,uibasepath):
        """Constructor"""
        self.uibasepath = uibasepath

    #----------------------------------------------------------------------
    def genWidgets(self):
        """"""
##        Logger.getMainLogger().debug("start generate UI Widgets.");
        self.walk(self.uibasepath)
##        Logger.getMainLogger().debug("end generate UI Widgets.");
       
    def walk(self,path):
        import sys, os, optparse
        from pysideuic.driver import Driver
        from pysideuic.port_v2.invoke import invoke
            
        for item in os.listdir(path):
            itemsrc = os.path.join(path, item)
            if ".ui" in itemsrc: 
                optlist = {}
                optlist["debug"] = False
                optlist["preview"] = False
                optlist["execute"] = False
                optlist["from_imports"] = False
                optlist["indent"] = 4
                optlist["output"] = os.path.join(os.path.dirname(itemsrc),"Ui_"+os.path.basename(itemsrc).replace(".ui", ".py"))
                opts = optparse.Values(optlist)
                print itemsrc
                invoke(Driver(opts, itemsrc))

##pyside-uic main.ui -o Ui_mainWidget.py
if __name__ == '__main__':  
    worker = WidgetsGenerator(os.getcwd())
    worker.genWidgets()