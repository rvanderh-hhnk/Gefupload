#!env/bin/python
# -----------------------------------------------------------------------------
# Name   : UtlGefOpen.py
# Purpose: Set van Gef gerelateerde functies.
# Note   : - Afgeleid van UtlGef.py van Paul Lauman van 13 Jul 2012
#	   - Exact dezelfde output wordt gegenereerd als door UtlGef.py
#	   - Maakt geen gebruik van Gef2.dll
#	   - Kan dus ook buiten Windows gebruikt worden
#	   - Alleen Categorie A is gewijzigd. Overige Categorien zijn idem versie 2012
# Versie: Python 2.7
# Datum:  10 Jul 2015
# Rik van der Helm
#
# Bijgewerkt door Bart Kropf
# Datum:  23-10-2015
# aanpassingen:

# Bijgewerkt door Rik van der Helm
# Datum:  18-01-2016
# aanpassingen:

# Bijgewerkt door Bart Kropf
# Datum:  07-02-2016
# aanpassingen:
# 'STARTDATE' vervangen door 'FILEDATE'

import re
import datetime
import os

#Variabelen
#i_sISODatum='2015-01-01'

# Hulpfuncties
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def removetrailers(string):
	d=re.sub('^[\t|\ ]*','',string)
	e=re.sub('\r\n$','',d)
	return e

# Een dictionary met alle data uit het input gefbestand. keys zijn gelijk aan de headernamen van het gefbestand

def headerdict(i_sBestandGef):
    EOH=False
    try:
        multipars=['COLUMNINFO','COLUMNVOID','MEASUREMENTTEXT','MEASUREMENTVAR','SPECIMENVAR','SPECIMENTEXT']
        headerdict={}
        f = open(i_sBestandGef,'r')
        tel=0
        for line in f.readlines():
	    line=re.sub('\r\n','',line) # haal alle \r\n aan het einde van de regel weg
	    line=re.sub('(^[ \t]*)','',line) #remove trailing whitespace
	    if not re.sub('^[\ \t]*$','',line)=='': # lege regels uitsluiten. moet dit in test_gef?
		    if 1==1: #test1: begint line1 met '#' en komt '=' minstens 1x voor
		    	line=line.split('=',1)
			par=re.sub('^#([^ \t]*)[ \t]*$','\\1',line[0])
			if len(line)>1:
				keyinfo=line[1]
		    		keyinfo=re.sub('(^[ \t]*)','',keyinfo) #remove trailing whitespace
	  	    		keyinfo=re.sub('([,])([ \t])+','\\1',  re.sub('([ \t])+([,])','\\2',keyinfo)) #haal eerst alle witruimte (spaties/tabs) rond de separators (',') weg. 15-10-29
				keyinfo=keyinfo.split(',')
			else:
				keyinfo=None
			b=keyinfo
	                if par in multipars: #tabje hoger gezet zodat conditie alleen geldt als een par bestaat. 2015-10-29
		        	if is_number(b[0]):
		        		parno=float(b[0])
		        	else:
		                	parno=b[0]
				#del keyinfo[0]
		                testpar='par1'
		                c=[]
				if keyinfo is not None:
			                for i in b:
			                    e=removetrailers(i)
			                    if is_number(e):
			                        c.append(float(e))
			                    else:
			                        c.append(e)
			                if par not in headerdict:
			                    headerdict[par]={parno:c}
			                else:
			                    headerdict[par][parno]=c
				else: parno=None
	                if par == 'EOH':
	                    headerdict['datablok']={}
			    EOH=True
	                    headerdict[par]={}
			if EOH is True and par<>'EOH':
	                        tel=tel+1
				data=par
				data=re.sub(';!','',data) #einde dataregel. moet hier een test op?
				data=re.sub("'","",data)
				data=re.sub('"','',data)
	                        data=re.split(';|\ |\t|\n',data)
	                        a2=[]
	                        for i in data:
	                            if is_number(i):
	                                a2.append(float(i))
	                            else:
	                                a2.append(i)
	                        headerdict['datablok'][tel]=a2
	                if (par <> 'EOH') and (par not in multipars) and (EOH is not True):
	                    testpar='par2'
	                    c=[]
	                    for i in b:
	                        e=removetrailers(i)
	                        if is_number(e):
	                            c.append(float(e))
	                        else:
	                            c.append(e)
	                    headerdict[par]=c
        return headerdict
    except IndexError:
        print ("%s Headerdict() in UtlGefOpen.py geef IndexError: fout bij uitlezen gef"%os.path.basename(i_sBestandGef))
        return headerdict

