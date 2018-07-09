# -*- coding: UTF-8 -*-   
#--------------------------------------------------------------------------
#
# ScriptName : Normal Translator Tool
# Contents   : UI for Normal changing/ Toolset
# Author	 : 则远霄汉Yiyang Chen
# Update	 : 2017/7/8
# Note	   : Credits to Charlie McKenna for helping me out
#			   
#--------------------------------------------------------------------------
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import PySide2 as QT
import maya.cmds as cmds
import maya.OpenMaya as om
import math



class mayaDockableWindow( MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow  ):
	def __init__(self, parent=None):
		super(mayaDockableWindow, self).__init__( 	parent)
		self.Xsign = 1
		self.Ysign = 1
		self.Zsign = 1
		self.VecOriginlist=[]
#		self.TargetVectorDic={'index':[]}
#		self.OriginVectorDic={'index':[]}
		self.savedsel = []
		self.vertexlimit = 200000
		self.stopfunction = False
		self.selectlive = True
		#Preset Values
		#self.PresetxyzData=[0,0,0,1,1,1,360,360,360,0,0,0]
		#MAIN WINDOWS need a central Widget...
		#We will create a blank Widget...
		self.wdgMain =								QT.QtWidgets.QWidget(self)
		self.setCentralWidget						(self.wdgMain)
		self.wdgToolfunction =						QT.QtWidgets.QWidget(self)
		self.wdgHardEdge =							QT.QtWidgets.QWidget(self)
		self.wdgTogNor = 							QT.QtWidgets.QWidget(self)
		self.wdgLineX =								QT.QtWidgets.QWidget(self)
		self.wdgLineY =								QT.QtWidgets.QWidget(self)
		self.wdgLineZ =								QT.QtWidgets.QWidget(self)
		self.wdgLineLerp =							QT.QtWidgets.QWidget(self)
		self.FuncLine1 =							QT.QtWidgets.QWidget(self)
		self.FuncLine2 =							QT.QtWidgets.QWidget(self)
		self.FuncLine3 =							QT.QtWidgets.QWidget(self)
		#ADD a Label

		self.TitleLabel = QT.QtWidgets.QLabel( "Normal Editing Tools", self )
		
		self.radioAddLabel = QT.QtWidgets.QLabel( "Add", self )
		self.radioMulLabel = QT.QtWidgets.QLabel( "Multiply", self )
		self.radioRotLabel = QT.QtWidgets.QLabel( "Rotate", self )
		self.radioRepLabel = QT.QtWidgets.QLabel( "Replace", self )
		self.radioAvgLabel = QT.QtWidgets.QLabel( "Average", self )
		self.radioSphLabel = QT.QtWidgets.QLabel( "Spherize", self )
		self.LerpLabel = QT.QtWidgets.QLabel( "Lerp", self )
		self.XLabel = QT.QtWidgets.QLabel( "X", self )
		self.YLabel = QT.QtWidgets.QLabel( "Y", self )
		self.ZLabel = QT.QtWidgets.QLabel( "Z", self )
		self.XLabel.setMaximumSize(12,24)
		self.YLabel.setMaximumSize(12,24)
		self.ZLabel.setMaximumSize(12,24)
		
		#Intensity slider
		self.SliderIntensity =								QT.QtWidgets.QSlider(QT.QtCore.Qt.Horizontal)
		self.SliderIntensity.setRange(0,200)
		self.SliderIntensity.setValue(200)
#		self.SliderIntensity.setSingleStep(0.01)
#		self.SliderIntensity.valueChanged.connect (self.checkSelection)
		self.SliderIntensity.valueChanged.connect (self.applyIntensity)
		
		#Spin Boxes 
		self.NormalAngle =   QT.QtWidgets.QDoubleSpinBox( self)
		self.NormalAngle.setRange  (0,180)
		self.NormalAngle.setSingleStep (0.1)
#		self.NormalAngle.setMinimumSize(90,24)
		
		self.ValueXfloat =   QT.QtWidgets.QDoubleSpinBox( self)
		self.ValueXfloat.setRange  (-10,10)
		self.ValueXfloat.setSingleStep (0.1)
		self.ValueXfloat.setMinimumSize(90,24)
		self.ValueXfloat.valueChanged.connect (self.applySpinbox)
		self.ValueXfloat.valueChanged.connect (self.applyIntensity)
#		self.ValueXfloat.setWhatsThis('Targeted X Relative Value')
#		self.ValueXfloat.valueChanged.connect (self.checksignx)
#		self.ValueXfloat.valueChanged.connect (self.togglesign)
#		self.ValueXfloat.valueChanged.connect (self.loadToolsetting)
		self.ValueYfloat =   QT.QtWidgets.QDoubleSpinBox( self)
		self.ValueYfloat.setRange  (-10,10)
		self.ValueYfloat.setSingleStep (0.1)
		self.ValueYfloat.setMinimumSize(90,24)
		self.ValueYfloat.valueChanged.connect (self.applySpinbox)
		self.ValueYfloat.valueChanged.connect (self.applyIntensity)
#		self.ValueYfloat.valueChanged.connect (self.checksigny)
#		self.ValueYfloat.valueChanged.connect (self.togglesign)
#		self.ValueYfloat.valueChanged.connect (self.loadToolsetting)
		self.ValueZfloat =   QT.QtWidgets.QDoubleSpinBox( self)
		self.ValueZfloat.setRange  (-10,10)
		self.ValueZfloat.setSingleStep (0.1)
		self.ValueZfloat.setMinimumSize(90,24)
		self.ValueZfloat.valueChanged.connect (self.applySpinbox)
		self.ValueZfloat.valueChanged.connect (self.applyIntensity)
#		self.ValueZfloat.valueChanged.connect (self.checksignz)
#		self.ValueZfloat.valueChanged.connect (self.togglesign)
#		self.ValueZfloat.valueChanged.connect (self.loadToolsetting)

		self.Toolfuncgrp = QT.QtWidgets.QButtonGroup( self)
		self.radioAdd = QT.QtWidgets.QRadioButton( self,1)
		self.radioMul = QT.QtWidgets.QRadioButton( self,2)
		self.radioRot = QT.QtWidgets.QRadioButton( self,3)
		self.radioRep = QT.QtWidgets.QRadioButton( self,4)
		self.radioAvg = QT.QtWidgets.QRadioButton( self,5)
		self.radioSph = QT.QtWidgets.QRadioButton( self,6)
		self.radioAdd.setChecked(1)
		self.Toolfuncgrp.addButton ( self.radioAdd)
		self.Toolfuncgrp.addButton ( self.radioMul)
		self.Toolfuncgrp.addButton ( self.radioRot)
		self.Toolfuncgrp.addButton ( self.radioRep)
		self.Toolfuncgrp.addButton ( self.radioAvg)
		self.Toolfuncgrp.addButton ( self.radioSph)
#		self.Toolfuncgrp.buttonClicked.connect(self.saveToolxyz)
		self.Toolfuncgrp.buttonClicked.connect(self.loadToolsetting)
