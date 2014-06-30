# -*- coding: utf-8 -*- 
'''
@author:       cherry
@license:      GNU General Public License 2.0 or later
@contact:      chery.wb@gmail.com
'''
from PySide import QtCore, QtGui
from PySide.QtGui import QApplication
from PySide.QtGui import QMainWindow 
import sys,os
import random
import numpy as np
import matplotlib.pyplot as plt

 

historydata = [] #期号/snum 时间/time 红号1/r1 红号2/r2 红号3/r3 红号4/r4 红号5/r5 红号/r6 蓝号/b1 currentblacklsit 候选集合 命中分析 邻号 二组邻号 三组邻号 二组重号 三组重号 三组连号
datakeys = ['currentwhitelist','currentblacklist','sublist','addlist','continuenum','neighbor','twoneighbor','threeneighbor','tworepeat','threerepeat','threecontinuenum','randomsel']
mykey = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,4,2,1,1,7,0,6,7,9]

#----------------------------------------------------------------------
def constructhistory(linedata):
    """
    根据历史分析构造 黑名单 白名单 重号 邻号 等候选号码组
    """
    linedata = str(linedata).split(" ")
    redballs = []
    neighbor = []
    threeneighbor = []
    twoneighbor = []
    tworepeat =[]
    threerepeat= []
    continuenum = []
    currentblacklist = []
    currentwhitelist = []
    randomsel = []
    for i in range(2,8):
	redballs.append(int(linedata[i]))
	lower = 1
	higher = 33
	if int(linedata[i]) != 1:
	    lower = int(linedata[i]) - 1
	else:
	    lower = 33
    
	if int(linedata[i]) != 33:
	    higher = int(linedata[i]) + 1
	else:
	    higher = 1
	if lower not in neighbor:
	    neighbor.append(lower)
	if higher not in neighbor:
	    neighbor.append(higher)
	neighbor.sort()
	
    for i in range(2,7):
	if (int(linedata[i+1]) - int(linedata[i])) == 1:
	    continuenum.append(int(linedata[i+1]))
	    if int(linedata[i]) not in continuenum:
		continuenum.append(int(linedata[i]))
	
    hlen = len(historydata)
    if hlen == 0:
	threeneighbor = neighbor[:]
	twoneighbor = neighbor[:]
	tworepeat = redballs[:]
	threerepeat = redballs[:]
	threecontinuenum = continuenum[:]
	currentblacklist = []
	currentwhitelist = []
    elif hlen == 1:
	twoneighbor= list(set(historydata[hlen-1]['neighbor']).union(set(neighbor)))
	threeneighbor = twoneighbor[:]
	tworepeat = list(set(historydata[hlen-1]['redballs']).union(set(redballs)))
	threerepeat = tworepeat[:]
	threecontinuenum =  list(set(historydata[hlen-1]['continuenum']).union(set(continuenum)))
    elif hlen >= 2:
	twoneighbor = list(set(historydata[hlen-1]['neighbor']).union(set(neighbor)))
	threeneighbor = list(set(historydata[hlen-1]['neighbor']).union(set(historydata[hlen-2]['neighbor'])).union(set(neighbor)))
	tworepeat = list(set(historydata[hlen-1]['redballs']).union(set(redballs)))
	threerepeat = list(set(historydata[hlen-1]['redballs']).union(set(historydata[hlen-2]['redballs'])).union(set(redballs)))
	threecontinuenum =  list(set(historydata[hlen-1]['continuenum']).union(set(historydata[hlen-2]['continuenum'])).union(set(continuenum)))
    
	nextindex = 3;
	while True:
	    #if len(threecontinuenum) >= 10:
	    if len(threecontinuenum) >= 15:
		break;
	    if (hlen - nextindex) <= 0:
		break;
	    threecontinuenum =  list(set(historydata[hlen-nextindex]['continuenum']).union(set(threecontinuenum)))
	    nextindex +=1
	    
    if hlen >=4:
	currentblacklist = list(set(historydata[hlen-1]['redballs']).intersection(set(historydata[hlen-2]['redballs'])).union(set(currentblacklist)))
	#currentblacklist = list(set(historydata[hlen-1]['redballs']).intersection(set(historydata[hlen-3]['redballs'])).union(set(currentblacklist)))
	#currentblacklist = list(set(historydata[hlen-1]['redballs']).intersection(set(historydata[hlen-4]['redballs'])).union(set(currentblacklist)))
	currentblacklist = list(set(historydata[hlen-2]['redballs']).intersection(set(historydata[hlen-3]['redballs'])).union(set(currentblacklist)))
	#currentblacklist = list(set(historydata[hlen-2]['redballs']).intersection(set(historydata[hlen-4]['redballs'])).union(set(currentblacklist)))
	#currentblacklist = list(set(historydata[hlen-3]['redballs']).intersection(set(historydata[hlen-4]['redballs'])).union(set(currentblacklist)))
	currentblacklist = list(set(historydata[hlen-3]['redballs']).intersection(set(historydata[hlen-4]['redballs'])).intersection(set(historydata[hlen-2]['redballs'])).intersection(set(historydata[hlen-1]['redballs'])).union(set(currentblacklist)))    
    
    if hlen >=5:
	for item in range(1,34):
	    if (item not in historydata[hlen-1]['redballs']) and (item not in historydata[hlen-2]['redballs']) and (item not in historydata[hlen-3]['redballs'])and (item not in historydata[hlen-4]['redballs'])and (item not in historydata[hlen-5]['redballs']):
		currentwhitelist.append(item)
    sublist = []
    addlist = []
    returnvalue = {'snum':linedata[0],'time':linedata[1],'r1':int(linedata[2]),'r2':int(linedata[3]),'r3':int(linedata[4]),'r4':int(linedata[5]),'r5':int(linedata[6]),'r6':int(linedata[7]),'b1':int(linedata[8]),'randomsel':randomsel,'currentwhitelist':currentwhitelist,'currentblacklist':currentblacklist,'redballs':redballs,'sublist':sublist,'addlist':addlist,'houxuan':[],'hit':0,'continuenum':continuenum,'neighbor':neighbor,'twoneighbor':twoneighbor,'threeneighbor':threeneighbor,'tworepeat':tworepeat,'threerepeat':threerepeat,'threecontinuenum':threecontinuenum}

    for j in range(6,1,-1):
	if(returnvalue['r%d' % j]>16) and (j > 2):
	    for k in range(j-1,0,-1):
		subres = returnvalue['r%d' % j] - returnvalue['r%d' % k]
		if subres not in sublist:
		    sublist.append(subres)
	    
    for j in range(6,1,-1):
	if (j > 2):
	    for k in range(j-1,0,-1):
		addres = ((returnvalue['r%d' % j] + returnvalue['r%d' % k]) % 33) +1
		if addres not in addlist:
		    addlist.append(addres)    
    returnvalue['addlist'] = addlist
    returnvalue['sublist'] = sublist
    
    #
    blueBalls = range(1, 34)
    blueBallRS = []
    ##先随机选五条，剔除后再重新选
    random.seed(hlen)
    for pre in range(2):
	choice = random.sample(blueBalls,6)
	blueBallRS.extend(choice)
    for selected in blueBallRS:
	for i in range(len(blueBalls)-1,0,-1):
	    if blueBalls[i] == selected:
		del blueBalls[i]
    randomsel = blueBalls[:]
    returnvalue['randomsel'] = randomsel
    
    return returnvalue

