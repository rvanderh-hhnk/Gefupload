#!env/bin/python
# -----------------------------------------------------------------------------
# Name   : UtlGefOpen.py
# Purpose: Aanvullende functies voor Gef2Open.
# Note   : - Afgeleid van UtlGef.py van Paul Lauman van 13 Jul 2012
#	   - Exact dezelfde output wordt gegenereerd als door UtlGef.py
#	   - Maakt geen gebruik van Gef2.dll
#	   - Kan dus ook buiten Windows gebruikt worden
#	   - Categorie A functies zijn verwijderd. Deze staan in Gef2Open.py

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

from Gef2Open import *


# -----------------------------------------------------------------------------
# CATEGORIE B. aanvullende helper functies
# -----------------------------------------------------------------------------

# Purpose: Converteert ISO datum tekst string (yyyy-mm-dd),
#          bv '2011-1-17', als tekst string volgens ingestelde Windows locale
# Note   : - datum is in gef bestand altijd aangegeven volgens 'ISO' standaard
#def Get_ISODate_AsText_Local(i_sISODatum):
#aap='2015-01-01'#gaat iets fout in Get_SON_MethodeSondering()
def Get_ISODate_AsText_Local(i_sISODatum):
    try:
        oListISODatum = i_sISODatum.split('-')
        iJaar = oListISODatum[0]
        iMaand = oListISODatum[1]
        iDag = oListISODatum[2]
        if iJaar is not None:
            oDate = datetime.date(int(iJaar), int(iMaand), int(iDag))
            out = oDate.strftime('%x') # format volgens ingestelde Windows locale
        return out
    except:
        print (oListISODatum)
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
    if (get_startdate_Yyyy() is not None) and (get_startdate_Mm() is not None) and (get_startdate_Dd() is not None):
        out = str(get_startdate_Yyyy()) + '-' + \
              str(get_startdate_Mm()) + '-' + \
              str(get_startdate_Dd())
    try:
        print (get_startdate_Yyyy())
        print (get_startdate_Mm())
        print (get_startdate_Dd())
        return out
    except:
        return None

# Purpose: Geeft startdate combinatie als lokale tekst string. Bij NL
#          (dd-mm-yyyy), bv '17-1-2011'
# Note   :  - een geodatabase datum kolom accepteert geen Python datum object,
#             alleen een tekst string
def Get_StartDate_AsText_Local(headerdict):
    #if (get_startdate_Yyyy() == None) or (get_startdate_Mm() == None) or (get_startdate_Dd() == None):
    if (get_startdate_Yyyy() == None) or (get_startdate_Mm() == None) or (get_startdate_Dd() == None):
        return None
    iJaar = get_startdate_Yyyy()
    iMaand = get_startdate_Mm()
    iDag = get_startdate_Dd()
    if iJaar is not None:
        oDate = datetime.date(iJaar, iMaand, iDag)
        return oDate.strftime('%x') # format volgens ingestelde Windows locale
    else:
        return 'ditlijktmeeenontbreekndeinput'

def Get_StartDate_AsText_Local_new(headerdict):
    if (get_startdate_Yyyy() is not None) and (get_startdate_Mm() is not None) and (get_startdate_Dd() is not None):
        iJaar = get_startdate_Yyyy()
        iMaand = get_startdate_Mm()
        iDag = get_startdate_Dd()
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
    if get_projectid_flag():
        out = get_projectid_Number()
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
    iRijenDataBlock = get_nr_scans()
    bHasDataBlock = (iRijenDataBlock > 0)
    iKolomNrSondeerLengte = qn2column(iQTY_SONDEERLENGTE)
    iKolomNrGecorrDiepte = qn2column(iQTY_GECORRIGEERDE_DIEPTE)

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
    if get_measurementtext_flag(4):
        out = get_measurementtext_Tekst(4)[1] #'[1] toegevoegd ivm vermoeden rik
    try:
        return out
    except:
        return None

# Purpose: SondeerKlasse van sondering (# MEASUREMENTTEXT 6 (sondeer klasse)
def Get_SON_KlasseSondering(headerdict):
    if get_measurementtext_flag(6):
        out = get_measurementtext_Tekst(6)[1] #'[1] toegevoegd ivm vermoeden rik
    try:
        return out
    except:
        return None

# -----------------------------------------------------------------------------
# CATEGORIE E. voor vullen kolommen gebruikt door tabel BORING (BOR)
# -----------------------------------------------------------------------------

# Purpose: Datum van boring (# MEASUREMENTTEXT 16)
def Get_BOR_DatumBoring(headerdict):
    if get_measurementtext_flag(16):
        sISODatum = get_measurementtext_Tekst(16)
        print (sISODatum)
        # out = Get_ISODate_AsText_Local(sISODatum)
        out = sISODatum # omzetten naar ISODate_AsText_Local moet juist niet!
        try:
            datetime.datetime.strptime(out, '%Y-%m-%d') # check of waarde past.
            return out
        except Exception as e:
            return e # geeft betekenisvolle informatie terug.
    else:
        return None

# Purpose: Einddiepte van boring (# MEASUREMENTVAR 16)
def Get_BOR_EindDiepte(headerdict): # dit klopt waarschijnlijk helemaal niet.
    if get_measurementtext_flag(16):
        out = get_measurementvar_Value(16)
    try:
        return out
    except:
        return None