#		self.Toolfuncgrp.buttonClicked.connect(self.loadToolxyz)
#		self.Toolfuncgrp.buttonClicked.connect(self.setoldTool)
		
		self.btnSelectlive =   QT.QtWidgets.QPushButton('Live On', self)
		self.btnSelectlive.released.connect (self.ToggleSelectlive)
		
		#Set to default value button
		self.btnDefault =   QT.QtWidgets.QPushButton('Default', self)
		self.btnDefault.released.connect (self.setdefaultvalue)
		
		#Template value button
		self.btnApply =   QT.QtWidgets.QPushButton('Apply', self)
		self.btnApply.released.connect (self.applyTool)
		
		self.btnNrmtoCol =   QT.QtWidgets.QPushButton('Nrm to Col', self)
		self.btnNrmtoCol.released.connect (self.convertNrmtoCol)
		
		self.btnColtoNrm =   QT.QtWidgets.QPushButton('Col to Nrm', self)
		self.btnColtoNrm.released.connect (self.convertColtoNrm)
		
		self.btnemptyCol =   QT.QtWidgets.QPushButton('Empty Col', self)
		self.btnemptyCol.released.connect (self.emptyCol)
		
		self.btnHardedge =   QT.QtWidgets.QPushButton('Hard Edges', self)
		self.btnHardedge.released.connect (self.HardedgeNormals)
		self.btnHardedgeset0 =   QT.QtWidgets.QPushButton('H', self)
		self.btnHardedgeset0.released.connect (self.Hardedgeset0)
		self.btnHardedgeset180 =   QT.QtWidgets.QPushButton('S', self)
		self.btnHardedgeset180.released.connect (self.Hardedgeset180)

		self.btnToggleNorShow =   QT.QtWidgets.QPushButton('Display', self)
		self.btnToggleNorShow.released.connect (self.ToggleNorShow)
		self.btnNorLenAdd =   QT.QtWidgets.QPushButton('+', self)
		self.btnNorLenAdd.released.connect (self.NorLenAdd)
		self.btnNorLenSub =   QT.QtWidgets.QPushButton('-', self)
		self.btnNorLenSub.released.connect (self.NorLenSub)

		self.btnOrigin =   QT.QtWidgets.QPushButton('Origin', self)
		self.btnOrigin.setMaximumSize(100,24)
		self.btnOrigin.setMinimumSize(60,24)
		self.btnOrigin.released.connect(self.applyIntensityOrigin)
		self.btnTarget =   QT.QtWidgets.QPushButton('Target', self)
		self.btnTarget.setMaximumSize(100,24)
		self.btnTarget.setMinimumSize(60,24)
		self.btnTarget.released.connect(self.applyIntensityTarget)
		
#		self.btnX0 =   QT.QtWidgets.QPushButton('X', self)
#		self.btnX0.released.connect (self.applyToolx0)
		self.btnX1 =   QT.QtWidgets.QPushButton('-', self)
		self.btnX1.setMaximumSize(50,24)
		self.btnX1.setMinimumSize(20,24)
		self.btnX1.released.connect (self.applyToolx1)
		self.btnX1.released.connect (self.togglesign)
		self.btnX2 =   QT.QtWidgets.QPushButton('0.15', self)
		self.btnX2.setMaximumSize(70,24)
		self.btnX2.setMinimumSize(40,24)
		self.btnX2.released.connect (self.applyToolx2)
		self.btnX3 =   QT.QtWidgets.QPushButton('0.5', self)
		self.btnX3.setMaximumSize(70,24)
		self.btnX3.setMinimumSize(40,24)
		self.btnX3.released.connect (self.applyToolx3)
		self.btnX4 =   QT.QtWidgets.QPushButton('1', self)
		self.btnX4.setMaximumSize(70,24)
		self.btnX4.setMinimumSize(40,24)
		self.btnX4.released.connect (self.applyToolx4)
		self.btnX5 =   QT.QtWidgets.QPushButton('Def', self)
		self.btnX5.setMaximumSize(60,24)
		self.btnX3.setMinimumSize(40,24)
		self.btnX5.released.connect (self.xdefault)
#		self.btnY0 =   QT.QtWidgets.QPushButton('Y', self)
#		self.btnY0.released.connect (self.applyTooly0)
		self.btnY1 =   QT.QtWidgets.QPushButton('-', self)
		self.btnY1.setMaximumSize(50,24)
		self.btnY1.setMinimumSize(20,24)
		self.btnY1.released.connect (self.applyTooly1)
		self.btnY1.released.connect (self.togglesign)
		self.btnY2 =   QT.QtWidgets.QPushButton('0.15', self)
		self.btnY2.setMaximumSize(70,24)
		self.btnY2.setMinimumSize(40,24)
		self.btnY2.released.connect (self.applyTooly2)
		self.btnY3 =   QT.QtWidgets.QPushButton('0.5', self)
		self.btnY3.setMaximumSize(70,24)
		self.btnY3.setMinimumSize(40,24)
		self.btnY3.released.connect (self.applyTooly3)
		self.btnY4 =   QT.QtWidgets.QPushButton('1', self)
		self.btnY4.setMaximumSize(70,24)
		self.btnY4.setMinimumSize(40,24)
		self.btnY4.released.connect (self.applyTooly4)
		self.btnY5 =   QT.QtWidgets.QPushButton('Def', self)
		self.btnY5.setMaximumSize(60,24)
		self.btnY3.setMinimumSize(40,24)
		self.btnY5.released.connect (self.ydefault)
#		self.btnZ0 =   QT.QtWidgets.QPushButton('Z', self)
#		self.btnZ0.released.connect (self.applyToolz0)
		self.btnZ1 =   QT.QtWidgets.QPushButton('-', self)
		self.btnZ1.setMaximumSize(50,24)
		self.btnZ1.setMinimumSize(20,24)
		self.btnZ1.released.connect (self.applyToolz1)
		self.btnZ1.released.connect (self.togglesign)
		self.btnZ2 =   QT.QtWidgets.QPushButton('0.15', self)
		self.btnZ2.setMaximumSize(70,24)
		self.btnZ2.setMinimumSize(40,24)
		self.btnZ2.released.connect (self.applyToolz2)
		self.btnZ3 =   QT.QtWidgets.QPushButton('0.5', self)
		self.btnZ3.setMaximumSize(70,24)
		self.btnZ3.setMinimumSize(40,24)
		self.btnZ3.released.connect (self.applyToolz3)
		self.btnZ4 =   QT.QtWidgets.QPushButton('1', self)
		self.btnZ4.setMaximumSize(70,24)
		self.btnZ4.setMinimumSize(40,24)
		self.btnZ4.released.connect (self.applyToolz4)
		self.btnZ5 =   QT.QtWidgets.QPushButton('Def', self)
		self.btnZ5.setMaximumSize(60,24)
		self.btnZ3.setMinimumSize(40,24)
		self.btnZ5.released.connect (self.zdefault)


		# layout for tool function radio group
		layToolfunction =	 QT.QtWidgets.QHBoxLayout(self.wdgToolfunction)
		layToolfunction.addWidget	(self.radioAdd)
		layToolfunction.addWidget	(self.radioAddLabel)
		layToolfunction.addStretch()
		layToolfunction.addWidget	(self.radioMul)
		layToolfunction.addWidget	(self.radioMulLabel)
		layToolfunction.addStretch()
		layToolfunction.addWidget	(self.radioRot)
		layToolfunction.addWidget	(self.radioRotLabel)
		layToolfunction.addStretch()
		layToolfunction.addWidget	(self.radioRep)
		layToolfunction.addWidget	(self.radioRepLabel)
		layToolfunction.addStretch()
		layToolfunction.addWidget	(self.radioAvg)
		layToolfunction.addWidget	(self.radioAvgLabel)
		layToolfunction.addStretch()
		layToolfunction.addWidget	(self.radioSph)
		layToolfunction.addWidget	(self.radioSphLabel)
		layToolfunction.addStretch()

		# layout for tool function radio group
		layTogNor =	 QT.QtWidgets.QHBoxLayout(self.wdgTogNor)
		layTogNor.addWidget (self.btnNorLenSub)
		layTogNor.addWidget (self.btnToggleNorShow)
		layTogNor.addWidget (self.btnNorLenAdd)
		layTogNor.setSpacing(4)
		layTogNor.setContentsMargins(0,0,0,0)
		
		# layout for xyz lines
		layLineX =	 QT.QtWidgets.QHBoxLayout(self.wdgLineX)
		layLineX.addWidget	(self.XLabel)
		layLineX.addWidget	(self.btnX5)