#读取文件 ssq.txt 初始化历史数据
f = open("ssq.TXT")
while True:
    line = f.readline()
    if not line: break
    structedline = constructhistory(line)
    historydata.append(structedline);

predictsnum = int(historydata[len(historydata)-1]['snum'])+1
predictdata = "%s 2003-02-23 01 01 01 01 01 01 01 01 01 01 01 01 01 0 0 0 0 0 0 0 0 0 0 0 0 0 0" % predictsnum  
structedline = constructhistory(predictdata)
historydata.append(structedline);
f.close()

##for item in historydata:
##    print item

blacklist = {}
whitelist = {}

#----------------------------------------------------------------------
def randomselect():
    """"""
    blueBallRS = []
    blueBalls, redBalls = range(1, 34), range(1, 17)
    results=[]
    ##先随机选五条，剔除后再重新选
    for pre in range(5):
	for i in range(6):
	    choice = random.choice(blueBalls)
	    blueBallRS.append(choice)
    ##        blueBalls.remove(choice)
    
    for selected in blueBallRS:
	for i in range(len(blueBalls)-1,0,-1):
	    if blueBalls[i] == selected:
		del blueBalls[i]
##    print "========================================="
##    print blueBalls
##    print "========================================="
    
    for stocks in range(4):
	blueBallRS=[]
	blueBalls4Sel = blueBalls[:]
	for i in range(6):
	    choice = random.choice(blueBalls4Sel)
	    blueBallRS.append(choice)
	    blueBalls4Sel.remove(choice)
	blueBallRS.sort()
	redBallRS = random.choice(redBalls)
	tempres = []
	tempres.append(blueBallRS[:])
	tempres.append(redBallRS)
	results.append(tempres[:])
