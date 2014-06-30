#coding:utf-8
from PySide import QtCore,QtGui
from mainwindow_ui import Ui_MainWindow

import sys
import random
import time
import sip
import os
import codecs
import chardet
import xlwt

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

sys.setdefaultencoding(default_encoding)

choices=[u"分两组",u"分四组",u"两两分组",u"分任意组",u"N选1"]
class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.windowWidth=540
        self.windowHeight=450
        self.ui=Ui_MainWindow()
        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()
        self.ui.setupUi(self)
        self.initUI()
        self.setMouseTracking(True)
        self.setWindowIcon(QtGui.QIcon("./icon.png"))


        self.userRange=[]
        self.userNameImported=False
        self.teamNum=2
        self.result=[]
        self.singleTeam=[]

        self.bindBtn()
        self.__setStatusTip()
        self.ui.comboBox.addItems(choices)
        self.ui.lineEdit.setText(u"8")
    def bindBtn(self):
        self.ui.btnClear.clicked.connect(self.clearOutput)
        self.ui.btnExport.clicked.connect(self.onExportClicked)
        self.ui.btnImportUserName.clicked.connect(self.importUserName)
        self.ui.btnSplice.clicked.connect(self.splice)
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.comboBox.currentIndexChanged.connect(self.indexChanged)
    def __setStatusTip(self):
        self.ui.btnClear.setStatusTip(u"清空当前显示区内容，清空导入的选手姓名")
        self.ui.btnSplice.setStatusTip(u"导入选手姓名或设置选手人数后，点击将按分组数据进行随机分组")
        self.ui.btnExport.setStatusTip(u"输出当前显示区数据，方便编辑或打印")
        self.ui.btnImportUserName.setStatusTip(u"导入选手姓名，姓名文件每行一个名字")
        self.ui.comboBox.setStatusTip(u"选择分组方式")
        self.ui.btnClose.setStatusTip(u"退出程序")


    def clearOutput(self):
        self.ui.textEdit.setText(u"")
        self.ui.lineEdit.setText(u"")
        self.userRange=[]
        self.userNameImported=False
        self.ui.statusbar.clearMessage()
        self.result=self.singleTeam=[]

    def exportResult(self,tipe):
        fd=QtGui.QFileDialog(self)
        fd.move(self.x(),self.y())
        outputFile=fd.getSaveFileName(None,u"保存结果","./",
                        ("Text Files(*.txt);;Excel Files(*.xls)"))[0]
        if not outputFile:return
        tipe=outputFile.split(".")[-1]
        if tipe=="txt":
            result=self.ui.textEdit.toPlainText()
            f=open(outputFile,"a")
            f.write(result)
            f.close()
        elif tipe=="xls":
            for i in range(len(self.result)):
                self.result[i]=sorted(self.result[i])
                for j in range(len(self.result[i])):
                    if isinstance(self.result[i][j],int):
                        self.result[i][j]=u"%s 号"%(self.result[i][j]+1)
                self.result[i].insert(0,u"%s组"%chr(65+i))
            if self.singleTeam:
                self.singleTeam=sorted(self.singleTeam)
                for i in range(len(self.singleTeam)):
                    if isinstance(self.singleTeam[i],int):
                        self.singleTeam[i]=u"%s 号"%(self.singleTeam[i]+1)
                self.singleTeam.insert(0,
                            u"%s组(可作为独立组抽出)"%chr(65+len(self.result)))
                self.result.append(self.singleTeam)
            wk=xlwt.Workbook()
            ws=wk.add_sheet("RandomTeam")
            for i in range(len(self.result)):
                for j in range(len(self.result[i])):
                    ws.write(j,i,self.result[i][j])
            wk.save(outputFile)

        self.alert(u"保存成功！\n请查看%s."%outputFile)
        return outputFile
    def onExportClicked(self):
        self.exportResult("xls")
    def indexChanged(self):
        cbIndex=self.ui.comboBox.currentIndex()
        if cbIndex==0:
            teamNum=2
        elif cbIndex==1:
            teamNum=4
        elif cbIndex==2:
            teamNum=-2
        elif cbIndex==3:
            num,ok=QtGui.QInputDialog(self).getInt(self,u"选择分组数",
                                                u"请选择或输入分组数",
                                                value=3,min=1,max=65532,step=1)
            if num and ok:
                teamNum=num
            else:
                teamNum=0
        elif cbIndex==4:
            teamNum=-1
        try:
            teamNum_=int(teamNum)
        except:
            teamNum_=0
        self.teamNum=teamNum_
    def splice(self):
        self.result=[]
        self.singleTeam=[]
        if self.userNameImported:
            allpeople=self.userRange
        else:
            allpeople=self.getPeopleNum()
            if not allpeople:
                self.alert(u"请输入总参赛人数或者导入参赛选手的姓名！")
                return
            allpeople=range(allpeople)
        self.__splice(allpeople,self.teamNum)
    def __splice(self,peopleList,teamNum=2):
        outlist=[]
        residueSplice=[]
        listLength=len(peopleList)
        if teamNum>0 :
            residue=listLength%teamNum
            spliceLength=listLength/teamNum
        elif teamNum==-2:
            residue=listLength%2
            spliceLength=2
        elif teamNum==-1:
            outlist=random.sample(peopleList,1)
            self.displayResult([outlist],teamNum)
            return
        if residue>0 :
            residueSplice=random.sample(peopleList,residue)
        if residueSplice:
            outlist.append(residueSplice)
        peopleList=list(set(peopleList)-set(residueSplice))
        outlist=self.cutList(peopleList,spliceLength,outlist)
        self.displayResult(outlist,teamNum)


    def cutList(self,lst,spliceLength,outlist):
        try:
            splice=random.sample(lst,spliceLength)
        except:
            outlist=[]
            return outlist
        else:
            outlist.append(splice)
            lst=list(set(lst)-set(splice))
            if lst:
                self.cutList(lst,spliceLength,outlist)
            return outlist
    def displayResult(self,resultList_,teamNum):
        resultList=[]
        if len(resultList_)!=teamNum and teamNum>0:
            if len(resultList_[0])>=len(resultList_):
                resultList=resultList_
            else:
                for i in range(len(resultList_[0])):
                    resultList_[i+1].append(resultList_[0][i])
                resultList=resultList_[1:]
        else:
            resultList=resultList_
        log=u"\n--------------------------------------------------\n"
        if teamNum==-1:
            log+=u"N选1"
        else:
            log+=u"分%s组"%(len(resultList))
        for i in range(len(resultList)):
            log+=u"\n第%s组： "%(i+1)
            for j in range(len(resultList[i])):
                if isinstance(resultList[i][j],int):
                    log+=u"%4s号 "%(resultList[i][j]+1)
                else:
                    log+=u"%9s"%resultList[i][j]
        if teamNum!=-1:
            if len(resultList_[0])!=len(resultList_[1]) :
                log+=u"\n亦可抽出 "
                for i in resultList_[0]:
                    if isinstance(i,int):
                        log+=u"%3s号 "%(i+1)
                    else:
                        log+=u"%8s"%i
                    self.singleTeam.append(i)
                log+="单独为一组，其余分组信息不变"
        now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        log+=u"\n生成时间：%s"%now
        self.ui.textEdit.append(log)
        self.result=resultList
        print self.result
        print self.singleTeam



    def importUserName(self):
        fd=QtGui.QFileDialog(self)
        fd.move(self.x(),self.y())
        importFileName=fd.getOpenFileName(None,u"导入选手姓名","./",
                    ("Text Files(*.txt;*.csv)"))[0]
        if not importFileName:return
        if not os.path.isfile(importFileName):
            self.alert(u"不是一个有效的文件！")
            return
        convertedFile=self.convertFileCoding(importFileName)
        #f=open(convertedFile,"r")
        f=codecs.open(convertedFile,"r","utf-8")
        for line in f.readlines():
            self.userRange.append(line.strip())
        f.close()
        self.alert(u"选手姓名导入成功！")
        os.remove(convertedFile)
        self.userNameImported=True
        self.ui.statusbar.showMessage(u"选手信息已导入")

    def initUI(self):
        self.animation=QtCore.QPropertyAnimation(self,"geometry")
        self.animation.setDuration(200)

        self.animation.setStartValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.animation.setEndValue(QtCore.QRect((self.dskWidth-self.windowWidth)/2,
                                                (self.dskHeight-self.windowHeight)/2,
                                                self.windowWidth,
                                                self.windowHeight))
        self.animation.start()
    def alert(self,msg,title=u"提示"):
        QtGui.QMessageBox.warning(self,title,msg)

    def getPeopleNum(self,errorTip=None):
        try:
            allpeople=int(self.ui.lineEdit.text())
        except ValueError:
            if not errorTip:
                errorTip=u"请在输入框中输入数字。"
            self.alert(errorTip)
            self.ui.lineEdit.setText(u"")
        else:
            return allpeople
    #-------not used------------------------------------------------------------
    def getFileEncoding(self,fileName):
        f=open(fileName,"r")
        l=f.readline(1024)
        encoding=chardet.detect(l)['encoding']
        f.close()
        return encoding
    def convertFileCoding(self,filename):
        fname=filename.split("/")[-1]
        inFile=open(filename,"r")
        outFile=codecs.open("utf8_%s"%fname,"w","utf-8")
        encoding=self.getFileEncoding(filename)
        outFile.write(unicode(inFile.read().decode(encoding,'ignore')))
        outFile.close()
        inFile.close()
        return "utf8_%s"%fname


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    mw=MainWindow()
    mw.show()
    sys.exit(app.exec_())