#		layLineX.addWidget	(self.btnX0)
		layLineX.addWidget	(self.ValueXfloat)
		layLineX.addWidget	(self.btnX1)
		layLineX.addWidget	(self.btnX2)
		layLineX.addWidget	(self.btnX3)
		layLineX.addWidget	(self.btnX4)
		layLineY =	 QT.QtWidgets.QHBoxLayout(self.wdgLineY)
		layLineY.addWidget	(self.YLabel)
		layLineY.addWidget	(self.btnY5)
#		layLineY.addWidget	(self.btnY0)
		layLineY.addWidget	(self.ValueYfloat)
		layLineY.addWidget	(self.btnY1)
		layLineY.addWidget	(self.btnY2)
		layLineY.addWidget	(self.btnY3)
		layLineY.addWidget	(self.btnY4)
		layLineZ =	 QT.QtWidgets.QHBoxLayout(self.wdgLineZ)
		layLineZ.addWidget	(self.ZLabel)
		layLineZ.addWidget	(self.btnZ5)
#		layLineZ.addWidget	(self.btnZ0)
		layLineZ.addWidget	(self.ValueZfloat)
		layLineZ.addWidget	(self.btnZ1)
		layLineZ.addWidget	(self.btnZ2)
		layLineZ.addWidget	(self.btnZ3)
		layLineZ.addWidget	(self.btnZ4)
		layLineLerp =	 QT.QtWidgets.QHBoxLayout(self.wdgLineLerp)
		layLineLerp.addWidget(self.LerpLabel)
		layLineLerp.addWidget(self.btnOrigin)
		layLineLerp.addWidget   (self.SliderIntensity)
		layLineLerp.addWidget(self.btnTarget)
		
		layHardEdge =	 QT.QtWidgets.QHBoxLayout(self.wdgHardEdge)
		layHardEdge.addWidget(self.btnHardedgeset0)
		layHardEdge.addWidget(self.NormalAngle)
		layHardEdge.addWidget(self.btnHardedgeset180)
		layHardEdge.setSpacing(4)
		layHardEdge.setContentsMargins(0,0,0,0)
		
		layFuncLine1 =	 QT.QtWidgets.QHBoxLayout(self.FuncLine1)
		layFuncLine1.addWidget	(self.btnDefault)
		layFuncLine1.addWidget	(self.wdgTogNor)
		layFuncLine1.addWidget	(self.btnSelectlive)
		
		layFuncLine2 =	 QT.QtWidgets.QHBoxLayout(self.FuncLine3)
		layFuncLine2.addWidget	(self.btnNrmtoCol)
		layFuncLine2.addWidget	(self.btnColtoNrm)
		layFuncLine2.addWidget	(self.btnemptyCol)

		layFuncLine3 =	 QT.QtWidgets.QHBoxLayout(self.FuncLine2)
		layFuncLine3.addWidget	(self.btnHardedge)
		layFuncLine3.addWidget	(self.wdgHardEdge)
		layFuncLine3.addWidget	(self.btnApply)

		#Add the button to a layout....
		layMain =	QT.QtWidgets.QVBoxLayout(self.wdgMain)
		layMain.addWidget   (self.TitleLabel)
		layMain.addWidget   (self.wdgToolfunction)
		layMain.addWidget   (self.wdgLineX)
		layMain.addWidget   (self.wdgLineY)
		layMain.addWidget   (self.wdgLineZ)
		layMain.addWidget   (self.wdgLineLerp)
		layMain.addWidget   (self.FuncLine1)
		layMain.addWidget   (self.FuncLine2)
		layMain.addWidget   (self.FuncLine3)
		layMain.addStretch  ( )
		

		selVerArray = cmds.ls( selection=True, fl=True )
		###SET UP MAYA SCRIPT JOB

		self.getSpherizeTarget()
		self.hideSpherizeTarget()
		self._SphereMovedJob = cmds.scriptJob( ac= ["__NrmTrans_SpherizeTarget.translate",self.syncToSphereMove], protected=True)
		
		##check if already selection
		if not selVerArray:
			print "start: nothing selected"
		else:
#			print "something selected"
			cmds.select(selVerArray)
			self.checkSelection(selVerArray)
#			self.getVertexSelection()


		self._selChangedJob = cmds.scriptJob( e= ["SelectionChanged",self.syncToSelection], protected=True)
	#======================================================================================================================		

	def syncToSelection(self):
		"""This function is used to sync the UI/Tool everytime Maya Changes Selection."""
		#		print "SELECTION CHANGED."
		stsselVerArray = cmds.ls( selection= True, fl=True )
#		if selVerArray :
#			self.getVertexSelection
		if self.selectlive == True:
#			print "selectlive,checkSelection"
			self.checkSelection(stsselVerArray)
		else:
			print"selectnotlive"
#		self.applySpinbox()
#		self.applyIntensity()
	
	def syncToSphereMove(self):
#		print "Moved Sphere"
		self.getVertexSelection()
		if self.selectlive:
			self.applySpinbox()
			self.applyIntensity()
		else:
			print"Live off"
		self.getSpherizeTarget()
#		self.TargetVectorDic.clear()
#		self.TargetVectorDic={'index':[]}
	
	def closeEvent(self, event):
		print "Closing"
		cmds.scriptJob( kill=self._selChangedJob, force=True)
		cmds.scriptJob( kill=self._SphereMovedJob, force=True)