##	print blueBallRS, ':', redBallRS
    return results
    

class mainUI(QtGui.QMainWindow):  
    def __init__(self, parent=None): 
	from PySide import QtCore, QtGui
	from ui.Ui_mainWidget import Ui_mainWidget
	
	QtGui.QMainWindow.__init__(self)
	self.QtGui=QtGui
	self.ui = Ui_mainWidget()
	self.ui.setupUi(self)   
	self.ui.pBcontinueAnalysis.clicked.connect(self.pBcontinueAnalysis)
	
	self.ui.pBneighborAnalysis.clicked.connect(self.pBneighborAnalysis)
	self.ui.pB2neighborAnalysis.clicked.connect(self.pB2neighborAnalysis)
	self.ui.pB2repeatAnalysis.clicked.connect(self.pB2repeatAnalysis)
	self.ui.pB3neighborAnalysis.clicked.connect(self.pB3neighborAnalysis)
	self.ui.pB3repeatAnalysis.clicked.connect(self.pB3repeatAnalysis)
	self.ui.pBneighborAnd2repeat.clicked.connect(self.pBneighborAnd2repeat)
	self.ui.pBnot2repeatAnalysis.clicked.connect(self.pBnot2repeatAnalysis)
	self.ui.pBnot3repeatAnalysis.clicked.connect(self.pBnot3repeatAnalysis)
	self.ui.pB3NSub2RAndC.clicked.connect(self.pB3NSub2RAndC)
	self.ui.pB3NSubC.clicked.connect(self.pB3NSubC)
	
	self.ui.tableWidget_history.setSortingEnabled(False)
	#设置下拉框
	for datakey in datakeys:
	    self.ui.comboBox_keyname.addItem(str(datakey))
	
	self.ui.pB_allin.clicked.connect(self.pB_allin)
	self.ui.pB_allnotin.clicked.connect(self.pB_allnotin)
	
	self.header_labels = [u"期号", u"红1", u"红2", u"红3", u"红4", u"红5", u"红6", u"蓝",u"候选集合",u"命中分析", u"本组邻号",u"二组邻号",u"三组邻号",u"二组重号", u"三组重号", u"三组连号" , u"黑名单", u"白名单", u"差值集合" , u"和值集合", u'随机选号']
	self.ui.tableWidget_history.clear()
	self.ui.tableWidget_history.setColumnCount(len(self.header_labels))
	self.ui.tableWidget_history.setHorizontalHeaderLabels(self.header_labels)
	self.ui.tableWidget_history.setSelectionMode(self.QtGui.QAbstractItemView.MultiSelection)
	self.ui.tableWidget_history.resizeColumnsToContents()
	self.ui.tableWidget_history.verticalHeader().setVisible(True)
	self.ui.tableWidget_history.setSortingEnabled(True)        
	self.fillTableData()
    
        self.center()
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0,0,screen.width(), screen.height())
	
    #----------------------------------------------------------------------
    def pB_allin(self):
	""""""
	self.clearTableData()
	print "start pB_allin..."
	lucky_key = int(self.ui.spinBox_luckykey.text())
	datakey = self.ui.comboBox_keyname.currentText()
	hittimes = 6
	if(int(self.ui.spinBox_hittimes.text())>=0):
	    hittimes = int(self.ui.spinBox_hittimes.text())   
	    
	keepsize = 33
	if(int(self.ui.lineEdit_keepsize.text())>6):
	    keepsize = int(self.ui.lineEdit_keepsize.text())
	hlen = len(historydata)-1
	if datakey == 'randomsel':
	    hlen = len(historydata)
	for i in range(1, hlen):
	    if datakey == 'randomsel':	
		historydata[i]['houxuan'] =  historydata[i-1][datakey][:]
	    else:
		historydata[i]['houxuan'] =  historydata[i][datakey][:]
		
	    if len(historydata[i]['houxuan']) > 0:
		for index in mykey:
		    lastnum = historydata[i]['houxuan'].pop()
		    historydata[i]['houxuan'].insert(index % len(historydata[i]['houxuan']),lastnum)
	    counter = 0
	    while True:
		if(len(historydata[i]['houxuan'])<= keepsize ):
		    break;
		#轮转
		historydata[i]['houxuan'].pop(mykey[counter % len(mykey)] % keepsize)
		lastnum = historydata[i]['houxuan'].pop()
		historydata[i]['houxuan'].insert((mykey[counter % len(mykey)]+lucky_key) % keepsize,lastnum)
		counter += 1	
		
	hitcounter = 0
	for i in range(1,len(historydata)-1):
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i]['houxuan'])))
	    if len(intersectiondata) >= hittimes:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB_allin.text())
	print "end pB_allin..."				
    #----------------------------------------------------------------------
    def pB_allnotin(self):
	""""""
	allballs = range(1,34)
	datakey = self.ui.comboBox_keyname.currentText()
	self.clearTableData()
	hittimes = 6
	if(int(self.ui.spinBox_hittimes.text())>=0):
	    hittimes = int(self.ui.spinBox_hittimes.text())	
	print "start pB_allnotin..."
	lucky_key = int(self.ui.spinBox_luckykey.text())
	keepsize = 33
	if(int(self.ui.lineEdit_keepsize.text())>6):
	    keepsize = int(self.ui.lineEdit_keepsize.text())
	hlen = len(historydata)-1
	if datakey == 'randomsel':
	    hlen = len(historydata)
	for i in range(1, hlen):
	    if datakey == 'randomsel':
		historydata[i]['houxuan'] = list(set(allballs).difference(set(historydata[i][datakey])))
	    else:
		historydata[i]['houxuan'] = list(set(allballs).difference(set(historydata[i-1][datakey])))
	    if len(historydata[i]['houxuan']) > 0:
		for index in mykey:
		    lastnum = historydata[i]['houxuan'].pop()
		    historydata[i]['houxuan'].insert(index % len(historydata[i]['houxuan']),lastnum)
	    counter = 0
	    while True:
		if(len(historydata[i]['houxuan'])<= keepsize ):
		    break;
		#轮转
		historydata[i]['houxuan'].pop(mykey[counter % len(mykey)] % keepsize)
		lastnum = historydata[i]['houxuan'].pop()
		historydata[i]['houxuan'].insert((mykey[counter % len(mykey)]+lucky_key) % keepsize,lastnum)
		counter += 1
		
	hitcounter = 0
	for i in range(1,len(historydata)-1):
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i]['houxuan'])))
	    if len(intersectiondata) >= hittimes:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
