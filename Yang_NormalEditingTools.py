# -*- coding: UTF-8 -*-   
#--------------------------------------------------------------------------
#
# ScriptName : Normal Editing Tools
# Contents   : Adjusts the normal
# Author	 : 则远霄汉Yiyang Chen
# Update	 : 2017/7/8
# Note	  	 : Credits to Charlie McKenna for helping me out
#			   
#--------------------------------------------------------------------------
import maya.cmds as cmds
import maya.OpenMaya as om
import math

# works with om Vectors

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
		