#		self.setvtxtoorigin()
		ApplyNormals(self.VecOriginlist,self.TarNorArray,0)
		self.stopfunction = False
		cmds.delete( '__NrmTrans_SpherizeTarget' )
		cmds.delete( 'Mat_RigTransp_Blue_ShaderG' )
		cmds.delete( 'Mat_RigTransp_Blue' )
		event.accept()
	
	#======================================================================================================================		
	def setdefaultvalue(self):
		self.xdefault()
		self.ydefault()
		self.zdefault()
		return

	#======================================================================================================================		

	def loadToolsetting(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		print "Load tool setting of tool" , toolId
		if toolId == 1:
			self.ValueXfloat.setRange  (-10,10)
			self.ValueYfloat.setRange  (-10,10)
			self.ValueZfloat.setRange  (-10,10)
			self.ValueXfloat.setSingleStep (0.1)
			self.ValueYfloat.setSingleStep (0.1)
			self.ValueZfloat.setSingleStep (0.1)
			self.ValueXfloat.setValue(0)
			self.ValueYfloat.setValue(0)
			self.ValueZfloat.setValue(0)
		elif toolId == 2:
			self.ValueXfloat.setRange  (-100,100)
			self.ValueYfloat.setRange  (-100,100)
			self.ValueZfloat.setRange  (-100,100)
			self.ValueXfloat.setSingleStep (0.1)
			self.ValueYfloat.setSingleStep (0.1)
			self.ValueZfloat.setSingleStep (0.1)
			self.ValueXfloat.setValue(1)
			self.ValueYfloat.setValue(1)
			self.ValueZfloat.setValue(1)
		elif toolId == 3:
			self.ValueXfloat.setRange  (-360,360)
			self.ValueYfloat.setRange  (-360,360)
			self.ValueZfloat.setRange  (-360,360)
			self.ValueXfloat.setSingleStep (15)
			self.ValueYfloat.setSingleStep (15)
			self.ValueZfloat.setSingleStep (15)
			self.ValueXfloat.setValue(0)
			self.ValueYfloat.setValue(0)
			self.ValueZfloat.setValue(0)
		elif toolId == 4:
			self.ValueXfloat.setRange  (-1,1)
			self.ValueYfloat.setRange  (-1,1)
			self.ValueZfloat.setRange  (-1,1)
			self.ValueXfloat.setSingleStep (0.1)
			self.ValueYfloat.setSingleStep (0.1)
			self.ValueZfloat.setSingleStep (0.1)
			self.ValueXfloat.setValue(1)
			self.ValueYfloat.setValue(1)
			self.ValueZfloat.setValue(1)
		elif toolId in [5,6]:
			self.ValueXfloat.setRange  (-1,1)
			self.ValueYfloat.setRange  (-1,1)
			self.ValueZfloat.setRange  (-1,1)
			self.ValueXfloat.setSingleStep (0.1)
			self.ValueYfloat.setSingleStep (0.1)
			self.ValueZfloat.setSingleStep (0.1)
			self.ValueXfloat.setValue(0)
			self.ValueYfloat.setValue(0)
			self.ValueZfloat.setValue(0)
		else:
			print "error:loadToolsetting : Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		if toolId == 6:
			self.getSpherizeTarget()
			self.getVertexSelection()
		else:
			self.hideSpherizeTarget()
		self.togglesign()
		return
		
	def togglesign(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
#		if toolId == 1:
		if toolId in [1,2,5]:
			if self.Xsign == 1:
				self.btnX2.setText('0.15')
				self.btnX3.setText('0.5')
				self.btnX4.setText('1')
			elif self.Xsign == -1:
				self.btnX2.setText('-0.15')
				self.btnX3.setText('-0.5')
				self.btnX4.setText('-1')
			else:
				print"No Xsign"
			if self.Ysign == 1:
				self.btnY2.setText('0.15')
				self.btnY3.setText('0.5')
				self.btnY4.setText('1')
			elif self.Ysign == -1:
				self.btnY2.setText('-0.15')
				self.btnY3.setText('-0.5')
				self.btnY4.setText('-1')
			else:
				print"No Ysign"
			if self.Zsign == 1:
				self.btnZ2.setText('0.15')
				self.btnZ3.setText('0.5')
				self.btnZ4.setText('1')
			elif self.Zsign == -1:
				self.btnZ2.setText('-0.15')
				self.btnZ3.setText('-0.5')
				self.btnZ4.setText('-1')
			else:
				print"No Zsign"	
		elif toolId == 3:
			if self.Xsign == 1:
				self.btnX2.setText('22.5')
				self.btnX3.setText('36')
				self.btnX4.setText('90')
			elif self.Xsign == -1:
				self.btnX2.setText('-22.5')
				self.btnX3.setText('-36')
				self.btnX4.setText('-90')
			else:
				print"No Xsign"
			if self.Ysign == 1:
				self.btnY2.setText('22.5')
				self.btnY3.setText('36')
				self.btnY4.setText('90')
			elif self.Ysign == -1:
				self.btnY2.setText('-22.5')
				self.btnY3.setText('-36')
				self.btnY4.setText('-90')
			else:
				print"No Ysign"
			if self.Zsign == 1:
				self.btnZ2.setText('22.5')
				self.btnZ3.setText('36')
				self.btnZ4.setText('90')
			elif self.Zsign == -1:
				self.btnZ2.setText('-22.5')
				self.btnZ3.setText('-36')
				self.btnZ4.setText('-90')
			else:
				print"No Zsign"
		elif toolId == 4:
			self.btnX4.setText('__')
			self.btnZ4.setText('__')
			if self.Xsign == 1:
				self.btnX2.setText('X')
				if self.Ysign == 1:
					self.btnX3.setText('X.Y')
					if self.Zsign == 1:
						self.btnY4.setText('X.Y.Z')
					else:
						self.btnY4.setText('X.Y.-Z')
				else:
					self.btnX3.setText('X.-Y')
					if self.Zsign == 1:
						self.btnY4.setText('X.-Y.Z')
					else:
						self.btnY4.setText('X.-Y.-Z')
			elif self.Xsign == -1:
				self.btnX2.setText('-X')
				if self.Ysign == 1:
					self.btnX3.setText('-X.Y')
					if self.Zsign == 1:
						self.btnY4.setText('-X.Y.Z')
					else:
						self.btnY4.setText('-X.Y.-Z')
				else:
					self.btnX3.setText('-X.-Y')
					if self.Zsign == 1:
						self.btnY4.setText('-X.-Y.Z')
					else:
						self.btnY4.setText('-X.-Y.-Z')
			else:
				print"No Xsign"
			if self.Ysign == 1:
				self.btnY2.setText('Y')
				if self.Zsign == 1:
					self.btnY3.setText('Y.Z')
				else:
					self.btnY3.setText('Y.-Z')
			elif self.Ysign == -1:
				self.btnY2.setText('-Y')
				if self.Zsign == 1:
					self.btnY3.setText('-Y.Z')
				else:
					self.btnY3.setText('-Y.-Z')
			else:
				print"No Ysign"
			if self.Zsign == 1:
				self.btnZ2.setText('Z')
				if self.Xsign == 1:
					self.btnZ3.setText('X.Z')
				else:
					self.btnZ3.setText('-X.Z')
			elif self.Zsign == -1:
				self.btnZ2.setText('-Z')
				if self.Xsign == 1:
					self.btnZ3.setText('X.-Z')
				else:
					self.btnZ3.setText('-X.-Z')
			else:
				print"No Zsign"
		elif toolId ==6:
			self.btnX4.setText('Sphere')
			if self.Xsign == 1:
				self.btnX2.setText('0.15')
				self.btnX3.setText('0.5')
			elif self.Xsign == -1:
				self.btnX2.setText('-0.15')
				self.btnX3.setText('-0.5')
			else:
				print"No Xsign"
			self.btnY4.setText('Select')
			if self.Ysign == 1:
				self.btnY2.setText('0.15')
				self.btnY3.setText('0.5')
			elif self.Ysign == -1:
				self.btnY2.setText('-0.15')
				self.btnY3.setText('-0.5')
			else:
				print"No Ysign"
			self.btnZ4.setText('Center')
			if self.Zsign == 1:
				self.btnZ2.setText('0.15')
				self.btnZ3.setText('0.5')
			elif self.Zsign == -1:
				self.btnZ2.setText('-0.15')
				self.btnZ3.setText('-0.5')
			else:
				print"No Zsign"	
		else:
			print "error:togglesign:Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		return

# x part	
	def xdefault(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		print "set default value x for tool",toolId
		if toolId in [1,3,5,6]:
			self.ValueXfloat.setValue(0)
		elif toolId in [2,4]:
			self.ValueXfloat.setValue(1)
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		return

	def applyToolx1(self):
		n=self.ValueZfloat.value()
#		self.ValueXfloat.setValue(-self.ValueXfloat.value())
		self.Xsign *= -1
		print "applyToolx1", self.Xsign
		return

	def applyToolx2(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign*0.15,0,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign*22.5,0,0])
		elif toolId == 4:
			ChangeVector=[self.Xsign,0,0]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyToolx3(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign*0.5,0,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign*36,0,0])
		elif toolId == 4:
			ChangeVector=[self.Xsign,self.Ysign,0]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyToolx4(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5]:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign,0,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [self.Xsign*90,0,0])
		elif toolId == 4:
			print "Does nothing"
		elif toolId == 6:
			self.getSpherizeTarget()
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return