##	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i-1][datakey])))
##	    if len(intersectiondata) == (6-hittimes):
##		historydata[i]['hit'] = 1
##		hitcounter+=1
##	    else:
##		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB_allnotin.text())
	
	print "end pB_allnotin..."	
    #----------------------------------------------------------------------
    def pB3NSubC(self):
	""""""
	self.clearTableData()
	print "start pB2NSubC..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['neighbor'] 的子集，如果是表示命中
	    #list(set(b).difference(set(a))) # b中有而a中没有的 
	    #threeneighbor  - threecontinuenum
	    historydata[i]['houxuan'] = list(set(historydata[i-1]['threeneighbor']).difference(historydata[i-1]['threecontinuenum']))
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB3NSubC.text())
	print "end pB2NSubC..."			
    #----------------------------------------------------------------------
    def pB3NSub2RAndC(self):
	""""""
	self.clearTableData()
	print "start pB3NSub2RAndC..."
	hitcounter = 0
	hittimes = 6
	keepsize = 16
	lucky_key = int(self.ui.spinBox_luckykey.text())
	if(int(self.ui.lineEdit_keepsize.text())>6):
	    keepsize = int(self.ui.lineEdit_keepsize.text())
	if(int(self.ui.spinBox_hittimes.text())>=0):
	    hittimes = int(self.ui.spinBox_hittimes.text())   
	allballs = range(1,34)
	thetrustedballs = [4,7,11,13,17,24,26,27]
	#thetrustedballs = []
	_blacklist = []
	_whitelist = []
	_luckylist = []
	if len(self.ui.lineEdit_whitelist.text()) > 1:
	    _whitelist = self.ui.lineEdit_whitelist.text().split(" ")
	    if len(_whitelist) >0 :
		_whitelist = map(int,_whitelist)
	if len(self.ui.lineEdit_blacklist.text()) > 1:
	    _blacklist = self.ui.lineEdit_blacklist.text().split(" ")
	    if len(_blacklist) >0 :	
		_blacklist = map(int,_blacklist)
	if len(self.ui.lineEdit_lucky.text()) > 1:
	    _luckylist = self.ui.lineEdit_lucky.text().split(" ")
	    if len(_luckylist) >0 :
		_luckylist = map(int,_luckylist)
	
	for i in range(6,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['neighbor'] 的子集，如果是表示命中
	    #list(set(b).difference(set(a))) # b中有而a中没有的 
	    #threeneighbor - tworepeat + threecontinuenum #difference(historydata[i-4]['tworepeat']).union(historydata[i-2]['redballs']).union(historydata[i-1]['redballs']).union(historydata[i-3]['redballs']).
	    
	    if mykey[i % len(mykey)] % 7 == 0:
		historydata[i]['houxuan'] = list(set(historydata[i-1]['threeneighbor']).union(set(thetrustedballs)).difference(set(_blacklist)).union(historydata[i-3]['threecontinuenum']).union(historydata[i-2]['redballs']).union(set(allballs).difference(historydata[i-2]['threerepeat'])).difference(set(historydata[i-1]['sublist'])).union(set(_luckylist)).union(set(_whitelist))) #.union(historydata[i]['currentwhitelist']).difference(historydata[i]['currentblacklist'])
	    else:
		historydata[i]['houxuan'] = list(set(historydata[i-1]['threeneighbor']).union(set(thetrustedballs)).difference(set(_blacklist)).union(historydata[i-3]['threecontinuenum']).union(historydata[i-2]['redballs']).union(set(allballs).difference(historydata[i-2]['threerepeat'])).difference(set(historydata[i-1]['sublist'])).union(set(_luckylist)).union(set(_whitelist)))#.union(historydata[i]['currentwhitelist']).difference(historydata[i]['currentblacklist'])
	    #打乱
	    if(len(historydata[i]['houxuan'])>=15):
		for index in mykey:
		    lastnum = historydata[i]['houxuan'].pop()
		    historydata[i]['houxuan'].insert(index,lastnum)
	    
##	    mykey = [1,1,1,2,6,2]
##	    mypos = [2,5,4,1,6,3]
##	    counter = 0
##	    while True:
##		if(len(historydata[i]['houxuan'])<=keepsize) or (counter > 5):
##		    break;
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[0]]['r%d' % mykey[0]]]))
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[1]]['r%d' % mykey[1]]]))
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[2]]['r%d' % mykey[2]]]))
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[3]]['r%d' % mykey[3]]]))
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[4]]['r%d' % mykey[4]]]))
##		historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference([historydata[i-mypos[5]]['r%d' % mykey[5]]]))
##		counter += 1
##		#轮转
##		lastnum = mypos.pop()
##		mypos.insert(0,lastnum)
	    #################################################################	    
	  
	    counter = 0
	    while True:
		if(len(historydata[i]['houxuan'])<= keepsize ):
		    break;
		#轮转
		historydata[i]['houxuan'].pop(mykey[counter % len(mykey)] % keepsize)
		#historydata[i]['houxuan'].pop(keepsize/2 -1)
		lastnum = historydata[i]['houxuan'].pop()
		historydata[i]['houxuan'].insert((mykey[counter % len(mykey)]+lucky_key) % keepsize,lastnum)
		counter += 1
	    #################################################################
	    #historydata[i]['houxuan'] =  historydata[i]['houxuan'][5:16]
	    '''
	    historydata[i]['houxuan'] = list(set(historydata[i]['houxuan']).difference(historydata[i]['currentblacklist']))
	    '''
	    
	    #issubsetcon	= False
	    #issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    #if issubsetcon:
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i]['houxuan'])))
	    if len(intersectiondata) >= hittimes:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB3NSub2RAndC.text())
	print "end pB3NSub2RAndC..."			
    #----------------------------------------------------------------------
    def pBneighborAnalysis(self):
	""""""
	self.clearTableData()
	print "start pBneighborAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['neighbor'] 的子集，如果是表示命中
	    historydata[i]['houxuan'] = historydata[i-1]['neighbor'][:]
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pBneighborAnalysis.text())
	print "end pBneighborAnalysis..."		
    #----------------------------------------------------------------------
    def pB2neighborAnalysis(self):
	""""""
	self.clearTableData()
	print "start pB2neighborAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['twoneighbor'] 的子集，如果是表示命中
	    historydata[i]['houxuan'] = historydata[i-1]['twoneighbor'][:]
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB2neighborAnalysis.text())
	##绘制图形展示分析结果