# De functies zijn hieronder - alfabetisch - ingedeeld in 4 categorieen:
#    A. Basisfuncties zoals ook beschikbaar in en afgeleid uit gef2.dll
#    B. aanvullende helper functies
#    C. voor vullen kolommen gebruikt door meerdere tabellen (ALG)
#    D. voor vullen kolommen gebruikt door tabel SONDERING (SON)
#    E. voor vullen kolommen gebruikt door tabel BORING (BOR)
#    F. voor vullen kolommen gebruikt door tabel PEILBUISPUT (PBP)

# -----------------------------------------------------------------------------
# CATEGORIE A. Basisfunctis zoals ook beschikbaar in en afgeleid uit gef2.dll
# -----------------------------------------------------------------------------

# Purpose: Of een GEF-BORE-Report file is (boring)
# (rik: hoe dan ook, 'boring' is het zeker,gaap)

def Gbr_Is_Gbr(headerdict):
	if\
        ('PROCEDURECODE' in headerdict\
            and\
        'GEF-BORE-Report' in headerdict['PROCEDURECODE'])\
    	or\
        ('REPORTCODE' in headerdict\
            and\
        'GEF-BORE-Report' in headerdict['REPORTCODE']):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Of een GEF-CPT-Report file is (sondering)
def Gcr_Is_Gcr(headerdict):
	if\
        ('PROCEDURECODE' in headerdict and 'GEF-CPT-Report' in headerdict['PROCEDURECODE'])\
    	or\
        ('REPORTCODE' in headerdict and 'GEF-CPT-Report' in headerdict['REPORTCODE']):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Of een GEF-BOREHOLE-Report file is (peilbuisput) b.k.
def Brh_Is_Brh(headerdict):
	if\
        ('PROCEDURECODE' in headerdict and 'GEF-BOREHOLE-Report' in headerdict['PROCEDURECODE'])\
    	or\
        ('REPORTCODE' in headerdict and 'GEF-BOREHOLE-Report' in headerdict['REPORTCODE']):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Of #COMPANYID aanwezig
def Get_CompanyID_Flag(headerdict):
	if('COMPANYID' in headerdict and len(headerdict['COMPANYID'])>0):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Geeft aantal kolommen in het data block