# y part		

	def ydefault(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		print "set default value y for tool",toolId
		if toolId in [1,3,5,6]:
			self.ValueYfloat.setValue(0)
		elif toolId in [2,4]:
			self.ValueYfloat.setValue(1)
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		return

	def applyTooly1(self):
		n=self.ValueZfloat.value()
#		self.ValueYfloat.setValue(-self.ValueYfloat.value())
		self.Ysign *= -1
		print "applyTooly1", self.Ysign
		return

	def applyTooly2(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign*0.15,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign*22.5,0])
		elif toolId == 4:
			ChangeVector=[0,self.Ysign,0]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyTooly3(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign*0.5,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign*36,0])
		elif toolId == 4:
			ChangeVector=[0,self.Ysign,self.Zsign]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyTooly4(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign,0])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,self.Ysign*90,0])
		elif toolId == 4:
			ChangeVector=[self.Xsign,self.Ysign,self.Zsign]
		elif toolId == 6:
			self.getVertexSelection()
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
# z part		
	def zdefault(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		print "set default value z for tool",toolId
		if toolId in [1,3,5,6]:
			self.ValueZfloat.setValue(0)
		elif toolId in [2,4]:
			self.ValueZfloat.setValue(1)
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		return

	def applyToolz1(self):
		n=self.ValueZfloat.value()
#		self.ValueZfloat.setValue(-self.ValueZfloat.value())
		self.Zsign *= -1
		print "applyToolz1", self.Zsign
		return

	def applyToolz2(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign*0.15])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign*22.5])
		elif toolId == 4:
			ChangeVector=[0,0,self.Zsign]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyToolz3(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5,6]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign*0.5])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign*36])
		elif toolId == 4:
			ChangeVector=[self.Xsign,0,self.Zsign]
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return
		
	def applyToolz4(self):
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVector = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		if toolId in [1,2,5]:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign])
		elif toolId == 3:
			ChangeVector= self.addtwoVectors(ChangeVector, [0,0,self.Zsign*90])
		elif toolId == 4:
			print "Does nothing"
		elif toolId == 6:
			self.getCenterTarget()
		else:
			print "Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize"
		self.ChangeSpinbox(ChangeVector)
		return

	def applyIntensityOrigin(self):
		self.SliderIntensity.setSliderPosition(0)
	def applyIntensityTarget(self):
		self.SliderIntensity.setSliderPosition(200)
		
	def ChangeSpinbox(self,ChangeVector):
#		print ChangeVector
		self.ValueXfloat.setValue(ChangeVector[0])
		self.ValueYfloat.setValue(ChangeVector[1])
		self.ValueZfloat.setValue(ChangeVector[2])
		return
		
		
	def lerp(self,f1,f2,alpha):
		return alpha*f2+(1-alpha)*f1
	def lerpVectorflalpha(self,v1,v2,alpha):
		return [self.lerp(v1[0],v2[0],alpha), self.lerp(v1[1],v2[1],alpha), self.lerp(v1[2],v2[2],alpha)]
	def addtwoVectors(self,v1, v2):
		return [v1[0]+v2[0], v1[1] + v2[1], v1[2] + v2[2]]
#link with nrmedittool
	def applySpinbox(self):
#		print"start applySpinbox"
		toolId = -1 - self.Toolfuncgrp.checkedId()
		ChangeVec = [self.ValueXfloat.value(),self.ValueYfloat.value(),self.ValueZfloat.value()]		
		asbselVerArray = cmds.ls( selection=True, fl=True )
		if not asbselVerArray:
			print "applySpinbox:nothing selected"
		VerCountFloat = len(asbselVerArray)
		if VerCountFloat > self.vertexlimit:
			print "selection over limit"
			self.stopfunction = True
			return
		self.TarNorArray = AddMulNor(ChangeVec, toolId, self.VecOriginlist)
		return 

	def applyIntensity(self):
		if self.stopfunction:
			print "vertex amount over limit, change selection plz"
			return
		toolIntensity = float(self.SliderIntensity.value())/200
		ApplyNormals(self.VecOriginlist,self.TarNorArray,toolIntensity)
		return

	def zerooldSelection(self):
		vtxFaceCountFloat = len(self.TargetVectorDic) - 1
		if self.stopfunction:
			self.stopfunction = False
			return
		ApplyNormals(self.VecOriginlist,self.TarNorArray,0)
		return

	def applyTool(self):
		if self.stopfunction:
			print "vertex amount over limit, change selection plz"
			return
		#atselVerArray = cmds.ls( selection=True, fl=True )
		self.VecOriginlist = BuildVecOrigin()
		self.applySpinbox()
		self.applyIntensity()
		self.SliderIntensity.setValue(0)
		return
	
	def getSpherizeTarget(self):
		if cmds.objExists('__NrmTrans_SpherizeTarget'):
			cmds.select('__NrmTrans_SpherizeTarget')
