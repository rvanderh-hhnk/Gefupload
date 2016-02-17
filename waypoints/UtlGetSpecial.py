#!/usr/bin/python
import os
import UtlGefOpen
from UtlGefOpen import *
##Deel 1: Functies die onderdeel van Gef2.dll/UtlGef.py/Gef.py uitmaken
## waaronder onderdelen voor de functie Test_Gef 

##Deel 2: Testen die door Gijsbert of Bart belangrijk/nuttig worden gevonden

# Bart TestGefData r227 tm r234
def getSoortGef(headerdict):
	if	UtlGefOpen.Gbr_Is_Gbr(headerdict):
		SoortGef='boring' 
	elif UtlGefOpen.Gcr_Is_Gcr(headerdict): 
		SoortGef='sondering' 
	elif UtlGefOpen.Brh_Is_Brh(headerdict):
		SoortGef='peilbuisput'
	else: 
		SoortGef='onbekend'
	try:
		return SoortGef
	except: 
		return None	

# Bart TestGefData r255 tm 289
def testXYbinnenBereik(headerdict):
    try:
	X = Get_XYID_X(headerdict)
	if X is None:
		return 'X-waarde niet gevonden'
	elif X < 100000 or X > 200000:
		return 'X-coordinaat buiten gebied'
	Y = Get_XYID_Y(headerdict)
	if Y is None:
		return 'Y-waarde niet gevonden'
        elif Y < 400000 or Y > 600000:
		return 'Y-coordinaat buiten gebied'
	Z = Get_XYID_Y(headerdict)
	if Z is None:
		return 'Z-waarde niet gevonden'
        elif Z < -999 or Z > 999:
              return 'Z-waarde out of range'
    except:
	return None

# Bart testGefData r291 tm r295 
def getStartDatumBart(headerdict):
    try:
    	if UtlGefOpen.Gbr_Is_Gbr(headerdict): 
         	d = UtlGefOpen.Get_BOR_DatumBoring(headerdict) # '01/01/15'
         	StartDatum = '20'+d[6:8]+'-'+d[3:5]+'-'+d[0:2]
        else:
         	StartDatum = UtlGefOpen.Get_StartDate_AsText_ISO(headerdict) #gef.Get_StartDate_AsText_Local(headerdict)
	return StartDatum
    except:
	return None

# Bart TestGefData r373-398 (Paul L. checks)
def IsCorrectBestandPeilbuisput(headerdict,i_sTest1, i_sTest2, i_sTest3, i_sTest4):
    try:
	if (i_sTest1 == 'true' and not Is_Plotable(headerdict))\
	or (i_sTest2 == 'true' and not Test_Gef('DATA'))\
	or (i_sTest3 == 'true' and not Test_Gef('HEADER'))\
	or (i_sTest4 == 'true' and not Get_ReportType_Flag(headerdict,'GEF-BOREHOLE-Report')):
		return False
    except:
	return True