##	analysisresult = []
##	for item in historydata:
##	    analysisresult.append(item['hit'])
##	plt.figure(1)
##	plt.plot(range(0,len(analysisresult)),analysisresult,"b--",label="Result")
##	plt.show()
	
	print "end pB2neighborAnalysis..."	
    #----------------------------------------------------------------------
    def pB2repeatAnalysis(self):
	""""""
	self.clearTableData()
	print "start pB2repeatAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['tworepeat'] 的子集，如果是表示命中
	    historydata[i]['houxuan'] = historydata[i-1]['tworepeat'][:]
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:	    
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB2repeatAnalysis.text())
	
	print "end pB2repeatAnalysis..."	
    #----------------------------------------------------------------------
    def pBnot2repeatAnalysis(self):
	""""""
	self.clearTableData()
	print "start pBnot2repeatAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['tworepeat'] 无交集，如果是表示命中
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i-1]['tworepeat'])))
	    if len(intersectiondata) == 0:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pBnot2repeatAnalysis.text())
	print "end pBnot2repeatAnalysis..."	    		
    #----------------------------------------------------------------------
    def pB3neighborAnalysis(self):
	""""""
	self.clearTableData()
	print "start pB3neighborAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['threeneighbor'] 的子集，如果是表示命中
	    historydata[i]['houxuan'] = historydata[i-1]['threeneighbor'][:]
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:	    
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0	    
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB3neighborAnalysis.text())
	print "end pB3neighborAnalysis..."
    #----------------------------------------------------------------------
    def pBnot3repeatAnalysis(self):
	""""""
	self.clearTableData()
	print "start pBnot3repeatAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['threerepeat'] 无交集，如果是表示命中
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i-1]['threerepeat'])))
	    if len(intersectiondata) == 0:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pBnot3repeatAnalysis.text())
	print "end pBnot3repeatAnalysis..."	    	
    #----------------------------------------------------------------------
    def pB3repeatAnalysis(self):
	""""""
	self.clearTableData()
	print "start pB3repeatAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)):