#			cmds.sets( e=True, forceElement= 'Mat_RigTransp_Blue_ShaderG' )
			cmds.MoveTool()
		else:
			cmds.sphere( n = '__NrmTrans_SpherizeTarget',nsp=2,s=4)
		if cmds.objExists('Mat_RigTransp_Blue_ShaderG'):
			cmds.sets( '__NrmTrans_SpherizeTarget', e=True, forceElement= 'Mat_RigTransp_Blue_ShaderG' )
		else:
			cmds.shadingNode('lambert', asShader=True,n='Mat_RigTransp_Blue')
			cmds.sets (r=True, noSurfaceShader=True, n='Mat_RigTransp_Blue_ShaderG')
			cmds.connectAttr ('Mat_RigTransp_Blue.outColor', 'Mat_RigTransp_Blue_ShaderG.surfaceShader')
			cmds.setAttr( 'Mat_RigTransp_Blue.color',0, 1, 0, typ='double3' )
			cmds.setAttr( 'Mat_RigTransp_Blue.incandescence',0, 0, 1, typ='double3' )
			cmds.setAttr( 'Mat_RigTransp_Blue.transparency',0.85, 0.85, 1.85, typ='double3' )
			cmds.sets( '__NrmTrans_SpherizeTarget', e=True, forceElement= 'Mat_RigTransp_Blue_ShaderG' )
		cmds.showHidden( '__NrmTrans_SpherizeTarget' )
	def hideSpherizeTarget(self):
		if cmds.objExists('__NrmTrans_SpherizeTarget'):
			cmds.hide( '__NrmTrans_SpherizeTarget' )
	
	def getVertexSelection(self):
		cmds.select(d=True )
		if self.Vertexselect:
			cmds.select(self.Vertexselect)
			cmds.SelectVertexMask()
			cmds.SelectTool()
		else:
			return
	
	def getCenterTarget(self):
		gctselVerArray = cmds.ls( selection=True, fl=True )
		pointCon = gctselVerArray[len(gctselVerArray)-1]
		if '.vtx' in pointCon or '.map' in pointCon:
			newcoor = cmds.pointPosition(pointCon)
#			cmds.setAttr( '__NrmTrans_SpherizeTarget.translate', newcoor )
			cmds.setAttr( '__NrmTrans_SpherizeTarget.translate', newcoor[0],newcoor[1],newcoor[2] )
		elif '.f' in pointCon or '.e' in pointCon:
			pointConlist = cmds.ls(cmds.polyListComponentConversion( pointCon, tv=True ), fl=True )
			newcoor=[0,0,0]
			pointcount = len(pointConlist)
			for y in range (0,pointcount):
				addedvect= cmds.pointPosition(pointConlist[y])
				newcoor = self.addtwoVectors(addedvect,newcoor)
			newcoor = [newcoor[0]/pointcount,newcoor[1]/pointcount,newcoor[2]/pointcount]
			cmds.setAttr( '__NrmTrans_SpherizeTarget.translate', newcoor[0],newcoor[1],newcoor[2] )
		else:
			cmds.pointConstraint(gctselVerArray[0], '__NrmTrans_SpherizeTarget',n='__tobedelete_pointConstraint' )
			cmds.delete ('__tobedelete_pointConstraint')

	def setvtxtoorigin(self):
		vtxFaceCountFloat = len(self.OriginVectorDic) - 1
		ovdindex = self.OriginVectorDic['index']
		if not ovdindex:
			pass
		else:
			for x in range(0,vtxFaceCountFloat):
				currentvtxFace = ovdindex[x]
				currentvtxOVal = self.OriginVectorDic[ovdindex[x]]
				cmds.polyNormalPerVertex(currentvtxFace, xyz = currentvtxOVal)
		
	def checkSelection(self,selVerArray):
		#convert selection
	#	selVerArray = cmds.ls( selection=True, fl=True )
#		print "selVerArray",selVerArray
#		currentsel = cmds.polyListComponentConversion( selVerArray, tv=True)
#		print"start checkSelection"
#		print selVerArray
		if not selVerArray:
			print"checkSelection:nothing selected"
		elif self.savedsel == selVerArray:
#			print'same'
			if self.selectlive:
				self.applySpinbox()
				self.applyIntensity()
			else:
				print"Live off"
		elif '__NrmTrans_SpherizeTarget' in selVerArray:
#			self.SpherizeTargetselected= True
			print "is sphere"
		elif any('__NrmTrans_SpherizeTarget' in s for s in selVerArray):
#			print "is sphere part"
			cmds.select('__NrmTrans_SpherizeTarget')
		elif any('.vtx' in s for s in selVerArray ):
			if not self.VecOriginlist:
#				print "no before selection"
				pass
			else:
#				print"zerooldSelection"
				if self.stopfunction:
					self.stopfunction = False
				else:
					ApplyNormals(self.VecOriginlist,self.TarNorArray,0)
			
#			self.savedsel = selVerArray
			self.Vertexselect = selVerArray
		#####get all vtxFace of an object and edit it first to prevent the normal splitting bug###
			Activeallvtxface()
#			ApplyNormals(self.VecOriginlist,self.TarNorArray,toolIntensity)
#			self.checkobjnormals(selVerArray)
			self.VecOriginlist = BuildVecOrigin()
#			print "selection changed: current selection:" ,self.OriginVectorDic
			if self.selectlive:
				self.applySpinbox()
				self.applyIntensity()
			else:
				print"Live off"

		else:
			print "not vertex"
				
	def NorLenAdd(self):
		cmds.polyOptions( r=True, sn=1.41421356237 )
	
	def NorLenSub(self):
		cmds.polyOptions( r=True, sn=0.70710678118 )
		
	def ToggleNorShow(self):
		if cmds.polyOptions(q=True, dn=True )[0]:
			cmds.polyOptions( dn=False,pt=True )
		else:
			cmds.polyOptions( dn=True,pt=True )
		
	def HardedgeNormals(self):
		henselVerArray = cmds.ls( selection=True, fl=True )
		if not henselVerArray:
			pass
			print "nothing selected"
			return
		if self.selectlive:
#			print"test: sel islive in HardedgeNormals"
			self.selectlive = False
#			print "self.selectlive", self.selectlive
			cmds.polyNormalPerVertex(ufn=True)
			cmds.select(cmds.polyListComponentConversion( henselVerArray, te=True ))
			cmds.polySoftEdge( a=self.NormalAngle.value() )
#			cmds.polyNormalPerVertex(cmds.polyListComponentConversion( selVerArray, tv=True ),ufn=True)
			cmds.select(henselVerArray)
			self.VecOriginlist = BuildVecOrigin()
			self.SliderIntensity.setValue(0)
			self.selectlive = True
			return
		else:
#			print"test: sel is not live in HardedgeNormals"
			cmds.polyNormalPerVertex(ufn=True)
			cmds.select(cmds.polyListComponentConversion( henselVerArray, te=True ))
			cmds.polySoftEdge( a=self.NormalAngle.value() )
			cmds.select(henselVerArray)
			self.VecOriginlist = BuildVecOrigin()
			return
			#		cmds.polyNormalPerVertex(ufn=True)
			
	def Hardedgeset0(self):
		self.NormalAngle.setValue(0)
		
	def Hardedgeset180(self):
		self.NormalAngle.setValue(180)
		
	def ToggleSelectlive(self):
		if self.selectlive:
			self.selectlive = False
			self.btnSelectlive.setText('Live Off')
		else:
			self.selectlive = True
			self.btnSelectlive.setText('Live On')
			tslselVerArray = cmds.ls( selection=True, fl=True )
			self.checkSelection(tslselVerArray)
			
	def convertNrmtoCol(self):
		if self.stopfunction:
			print "vertex amount over limit, change selection plz"
			return
		cmds.polyColorPerVertex( cdo=True )
		self.applySpinbox()
		toolIntensity = float(self.SliderIntensity.value())/200
		NormaltoColor(self.VecOriginlist,self.TarNorArray,toolIntensity)
		self.VecOriginlist = BuildVecOrigin()
		self.SliderIntensity.setValue(0)
		
	def convertColtoNrm(self):
		if self.stopfunction:
			print "vertex amount over limit, change selection plz"
			return
		ColortoNormal(self.VecOriginlist)
		self.VecOriginlist = BuildVecOrigin()
		self.SliderIntensity.setValue(0)
		
	def emptyCol(self):
		if self.stopfunction:
			print "vertex amount over limit, change selection plz"
			return
		EmptyColor(self.VecOriginlist)
		self.VecOriginlist = BuildVecOrigin()
		self.SliderIntensity.setValue(0)
		
#This is the FUNCTION that will LAUNCH the Window
def launchUI():
	window =										None
	uiName =										'Normal_translator'
	#FIRST... check to see if the Window already EXISTS.. .and if so, just 'RAISE' it to the top
	if uiName in globals() and globals()[uiName].isVisible():
		window =									globals()[uiName]
		if window.isVisible():
			window.show								( )
			window.raise_							( )
			return									None
	
	#IF it doesn't exists... Make a new window...
	nuWindow =										mayaDockableWindow( )
	globals()[uiName] =								nuWindow
	nuWindow.show									(dockable = 	True,
													area=			'right',
													floating = 		True )
	nuWindow.raise_ ( )
	return							
#================================================================================================

def multiplyxyzVectors(v1, v2):
	return om.MVector(v1.x*v2.x, v1.y*v2.y, v1.z*v2.z)
def rotateVector(vA, RotdegV):
	eRot = om.MEulerRotation(math.radians(RotdegV.x), math.radians(RotdegV.y) ,math.radians(RotdegV.z) )
	vB = vA.rotateBy(eRot)
	vB.x = round(vB.x, 6)
	vB.y = round(vB.y, 6)
	vB.z = round(vB.z, 6)
	return vB
def lerp(f1,f2,alpha):
	return alpha*f2+(1-alpha)*f1
def lerpVector(v1,v2,alpha):
	return om.MVector(lerp(v1.x,v2.x,alpha.x), lerp(v1.y,v2.y,alpha.y), lerp(v1.z,v2.z,alpha.z))
	
def _getSelectedComponents( ):
	"""Returns the selected Components, if any, of the target Object.
	target		<MFnDependencyNode>		The Dependency Node of the target Mesh."""
	selection = 									om.MSelectionList()		# ACTIVE SCENE SELECTION
	om.MGlobal.getActiveSelectionList				(selection)	
	adddagPathMesh =									    om.MDagPath()
	dagPathMeshArray = 								    om.MDagPathArray()
	oMeshList =  om.MObjectArray()
	oComponentsArray =  om.MObjectArray()
	for i in range(selection.length()):
#		print"loop selection length"
		dagPathMesh =									    om.MDagPath()
		oComponents =								om.MObject()
		selection.getDagPath						(i, dagPathMesh, oComponents)
#		print "oComponents",oComponents
#		print "dagPathMesh",dagPathMesh
		if not dagPathMesh == adddagPathMesh:
#			print"loop 0"
			adddagPathMesh = dagPathMesh
			oComponentsArray.append(oComponents)
			oMesh = dagPathMesh.node()
			oMeshList.append(oMesh)
			dagPathMeshArray.append(dagPathMesh)
		#oMesh =										_getMeshShape(oGeo)
		#result =							    	oComponents
		if not oComponents.isNull():
#			print"update result"
			result =  ( dagPathMeshArray, oComponentsArray, oMeshList)
#			print result
#			break
#		result =  ( dagPathMeshArray, oComponents)
#	else:
#		print"else"
#		result = (om.MObject(), om.MObject() )
	return											result
	
def BuildVecOrigin():
	dagPathMeshArray, oCompsArray, oMeshList =  _getSelectedComponents()
	if not oCompsArray[0].isNull():
		oMeshArray = om.MObjectArray()
		iVertArray = om.MIntArray()
		iFaceArray = om.MIntArray()
		vPosArray = om.MVectorArray()
		vNormalArray = om.MVectorArray()
		cVtxColorArray = om.MColorArray()
		for x in range(dagPathMeshArray.length()):
			dagPathMesh = dagPathMeshArray[x]
			oMesh = dagPathMesh.node()
			oComps = oCompsArray[x]
			itComponent = 									om.MItMeshFaceVertex(dagPathMesh,oComps) 	# iterate only on selected components
			while not itComponent.isDone():
				iVertArray.append(itComponent.vertId())
				iFaceArray.append(itComponent.faceId())
				oMeshArray.append(oMesh)
				cVtxColor = om.MColor()
				itComponent.getColor(cVtxColor, om.MSpace.kObject)
				cVtxColorArray.append(cVtxColor)
				#get normals in each vertex
				pPos=itComponent.position(om.MSpace.kWorld)
				vPosArray.append(om.MVector(pPos.x,pPos.y,pPos.z))
				oNormal = om.MVector()
				itComponent.getNormal(oNormal, om.MSpace.kObject)
				vNormalArray.append(oNormal)
				itComponent.next()
		return [oMeshArray,iVertArray,iFaceArray,vNormalArray,vPosArray,oMeshList,cVtxColorArray]
	else:
		print"nothing test"
		return [0,0,0,0,0]

def Activeallvtxface():
#	print (VerA)
#	print" Activeallvtxface "
	dagPathMeshArray, oCompsArray, oMeshList =  _getSelectedComponents()
#	print dagPathMeshArray, oComps
	if not oCompsArray[0].isNull():
		for x in range(dagPathMeshArray.length()):
			dagPathMesh = dagPathMeshArray[x]
			oMesh = dagPathMesh.node()
			#set to empty everyloop
			iVertArray = om.MIntArray()
			iFaceArray = om.MIntArray()
#			vPosArray = om.MVectorArray()
			vNormalArray = om.MVectorArray()
			itComponent = 									om.MItMeshFaceVertex(oMesh) 	# iterate all
			while not itComponent.isDone():
				iVertArray.append(itComponent.vertId())
				iFaceArray.append(itComponent.faceId())
				#get normals in each vertex
				oNormal = om.MVector()
				itComponent.getNormal(oNormal, om.MSpace.kObject)
				vNormalArray.append(oNormal)
				itComponent.next()
			mMesh = om.MFnMesh(oMesh)
			mMesh.setFaceVertexNormals (vNormalArray, iFaceArray, iVertArray, om.MSpace.kObject)
	else:
		print"nothing test"
		
	
		