# (rik: getest maar melding hierboven klopt niet, waarde is zelfde waarde als achter 'COLUMN')
def Get_Column(headerdict):
	if ('COLUMN' in headerdict and len(headerdict['COLUMN'])==1):
		out=headerdict['COLUMN'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #COLUMN aanwezig
def Get_Column_Flag(headerdict):
	if ('COLUMN' in headerdict ):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Geeft company naam
def Get_CompanyID_Name(headerdict):
	if('COMPANYID' in headerdict and len(headerdict['COMPANYID'])>0):
		out=headerdict['COMPANYID'][0]
	try:
		return out
	except:
		return None

# Purpose: Geeft waarde uit bepaalde cel van data block
def Get_Data(headerdict,i_Kol, iRij):
	#dit moet ik nog eens uitzoeken, maar ik vermoed dat het dit is:
	out=headerdict['datablok'][iRij][i_Kol]
	try:
		return out
	except:
		return None

# Purpose: Of gegeven #MEASUREMENTTEXT index aanwezig
def Get_MeasurementText_Flag(headerdict,i_Index):
	if ('MEASUREMENTTEXT' in headerdict and i_Index in headerdict['MEASUREMENTTEXT']):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Of gegeven #MEASUREMENTVAR index aanwezig
def Get_MeasurementVar_Flag(headerdict,i_Index):
	if ('MEASUREMENTVAR' in headerdict and i_Index in headerdict['MEASUREMENTVAR']):
		out = True
	else:
		out = False
	try:
		return out
	except:
		return None

# Purpose: Geeft measurementtext tekst
def Get_MeasurementText_Tekst(headerdict,i_Index):
	try:
		out=headerdict['MEASUREMENTTEXT'][i_Index] #??
		return out
	except:
		return None

# Purpose: Geeft measurementvar value
def Get_MeasurementVar_Value(headerdict,i_Index):
	if\
        ('MEASUREMENTVAR' in headerdict\
        and\
        i_Index in headerdict['MEASUREMENTVAR'] and len(headerdict['MEASUREMENTVAR'][i_Index])>0):
		  out = headerdict['MEASUREMENTVAR'][i_Index][1]
	try:
		return out
	except:
		return None

# Purpose: Geeft aantal rijen in het data block
# neem aan waarde achter 'LASTSCAN', maar check dit!
def Get_Nr_Scans(headerdict):
	if ('LASTSCAN' in headerdict and len(headerdict['LASTSCAN'])>0):
		out=headerdict['LASTSCAN'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #PARENT aanwezig
# neeem aan dat er een par 'PARENT' aanwezig moet zijn. Check!
def Get_Parent_Flag(headerdict):
	if ('PARENT' in headerdict and len(headerdict['PARENT'])>0):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Geeft referentie naar de parent, bv bestandsnaam
def Get_Parent_Reference(headerdict):
	if ('PARENT' in headerdict and len(headerdict['PARENT'])>0):
		out=headerdict['PARENT'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #PROCEDURECODE aanwezig
def Get_ProcedureCode_Flag(headerdict):
	if ('PROCEDURECODE' in headerdict and len(headerdict['PROCEDURECODE'])>0):
		out=True
	else:
		out=False
	try:
		return out
	except:
		return None

# Purpose: Geeft procedurecode code
def Get_ProcedureCode_Code(headerdict):
	if ('PROCEDURECODE' in headerdict and len(headerdict['PROCEDURECODE'])>0):
		out=headerdict['PROCEDURECODE'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #PROJECTID aanwezig
def Get_ProjectID_Flag(headerdict):
	if ('PROJECTID' in headerdict and len(headerdict['PROJECTID'])>0):
		out = True
	else:
		out = False

# Purpose: Geeft projectid nummer
def Get_ProjectID_Number(headerdict):
	if ('PROJECTID' in headerdict and len(headerdict['PROJECTID'])>0):
		out = headerdict['PROJECTID'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #REPORTCODE aanwezig
def Get_ReportCode_Flag(headerdict):
	if ('REPORTCODE' in headerdict and len(headerdict['REPORTCODE'])>0):
		out = True
	else:
		out = False
	try:
		return out
	except:
		return None

# Purpose: Geeft reportcode code
def Get_ReportCode_Code(headerdict):
	if ('REPORTCODE' in headerdict and len(headerdict['REPORTCODE'])>0):
		out = headerdict['REPORTCODE'][0]
	try:
		return out
	except:
		return None

# Purpose: Of #STARTDATE aanwezig
def Get_StartDate_Flag(headerdict):
	if ('FILEDATE' in headerdict and len(headerdict['FILEDATE'])>2):
		out = True
	else:
		out = False
	try:
		return out
	except:
		return None

# Purpose: Geeft startdate jaar (yyyy)
def Get_StartDate_Yyyy(headerdict):
	if ('FILEDATE' in headerdict and len(headerdict['FILEDATE'])>2):
		out = int(headerdict['FILEDATE'][0])
	try:
		return out
	except:
		return None

# Purpose: Geeft startdate maand (mm)
def Get_StartDate_Mm(headerdict):
	if ('FILEDATE' in headerdict and len(headerdict['FILEDATE'])>2):
		out = int(headerdict['FILEDATE'][1])
	try:
		return out
	except:
		return None

# Purpose: Geeft startdate dag (dd)
def Get_StartDate_Dd(headerdict):
	if ('FILEDATE' in headerdict and len(headerdict['FILEDATE'])>2):
		out = int(headerdict['FILEDATE'][2])
	try:
		return out
	except:
		return None

# Purpose: Of #XYID aanwezig
def Get_XYID_Flag(headerdict):
	if ('XYID' in headerdict and len(headerdict['XYID'])>4):
		out = True
	else:
		out = False
	try:
		return out
	except:
		return None

# Purpose: Geeft X coordinaat
def Get_XYID_X(headerdict):
	if ('XYID' in headerdict and len(headerdict['XYID'])>4):
		out = headerdict['XYID'][1]
	try:
		return out
	except:
		return None

# Purpose: Geeft Y coordinaat
def Get_XYID_Y(headerdict):
	if ('XYID' in headerdict and len(headerdict['XYID'])>4):
		out = headerdict['XYID'][2]
	try:
		return out
	except:
		return None

# Purpose: Of #ZID aanwezig
def Get_ZID_Flag(headerdict):
	if ('ZID' in headerdict and len(headerdict['ZID'])>1):
		out = True
	else:
		out = False
	try:
		return out
	except:
		return None

# Purpose: Geeft Z coordinaat
def Get_ZID_Z(headerdict):
	if ('ZID' in headerdict and len(headerdict['ZID'])>1):
		out = headerdict['ZID'][1]
	try:
		return out
	except:
		return None

# Purpose: Initialiseren interne geheugenstructuur
# lijkt me niet nodig
def Init_Gef():
	 True

# Purpose: Of een bestand geplot kan worden
def Is_Plotable():
	return 'datmoetenwenogeensuitzoeken'

# Purpose: Geeft kolom nummer die correspondeert met gegeven 'quantity
#          number', en 0 wanneer deze niet aanwezig.
# Note   : Bv, quantity number voor 'gecorrigeerde diepte' is 11.
def Qn2Column(i_iQtyNumber):
	return 'datmoetenwenogeensuitzoeken'

# Purpose: Leest een gegeven Gef bestand in geheugen
# lijkt me niet nodig
def Read_Gef(i_sBestandGef):
	#return True
    	out = i_sBestandGef
	try:
		return out
	except:
		return None

# Purpose: Of een bepaald aspect van een bestand correct is
# Parms  : Toegestaan: 'HEADER', 'DATA', 'GEF-CPT-Report','GEF-BORE-Report'
# Note   : - heb gemerkt dat deze functie bij aanroep met parm 'GEF-CPT-Report'
#            bij een corrupte gef een onverwachte fout kan genereren:
#            WindowsError: exception: access violation reading 0x00000004
def Test_Gef(i_sAspect):
	return 'datmoetenwenogeensuitzoeken'

# -----------------------------------------------------------------------------
# CATEGORIE B. aanvullende helper functies
# -----------------------------------------------------------------------------

# Purpose: Converteert ISO datum tekst string (yyyy-mm-dd),
#          bv '2011-1-17', als tekst string volgens ingestelde Windows locale
# Note   : - datum is in gef bestand altijd aangegeven volgens 'ISO' standaard
#def Get_ISODate_AsText_Local(i_sISODatum):
#aap='2015-01-01'#gaat iets fout in Get_SON_MethodeSondering()
def Get_ISODate_AsText_Local(i_sISODatum):
    oListISODatum = i_sISODatum.split('-')
    iJaar = oListISODatum[0]
    iMaand = oListISODatum[1]
    iDag = oListISODatum[2]
    if iJaar is not None:
        oDate = datetime.date(int(iJaar), int(iMaand), int(iDag))
        out = oDate.strftime('%x') # format volgens ingestelde Windows locale
    try:
	return out
    except:
	return None

# Purpose: Of een gegeven report string voorkomt in de tags
#          #PROCEDURECODE dan wel #REPORTCODE.
# Parms  : Toegestane waarden zijn:
#          - 'GEF-CPT-Report'
#          - 'GEF-BORE-Report'
#          - 'GEF-BOREHOLE-Report'
# Note   : Gef2.dll herkent niet 'GEF-BOREHOLE-Report'
def Get_ReportType_Flag(headerdict,i_sReportString):
    if Get_ProcedureCode_Flag(headerdict) and \
       Get_ProcedureCode_Code(headerdict).upper() == i_sReportString.upper():
            out = True
    elif Get_ReportCode_Flag(headerdict) and \
         Get_ReportCode_Code(headerdict).upper() == i_sReportString.upper():
            out = True
    else:
        out = False
    try:
	return out
    except:
	return None

# Purpose: Geeft startdate combinatie als ISO tekst string
#           (yyyy-mm-dd), bv '2011-1-17'
# Note   :  - een geodatabase datum kolom accepteert geen Python datum object,
#             alleen een tekst string
def Get_StartDate_AsText_ISO(headerdict):
    if (Get_StartDate_Yyyy(headerdict) is not None) and (Get_StartDate_Mm(headerdict) is not None) and (Get_StartDate_Dd(headerdict) is not None):
        out = str(Get_StartDate_Yyyy(headerdict)) + '-' + \
              str(Get_StartDate_Mm(headerdict)) + '-' + \
              str(Get_StartDate_Dd(headerdict))
	try:
		print (Get_StartDate_Yyyy(headerdict))
		print (Get_StartDate_Mm(headerdict))
		print (Get_StartDate_Dd(headerdict))
		return out
	except:
		return None

# Purpose: Geeft startdate combinatie als lokale tekst string. Bij NL
#          (dd-mm-yyyy), bv '17-1-2011'
# Note   :  - een geodatabase datum kolom accepteert geen Python datum object,
#             alleen een tekst string
def Get_StartDate_AsText_Local(headerdict):
    #if (Get_StartDate_Yyyy(headerdict) == None) or (Get_StartDate_Mm(headerdict) == None) or (Get_StartDate_Dd(headerdict) == None):
    if (Get_StartDate_Yyyy(headerdict) == None) or (Get_StartDate_Mm(headerdict) == None) or (Get_StartDate_Dd(headerdict) == None):
        return None
    iJaar = Get_StartDate_Yyyy(headerdict)
    iMaand = Get_StartDate_Mm(headerdict)
    iDag = Get_StartDate_Dd(headerdict)
    if iJaar is not None:
        oDate = datetime.date(iJaar, iMaand, iDag)
        return oDate.strftime('%x') # format volgens ingestelde Windows locale
    else:
        return 'ditlijktmeeenontbreekndeinput'

def Get_StartDate_AsText_Local_new(headerdict):
    if (Get_StartDate_Yyyy(headerdict) is not None) and (Get_StartDate_Mm(headerdict) is not None) and (Get_StartDate_Dd(headerdict) is not None):
    	iJaar = Get_StartDate_Yyyy(headerdict)
    	iMaand = Get_StartDate_Mm(headerdict)
    	iDag = Get_StartDate_Dd(headerdict)
        oDate = datetime.date(iJaar, iMaand, iDag)
        out = oDate.strftime('%x') # format volgens ingestelde Windows locale
    try:
	return out
    except:
	return None

# -----------------------------------------------------------------------------
# CATEGORIE C. voor vullen kolommen gebruikt door meerdere tabellen (ALG)
# -----------------------------------------------------------------------------

# Purpose: Waarde voor kolom 'BEDRIJF' (# COMPANYID)
def Get_ALG_Bedrijf(headerdict):
    if Get_CompanyID_Flag(headerdict):
        out = Get_CompanyID_Name(headerdict)
    try:
	return out
    except:
	return None

# Purpose: Waarde voor kolom 'MV_NAP' (# ZID)
def Get_ALG_MVNAP(headerdict):
    if Get_ZID_Flag(headerdict):
        out = Get_ZID_Z(headerdict)
    try:
	return out
    except:
	return None

# Purpose: Waarde voor kolom 'PROJECTNUMMER' (# PROJECTID)
def Get_ALG_ProjectNummer(headerdict):
    if Get_ProjectID_Flag(headerdict):
        out = Get_ProjectID_Number(headerdict)
    try:
	return out
    except:
	return None

# Purpose: Waarde voor kolom 'X_RD' (# XYID)
def Get_ALG_XRD(headerdict):
    if not Get_XYID_Flag(headerdict):
        out = 0.0
    else:
        out = Get_XYID_X(headerdict)
    try:
	return out
    except:
	return None

# Purpose: Waarde voor kolom 'Y_RD' (# XYID)
def Get_ALG_YRD(headerdict):
    if not Get_XYID_Flag(headerdict):
        out = 0.0
    else:
        out = Get_XYID_Y(headerdict)
    try:
	return out
    except:
	return None

# -----------------------------------------------------------------------------
# CATEGORIE D. voor vullen kolommen gebruikt door tabel SONDERING (SON)
# -----------------------------------------------------------------------------

# Purpose: Datum van sondering (# STARTDATE)
def Get_SON_DatumSondering(headerdict):
    if Get_StartDate_Flag(headerdict):
        out = Get_StartDate_AsText_Local(headerdict)
    try:
	return out
    except:
	return None

def Get_SON_EindDiepteGegevens(headerdict):
    # Constanten en variabelen
    iQTY_SONDEERLENGTE = 1
    iQTY_GECORRIGEERDE_DIEPTE = 11

    # Verzamel details voor data block
    #iKolommenDataBlock = Get_Column(headerdict) #niet relevant lijkt me,rik
    iRijenDataBlock = Get_Nr_Scans(headerdict)
    bHasDataBlock = (iRijenDataBlock > 0)
    iKolomNrSondeerLengte = Qn2Column(iQTY_SONDEERLENGTE)
    iKolomNrGecorrDiepte = Qn2Column(iQTY_GECORRIGEERDE_DIEPTE)

    # Bepaal de einddiepte uit laatste regel data block
    try:
        bHasDataBlock in globals()
        # Neem gecorr diepte, als bekend. Anders sondeerlengte
        if iKolomNrGecorrDiepte > 0:
            sEindDiepteType = 'corrected depth'
            fEindDiepte = Get_Data(headerdict,iKolomNrGecorrDiepte, iRijenDataBlock)
        elif iKolomNrSondeerLengte > 0:
            sEindDiepteType = 'uncorrected depth'
            fEindDiepte = Get_Data(iKolomNrSondeerLengte, iRijenDataBlock)
        else:
            # Niets is aangegeven, veronderstel eerste kolom
            sEindDiepteType = 'uncorrected depth'
            fEindDiepte = Get_Data(1, iRijenDataBlock)
        return [sEindDiepteType, fEindDiepte]

    except:
	return [None, None]

# Purpose: Methode van sondering (# MEASUREMENTTEXT 4 (conus type)
def Get_SON_MethodeSondering(headerdict):
    if Get_MeasurementText_Flag(headerdict,4):
        out = Get_MeasurementText_Tekst(headerdict,4)[1] #'[1] toegevoegd ivm vermoeden rik
    try:
	return out
    except:
	return None

# -----------------------------------------------------------------------------
# CATEGORIE E. voor vullen kolommen gebruikt door tabel BORING (BOR)
# -----------------------------------------------------------------------------

# Purpose: Datum van boring (# MEASUREMENTTEXT 16)
def Get_BOR_DatumBoring(headerdict):
    if Get_MeasurementText_Flag(headerdict,16):
        sISODatum = Get_MeasurementText_Tekst(headerdict,16)[1]
        out = Get_ISODate_AsText_Local(sISODatum)
    try:
	return out
    except:
	return None

# Purpose: Einddiepte van boring (# MEASUREMENTVAR 16)
def Get_BOR_EindDiepte(headerdict):
    if Get_MeasurementVar_Flag(headerdict,16):
        out = Get_MeasurementVar_Value(headerdict,16)
    try:
	return out
    except:
	return None

# Purpose: Methode van boring (# MEASUREMENTTEXT 31)
def Get_BOR_MethodeBoring(headerdict):
    if Get_MeasurementText_Flag(headerdict,31):
        out = Get_MeasurementText_Tekst(headerdict,31)[1]
    try:
	return out
    except:
	return None

# -----------------------------------------------------------------------------
# CATEGORIE F. voor vullen kolommen gebruikt door tabel PEILBUISPUT (PBP)
# -----------------------------------------------------------------------------

# Purpose: Waarde voor kolom 'BESTAND_PARENT' (# PARENT)
def Get_PBP_BestandParent(headerdict):
    if Get_Parent_Flag(headerdict):
        out = Get_Parent_Reference(headerdict)
    try:
	return out
    except:
	return None

# Purpose: Waarde voor PBP kolom 'AANTAL_PEILBUIZEN' (# MEASUREMENTVAR 1
def Get_PBP_AantalPeilbuizen(headerdict):
    out = Get_MeasurementVar_Flag(headerdict,1)
    try:
	return int(out)
    except:
	return 0


# Purpose: Waarde voor PBP kolom 'DATUM_PLAATSING' (# MEASUREMENTTEXT 2)
def Get_PBP_DatumPlaatsing(headerdict):
    #Init_Gef()
    try:
    	out = Get_MeasurementText_Flag(headerdict,2)
        sISODatum = Get_MeasurementText_Tekst(headerdict,2)[1]
        return Get_ISODate_AsText_Local(sISODatum)
    except:
	return None

# Purpose: Bovenkant van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n-10)
def Get_PBP_Filter_Bovenkant(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n - 10
    fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr, i_iFilterNr))
    try:
    	return fResult
    except:
	return None

# Purpose: Of een bepaalde filter in een gegeven peilbuis wel voorkomt
# Note   : Naar voorbeeld code Doeke Dam
def Get_PBP_Filter_Exists(headerdict,i_iPeilbuisNr, i_iFilterNr):
    fBoven = lambda k, n: 26*k + n - 10
    fOnder = lambda k, n: 26*k + n - 5
    if Get_MeasurementVar_Flag(headerdict,fBoven(i_iPeilbuisNr, i_iFilterNr)) and \
          Get_MeasurementVar_Flag(headerdict,fOnder(i_iPeilbuisNr, i_iFilterNr)):
        bResult = True
    try:
	return bResult
    except:
        return None

# Purpose: Lengte van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n)
def Get_PBP_Filter_LengteFilter(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n
    fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr, i_iFilterNr))
    return fResult

# Purpose: Onderkant van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n-5)
def Get_PBP_Filter_Onderkant(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n - 5
    fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr, i_iFilterNr))
    try:
    	return fResult
    except:
	return None

# Purpose: Aantal filters in een gegeven peilbuis
def Get_PBP_Peilbuis_AantalFilters(headerdict,i_iPeilbuisNr):
    iCount = 1 # teller voor aantal filters
    while Get_PBP_Filter_Exists(headerdict,i_iPeilbuisNr, iCount):
        iCount += 1
    else:
        # Maak laatste optelling ongedaan
        iCount -= 1
    try:
    	return iCount
    except:
	return None

# Purpose: Bovenkant van een gegeven peilbuis (# MEASUREMENTVAR 26k-15)
def Get_PBP_Peilbuis_Bovenkant(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 15
    #fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr))
    try:
    	return fResult
    except:
	return None

# Purpose: Code van een gegeven peilbuis (# MEASUREMENTTEXT 26k-15)
def Get_PBP_Peilbuis_Code(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 15
    #sResult = None
    if Get_MeasurementText_Flag(headerdict,f(i_iPeilbuisNr)):
        sResult = Get_MeasurementText_Tekst(headerdict,f(i_iPeilbuisNr))[1] # [1] toegevoegd 07-02-2016, B. Kropf
    try:
    	return sResult
    except:
	return None

# Purpose: Lengte zandvang van een gegeven peilbuis (# MEASUREMENTVAR 26k-11)
def Get_PBP_Peilbuis_LengtePeilbuis(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 11
    #fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr))
    try:
	return sResult
    except:
	return None

# Purpose: Lengte zandvang van een gegeven peilbuis (# MEASUREMENTVAR 26k-12)
def Get_PBP_Peilbuis_LengteZandvang(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 12
    #fResult = None
    if Get_MeasurementVar_Flag(headerdict,f(i_iPeilbuisNr)):
        fResult = Get_MeasurementVar_Value(headerdict,f(i_iPeilbuisNr))
    try:
    	return fResult
    except:
	return None