##	    historydata[i]['redballs'] 与 historydata[i-1]['threerepeat'] 的子集，如果是表示命中
	    historydata[i]['houxuan'] = historydata[i-1]['threerepeat'][:]
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:	    
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pB3repeatAnalysis.text())
	print "end pB3repeatAnalysis..."	    
    #----------------------------------------------------------------------
    def pBneighborAnd2repeat(self):
	""""""
	self.clearTableData()
	print "start pBneighborAnd2repeat..."
	hitcounter = 0
	for i in range(1,len(historydata)-1):
##	    historydata[i]['redballs'] 与 (historydata[i-1]['tworepeat'] 并集 historydata[i-1]['neighbor']) 的子集，如果是表示命中
	    historydata[i]['houxuan'] = list(set(historydata[i-1]['tworepeat']).union(historydata[i-1]['neighbor']))
	    issubsetcon	= False
	    issubsetcon = set(historydata[i]['redballs']).issubset(set(historydata[i]['houxuan']))
	    if issubsetcon:	    
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pBneighborAnd2repeat.text())
	print "end pBneighborAnd2repeat..."	
    #----------------------------------------------------------------------
    def pBcontinueAnalysis(self):
	""""""
	self.clearTableData()
	print "start pBcontinueAnalysis..."
	hitcounter = 0
	for i in range(1,len(historydata)-1):
	    historydata[i-1]['houxuan'] = []