def AddMulNor(VecChange, UseTool, VecOriginlist):
	iVertArray = VecOriginlist[1]
	vOriNorArray = VecOriginlist[3]
	vPosArray = VecOriginlist[4]
	vTarNorArray =[]
	ChangeVector = om.MVector(VecChange[0],VecChange[1],VecChange[2])
	#get Spherize Target
	if UseTool==6:
		SpherizeTargetCoor= cmds.getAttr('__NrmTrans_SpherizeTarget.translate')[0]
		oSpherizeTargetCoor = om.MVector(SpherizeTargetCoor[0],SpherizeTargetCoor[1],SpherizeTargetCoor[2])
	for x in range(vOriNorArray.length()):
		NewxyzVector = vOriNorArray[x]
		if UseTool==1:
			NewxyzVector = NewxyzVector + ChangeVector
		elif UseTool==2:
			NewxyzVector = multiplyxyzVectors(NewxyzVector, ChangeVector)
		elif UseTool==3:
			NewxyzVector = rotateVector(NewxyzVector, ChangeVector)
		elif UseTool==4:
			NewxyzVector = ChangeVector
		elif UseTool==5: 
			#get the position of the same vtxs
			samevtxposit=[i for i in range(iVertArray.length()) if iVertArray[i]== iVertArray[x]]
			AveragedVec=om.MVector(0,0,0)
			for y in range(len(samevtxposit)):
				AveragedVec = vOriNorArray[samevtxposit[y]] + AveragedVec
			AveragedVec.normalize()
			NewxyzVector = lerpVector(NewxyzVector,AveragedVec,ChangeVector)
		elif UseTool==6: 		
			VertexCoor = vPosArray[x]
			SpherizeTargetNormal = VertexCoor - oSpherizeTargetCoor
			NewxyzVector = lerpVector(NewxyzVector,SpherizeTargetNormal,ChangeVector)
		elif UseTool==7:
			pass
		else: 
		
			print "error:AddMulNor:Non specified UseTool: 1 Add 2 Multiply 3 Rotate 4 Replace 5 Average 6 Spherize 7 ColorTransfer"
#		NewxyzVector=[NewxyzVectorOM.x,NewxyzVectorOM.y,NewxyzVectorOM.z]
		vTarNorArray.append(NewxyzVector)
		#			VerAdict.update({vtxFaceName : NewxyzVector})
	return vTarNorArray

def ApplyNormals(VecOriginlist,vTarNorArray,Intensity):
	oMeshArray = VecOriginlist[0]
	iVertArray = VecOriginlist[1]
	iFaceArray = VecOriginlist[2]
	vOriNorArray = VecOriginlist[3]
	oMeshlist= VecOriginlist[5]
	for y in range(oMeshlist.length()):
		mMesh = om.MFnMesh(oMeshlist[y])
		IntenVec = om.MVector(Intensity,Intensity,Intensity)
		vResultArray = om.MVectorArray()
		CiVertArray = om.MIntArray()
		CiFaceArray = om.MIntArray()
		samemeshposit=[i for i in range(oMeshArray.length()) if oMeshArray[i]== oMeshlist[y]]
		for x in range(len(samemeshposit)):
			posit=samemeshposit[x]
			CiFaceArray.append(iFaceArray[posit])
			CiVertArray.append(iVertArray[posit])
			OriNor = vOriNorArray[posit]
			TarNor = vTarNorArray[posit]
			ResultNor = lerpVector(OriNor,TarNor,IntenVec)
			vResultArray.append(ResultNor)
		mMesh.setFaceVertexNormals (vResultArray, CiFaceArray, CiVertArray, om.MSpace.kObject)
	
def NormaltoColor(VecOriginlist,vTarNorArray,Intensity):
	oMeshArray = VecOriginlist[0]
	iVertArray = VecOriginlist[1]
	iFaceArray = VecOriginlist[2]
	vOriNorArray = VecOriginlist[3]
	oMeshlist= VecOriginlist[5]
	for y in range(oMeshlist.length()):
		mMesh = om.MFnMesh(oMeshlist[y])
		IntenVec = om.MVector(Intensity,Intensity,Intensity)
		cVtxColorArray = om.MColorArray()
		CiVertArray = om.MIntArray()
		CiFaceArray = om.MIntArray()
		samemeshposit=[i for i in range(oMeshArray.length()) if oMeshArray[i]== oMeshlist[y]]
		for x in range(len(samemeshposit)):
			posit=samemeshposit[x]
			CiFaceArray.append(iFaceArray[posit])
			CiVertArray.append(iVertArray[posit])
			OriNor = vOriNorArray[posit]
			TarNor = vTarNorArray[posit]
			ResultNor = lerpVector(OriNor,TarNor,IntenVec)
			cVtxColor=om.MColor((ResultNor.x+1)/2,(ResultNor.y+1)/2,(ResultNor.z+1)/2,1.0)
			cVtxColorArray.append(cVtxColor)
		mMesh.setFaceVertexColors(cVtxColorArray, CiFaceArray, CiVertArray)
		
def ColortoNormal(VecOriginlist):
	oMeshArray = VecOriginlist[0]
	iVertArray = VecOriginlist[1]
	iFaceArray = VecOriginlist[2]
	cVtxColorArray = VecOriginlist[6]
	oMeshlist= VecOriginlist[5]
	for y in range(oMeshlist.length()):
		mMesh = om.MFnMesh(oMeshlist[y])
		samemeshposit=[i for i in range(oMeshArray.length()) if oMeshArray[i]== oMeshlist[y]]
		CiVertArray = om.MIntArray()
		CiFaceArray = om.MIntArray()
		vResultArray = om.MVectorArray()
		for x in range(len(samemeshposit)):
			posit=samemeshposit[x]
			cVtxColor = cVtxColorArray[posit]
			ResultNor=om.MVector(cVtxColor.r*2-1,cVtxColor.g*2-1,cVtxColor.b*2-1)
			vResultArray.append(ResultNor)
			CiFaceArray.append(iFaceArray[posit])
			CiVertArray.append(iVertArray[posit])
		mMesh.setFaceVertexNormals (vResultArray, CiFaceArray, CiVertArray, om.MSpace.kObject)
	
	
	
def EmptyColor(VecOriginlist):
	oMeshArray = VecOriginlist[0]
	iVertArray = VecOriginlist[1]
	iFaceArray = VecOriginlist[2]
	oMeshlist= VecOriginlist[5]
	for y in range(oMeshlist.length()):
		mMesh = om.MFnMesh(oMeshlist[y])
		cVtxColorArray = om.MColorArray()
		CiVertArray = om.MIntArray()
		CiFaceArray = om.MIntArray()
		samemeshposit=[i for i in range(oMeshArray.length()) if oMeshArray[i]== oMeshlist[y]]
		for x in range(len(samemeshposit)):
			posit=samemeshposit[x]
			CiFaceArray.append(iFaceArray[posit])
			CiVertArray.append(iVertArray[posit])
		mMesh.removeFaceVertexColors(CiFaceArray, CiVertArray)
		
		
launchUI()