# Purpose: Methode van boring (# MEASUREMENTTEXT 31)
def Get_BOR_MethodeBoring(headerdict):
    if get_measurementtext_flag(31):
        out = get_measurementtext_Tekst(31) # hier [1] plaatsen = dubbelop
    try:
        return out
    except:
        return None

# -----------------------------------------------------------------------------
# CATEGORIE F. voor vullen kolommen gebruikt door tabel PEILBUISPUT (PBP)
# -----------------------------------------------------------------------------

# Purpose: Waarde voor kolom 'BESTAND_PARENT' (# PARENT)
def Get_PBP_BestandParent(headerdict):
    if get_parent_flag():
        out = get_parent_reference()
    try:
        return out
    except:
        return None

# Purpose: Waarde voor PBP kolom 'AANTAL_PEILBUIZEN' (# MEASUREMENTVAR 1
def Get_PBP_AantalPeilbuizen(headerdict):
    out = get_measurementtext_flag(1)
    try:
        return int(out)
    except:
        return 0


# Purpose: Waarde voor PBP kolom 'DATUM_PLAATSING' (# MEASUREMENTTEXT 2)
def Get_PBP_DatumPlaatsing(headerdict):
    #Init_Gef()
    try:
        out = get_measurementtext_flag(2)
        sISODatum = get_measurementtext_Tekst(2)[1]
        return Get_ISODate_AsText_Local(sISODatum)
    except:
        return None

# Purpose: Bovenkant van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n-10)
def Get_PBP_Filter_Bovenkant(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n - 10
    fResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr, i_iFilterNr))
    try:
        return fResult
    except:
        return None

# Purpose: Of een bepaalde filter in een gegeven peilbuis wel voorkomt
# Note   : Naar voorbeeld code Doeke Dam
def Get_PBP_Filter_Exists(headerdict,i_iPeilbuisNr, i_iFilterNr):
    fBoven = lambda k, n: 26*k + n - 10
    fOnder = lambda k, n: 26*k + n - 5
    if get_measurementtext_flag(fBoven(i_iPeilbuisNr, i_iFilterNr)) and \
          get_measurementtext_flag(fOnder(i_iPeilbuisNr, i_iFilterNr)):
        bResult = True
    try:
        return bResult
    except:
        return None

# Purpose: Lengte van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n)
def Get_PBP_Filter_LengteFilter(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n
    fResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr, i_iFilterNr))
    return fResult

# Purpose: Onderkant van filter in gegeven peilbuis (# MEASUREMENTVAR 26k+n-5)
def Get_PBP_Filter_Onderkant(headerdict,i_iPeilbuisNr, i_iFilterNr):
    f = lambda k, n: 26*k + n - 5
    fResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr, i_iFilterNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr, i_iFilterNr))
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
    if get_measurementtext_flag(f(i_iPeilbuisNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr))
    try:
        return fResult
    except:
        return None

# Purpose: Code van een gegeven peilbuis (# MEASUREMENTTEXT 26k-15)
def Get_PBP_Peilbuis_Code(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 15
    #sResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr)):
        print ("HALLO AANDACHT HIER"+str(get_measurementtext_Tekst(f(i_iPeilbuisNr))))
        sResult = get_measurementtext_Tekst(f(i_iPeilbuisNr)) # [1] toegevoegd 07-02-2016, B. Kropf
    try:
        return sResult
    except:
        return None

# Purpose: Lengte zandvang van een gegeven peilbuis (# MEASUREMENTVAR 26k-11)
def Get_PBP_Peilbuis_LengtePeilbuis(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 11
    #fResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr))
    try:
        return sResult
    except:
        return None

# Purpose: Lengte zandvang van een gegeven peilbuis (# MEASUREMENTVAR 26k-12)
def Get_PBP_Peilbuis_LengteZandvang(headerdict,i_iPeilbuisNr):
    f = lambda k: 26*k - 12
    #fResult = None
    if get_measurementtext_flag(f(i_iPeilbuisNr)):
        fResult = get_measurementvar_Value(f(i_iPeilbuisNr))
    try:
        return fResult
    except:
        return None

## aanvullende ProjectID functies

# note: toegevoegd op 25-02-2016, BK
# Purpose: Geeft projectnaam uit 'PROJECTID' 
def Get_ProjectID_Name(headerdict):
    if ('PROJECTID' in headerdict and len(headerdict['PROJECTID'])>0):
        out = headerdict['PROJECTID'][0]
    try:
        return out
    except:
        return None

# note: toegevoegd op 25-02-2016, BK
# Purpose: Geeft projectcode uit 'PROJECTID'
def Get_ProjectID_Code(headerdict):
    if ('PROJECTID' in headerdict and len(headerdict['PROJECTID'])>1):
        try:
            out = headerdict['PROJECTID'][1]
            return out
        except Exception as e:
            return e
    else:
        try:
            out = headerdict['PROJECTID'][0]
            return out
        except Exception as e:
            return e


# note: toegevoegd op 25-02-2016, BK
# Purpose: Geeft projectnaam uit 'PROJECTID' 
def Get_ProjectID_SubCode(headerdict):
    if ('PROJECTID' in headerdict and len(headerdict['PROJECTID'])>2):
        out = headerdict['PROJECTID'][2]
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