##	    historydata[i]['redballs'] 与 historydata[i-1]['threecontinuenum'] 的交集，如果为空表示命中
	    intersectiondata = list(set(historydata[i]['redballs']).intersection(set(historydata[i-1]['addlist'])))
	    if len(intersectiondata) == 0:
		historydata[i]['hit'] = 1
		hitcounter+=1
	    else:
		historydata[i]['hit'] = 0
	self.fillTableData()
	self.ui.successpercent.setText(str((hitcounter*1.0)/len(historydata)))
	self.ui.analysismethod.setText(self.ui.pBcontinueAnalysis.text())
	##绘制图形展示分析结果
##	analysisresult = []
##	for item in historydata:
##	    analysisresult.append(item['hit'])
##	plt.figure(1) # 创建图表1
##	plt.plot(range(0,len(analysisresult)),analysisresult,"b--",label="Result")
##	plt.show()
	
	print "end pBcontinueAnalysis..."

    def fillTableData(self):
	for item in historydata:
	    self.ui.tableWidget_history.insertRow(self.ui.tableWidget_history.rowCount())
	    tmp_item = self.QtGui.QTableWidgetItem(item['snum'])
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 0, tmp_item) 
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r1']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 1, tmp_item) 
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r2']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 2, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r3']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 3, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r4']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 4, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r5']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 5, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['r6']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 6, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['b1']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 7, tmp_item)
	    item['houxuan'].sort()
	    tmp_item = self.QtGui.QTableWidgetItem("%s:%d" % (str(item['houxuan']),len(item['houxuan'])))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 8, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['hit']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 9, tmp_item)	     
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['neighbor']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 10, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['twoneighbor']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 11, tmp_item)	    
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['threeneighbor']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 12, tmp_item)	    
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['tworepeat']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 13, tmp_item)	    
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['threerepeat']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 14, tmp_item)	
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['threecontinuenum']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 15, tmp_item)
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['currentblacklist']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 16, tmp_item)	
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['currentwhitelist']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 17, tmp_item)	
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['sublist']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 18, tmp_item)	
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['addlist']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 19, tmp_item)	  	    
	    tmp_item = self.QtGui.QTableWidgetItem(str(item['randomsel']))
	    self.ui.tableWidget_history.setItem(self.ui.tableWidget_history.rowCount()-1, 20, tmp_item)
	    #currentblacklist threecontinuenum
	self.ui.tableWidget_history.resizeColumnsToContents()

    def clearTableData(self):
	self.ui.tableWidget_history.clear()
	self.ui.tableWidget_history.setRowCount(0)
	self.ui.tableWidget_history.clear()
	self.ui.tableWidget_history.setColumnCount(len(self.header_labels))
	self.ui.tableWidget_history.setHorizontalHeaderLabels(self.header_labels)   	

if __name__ == '__main__':  
##    randomselected = randomselect()
##    print randomselected
    app = QApplication(sys.argv)  
    mainWnd = mainUI()
    mainWnd.show()  
    app.exec_() 