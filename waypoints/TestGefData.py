#-------------------------------------------------------------------------------
# Name:         TestGefData
# Purpose:      testen van gef-data uit dictionary
#
# Author:      Bart
#
# Created:     31-10-2015
# Copyright:   (c) Bart 2015
# Licence:     to rock
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# import system modules
import os, sys
# import django modules
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User as auth_user
# import django spatial-modules
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType, SpatialReference, CoordTransform # https://docs.djangoproject.com/en/1.8/ref/contrib/gis/gdal/#ogr-geometries
# Custom modules
from waypoints.models import Waypoint, Boring, Sondering, Peilbuisput, Peilbuisgegevens, Projecten
import UtlGefOpen
from Utl import print_log 


# deel A: hoofdprogramma: gef_main, gef_standaard,
# deel B: specifieke gef_functies: gef_boringen, gef_sonderingen, gef_peilbuisputten, gef_peilbuis,  
# deel C: save functies: save_boring, save_peilbuisput, save_sondering, save_project, save_waypoint.
# deel D: nevenfuncties met korte checks en Get-functies die buiten UtlGefOpen vallen 
# deel E: overige functies: PdfCheck, ProjectCountStart, ProjectCount, send_email.
# UtlGefOpen: script voor uitlezen gef: headerdictionary en standaard Get-functies

#########################################################################################################
####################################### deel A: hoofdprogramma ##########################################
#########################################################################################################

def gef_main(request,gefFile,d_GEF):
    print ( "START")
    # 1.) standaard gef-waarden ophalen als dictionary
    d = gef_standaard(request,gefFile,d_GEF)    #{User, UserID, gefFile, gefFileNaam, CompanyID, ProjectID, 
                                                # StartDatum, SoortGef, Hyperlink_root, X, Y, Z, g}
    
    # 2.) Geometrie punt toevoegen
    d['PointGeom'] = Get_PointGeom(d)
    
    # Tests werken nog niet, dus alles op 'false'
    Test1 = False # plotable
    Test2 = False # consistent data block
    Test3 = False # correcte header
    Test4 = False # herkend als BOREHOLE/GEF-BORE/CPT-Report (boring/pbp/sondering)
    Test5 = False # beschreven als BOREHOLE/GEF-BORE/CPT-Report (boring/pbp/sondering)

    if IsCorrectBestand(request, d, d_GEF, Test1, Test2, Test3, Test4, Test5) and d['g']:
        # Boringen
        if d['SoortGef'] == 'boring':
            d = gef_boring(request,d,d_GEF)
            if d['g']:
                save_boring(request,d,d_GEF)

        # Peilbuisputten
        elif d['SoortGef'] == 'peilbuisput':
            d = gef_peilbuisput(request,d,d_GEF) #BESTAND_PARENT, BORING_ID, DATUM_PLAATSING, AANTAL_PEILBUIZEN, PROJECTNUMMER
            d = gef_peilbuis(request,d,d_GEF) #PEILBUISIDENT, BOVENKANT_PEILBUIS, LENGTE_PEILBUIS,LENGTE_ZANDVANG, 
                                                #filtergegevens: AANTAL_FILTERS, BOVENKANT_FILTER, ONDERKANT_FILTER,LENGTE_FILTER
            if d['g']:
                save_peilbuisput(request,d,d_GEF)
                save_peilbuis(request, d, d_GEF)

        # Sonderingen
        elif d['SoortGef'] == 'sondering':
            d = gef_sondering(request,d,d_GEF)
            if d['g']:
                save_sondering(request,d,d_GEF)

        # Projectgegevens en Waypoints
        if d['g']: # alleen als er geen fouten in zitten
            print ('d = oke')
            # 3.) opslaan project
            d = save_project(request, d)
            # 4.) opslaan waypoint
            d = save_waypoint(request, d)
            # 5.) Opslaan standaard gef-waarden
            return True
        else:
            return False
        
    else:
        return False
    # except TypeError:
    #     print ("TypeError")
    #     print_log(request, "ERROR", '%s niet kunnen opslaan, controleer bestand'%gefFile)
    # except:
    #     print "onverwachte error in gef_main"
 
def gef_standaard(request,gefFile,d_GEF):
    ''' Haalt de standaard gegevens op uit gef-bestanden via UtlGefOpen en geeft dictionary terug.
    Voert verschillende checks uit en genereert ook foutmeldingen.'''
    # try:
    g = True

    # User bepalen
    if request.user.is_authenticated:
        User = str(request.user) # geeft ook AnonymousUser
    else:
        User = "Onbekend"
    # UserId bepalen
    if str(request.user) == "AnonymousUser":
        UserId = 13 # opgezocht. latern misschen doen: auth_user.objects.filter(username = "Anoniem")
    else:
        UserId = request.user.id
  
    gefFileNaam = str(gefFile) #[-5:] #os.path.basename(str(gefFile)) # ipv targetPath

    # Bepalen soort gef
    #  r227 tm r234
    SoortGef = Get_SoortGef(d_GEF)
    print ("SoortGef = %s"%SoortGef)
    if SoortGef == None or SoortGef == 'onbekend':
        g = False
        # Foutmelding...
        print_log(request, "ERROR", '%s soort gef onbekend'%(gefFile))
        if 'REPORTCODE' in d_GEF:
            print ('\n'+str(d_GEF['REPORTCODE'])+'\n')
        elif 'PROCEDURECODE' in d_GEF:
            print ('\n'+str(d_GEF['PROCEDURECODE'])+'\n')
        else:
            print ('\n'+str(d_GEF)+'\n')

    # standaard veldwaarden bepalen
    # Get_CompanyID_Name UtlGefOpen
    CompanyID = UtlGefOpen.get_companyid_name()
    if CompanyID == None:
        print_log(request,"ERROR","%s CompanyID niet in orde"%(gefFile))
        print_log(request,"TIP","tip! #COMPANYID = naam bedrijf, BTW nummer, landcode")
        g = False

    # Get_ProjectID_Code 
    ProjectID = UtlGefOpen.Get_ProjectID_Code(d_GEF)
    if ProjectID == None or type(ProjectID) in [IndexError,ValueError]:
        print_log(request,"ERROR","%s Projectcode niet in orde (%s)"%(gefFile,ProjectID))
        print_log(request,"TIP","tip! #PROJECTID = projectnaam, \
                    code voor hoofdproject, code voor subproject")
        g = False
    else:
        ProjectID = ProjectID.strip()
        


    # Get_ProjectID_Name
    ProjectNaam = UtlGefOpen.Get_ProjectID_Name(d_GEF)
    if ProjectID == None:
        print_log(request,"ERROR","%s Projectnaam niet in orde"%(gefFile))
        print_log(request,"TIP","tip! #PROJECTID = projectnaam, \
                    code voor hoofdproject, code voor subproject")
        g = False
    else:
        ProjectNaam = ProjectNaam.strip()

    # Get_XYID_X
    X = UtlGefOpen.get_xyid_X()
    try:
        X = float(X)
        if X < 100000 or X > 200000:
            print_log(request,"ERROR","%s X-coordinaat buiten gebied"%(X))
            g = False
    except:
        print_log(request, "ERROR", "%s geen correcte X-coordinaat gevonden"%(gefFile))
        print_log(request, "TIP",
            """tip! #XYID = code voor referentiesysteem, X coordinaat (m),
            coordinaat (m), nauwkeurigheid X (m), nauwkeurigheid Y (m).
            code voor referentiesysteem = 31000,
            nauwkeurigheid van zowel X als Y moet zijn ingevuld""")                
        g = False

    # Get_XYID_Y
    Y = UtlGefOpen.get_xyid_Y()
    try:
        Y = float(Y)
        if Y < 400000 or Y > 600000:
            print(str(Y)+' Y-coordinaat buiten gebied')
            g = False
    except:
        print_log(request, "ERROR", "%s Y-coordinaat niet gevonden"%(gefFile))
        print_log(request, "TIP", 
            """tip! #XYID = code voor referentiesysteem, X coordinaat (m), 
            coordinaat (m), nauwkeurigheid X (m), nauwkeurigheid Y (m).
            code voor referentiesysteem = 31000, 
            nauwkeurigheid van zowel X als Y moet zijn ingevuld""") 
        g = False

    # Get_ZID_Z
    Z = UtlGefOpen.get_zid_Z()
    try:
        Z = float(Z)
        if Z < -999 or Z > 999:
            print_log(request, "ERROR","%s Z-waarde out of range"%(Z))
            g = False
    except:
        print_log(request, "ERROR", "%s Z-waarde niet gevonden"%(gefFile))
        print_log(request, "TIP", 
            """tip! #ZID = code voor referentiesysteem, vert. positie maaiveld
            t.o.v. referentiesysteem (m), nauwkeurigheid (m)""")
        g = False

    # StartDatum
    StartDatum = UtlGefOpen.Get_StartDate_AsText_ISO(d_GEF) #gef.Get_StartDate_AsText_Local(d_GEF)
    print ("Startdatum: %s"%(StartDatum))
    if StartDatum == None:
        print_log(request, "ERROR", "%s StartDatum niet orde"%(gefFile))
        g = False
    Hyperlink_root = Get_hyperlink_root(request)

    # Bepaal ReportType voor Test4 en Test5 IsbestandCorrect
    if SoortGef == 'boring': 
        ReportType = 'GEF-BOREHOLE-Report'
    elif SoortGef == 'peilbuisput':
        ReportType = 'GEF-BORE-Report'
    elif SoortGef == 'sondering':
        ReportType = 'GEF-CPT-Report'
    else:
        g = False # maar dat weten we inmiddels al...
        ReportType = None
    # Stop resultaten in dict
    d = {}
    d['User'] = User
    d['UserId'] = UserId
    d['gefFile'] = gefFile
    d['gefFileNaam'] = gefFileNaam
    d['CompanyID'] = CompanyID
    d['ProjectID'] = ProjectID
    d['ProjectNaam'] = ProjectNaam
    d['StartDatum'] = StartDatum
    d['SoortGef'] = SoortGef
    d['Hyperlink_root'] = Hyperlink_root
    d['ReportType'] = ReportType
    d['X'] = X
    d['Y'] = Y
    d['Z'] = Z
    d['g'] = g
    for i in d:
        print ("%s: %s"%(i,d[i]))
    return d

    # except IOError:
    #     print ("IOError")
    #     print (gefFile)
    #     return None
    # except TypeError:
    #     print ("TypeError")
    #     return None
    # except:
    #     print_log(request, "ERROR", "%s: Een onverwachte fout heeft zich voorgedaan in gef_standaard"%(gefFile))
    #     return None

#########################################################################################################
################################## deel B: spefifieke gef-functies#######################################
#########################################################################################################

def gef_boring(request,d,d_GEF):
    """Haalt specifieke boring-attributen op, controleert en geeft indien nodig foutmeldingen."""

    gefFile = d['gefFile']
    
    # Datum Boring #MEASUREMENTTEXT = 16, yyyy-mm-dd, datum boring
    DatumBoring = UtlGefOpen.Get_BOR_DatumBoring(d_GEF) # zette eerst om naar '01/31/15', maar geeft nu origineel terug '2015-01-31'.
    # DatumBoring = Convert_Date(DatumBoring) # DateField = 'YYYY-MM-DD' ipv 'MM/DD/YY'. niet meer nodig, Get_BOR_DatumBoring aangepast.
    if type(DatumBoring) == ValueError or DatumBoring is None:
        d['g'] = False
        print_log(request, "ERROR", '%s: Geen correcte datum boring gevonden! %s'%(gefFile,DatumBoring))
        print_log(request, "TIP", "tip! #MEASUREMENTTEXT = 16, yyyy-mm-dd, datum boring")
    else:
        d['DATUM_BORING'] = DatumBoring

    # Get_BOR_MethodeBoring
    METHODE_BORING = UtlGefOpen.Get_BOR_MethodeBoring(d_GEF)
    if METHODE_BORING != None:
        d['METHODE_BORING'] = METHODE_BORING 
    else:
        d['g'] = False
        print_log(request, "ERROR", '%s: Geen correcte METHODE_BORING gevonden!'%(gefFile))
    
    # Get_BOR_EindDiepte Einddiepte t.o.v. NAP: #MEASUREMENTVAR = 29+2k, [diepte], m, diepte onderkant boortraject tov maaiveld.
    # Omrekenen naar einddiepte tov NAP = #ZID(2) - #MEASUREMENTVAR = 29+2k (1)
    try:
        EINDDIEPTE = UtlGefOpen.Get_BOR_EindDiepte(d_GEF)
        EINDDIEPTE = float(EINDDIEPTE)
        d['EINDDIEPTE'] = EINDDIEPTE
    except:
        # d['g'] = False # tijdelijke maatregel.
        d['EINDDIEPTE'] = None
        print_log(request, "ERROR", '%s: Geen correcte einddiepte gevonden! %s'%(gefFile,EINDDIEPTE))
        print_log(request, "TIP", """Tip! Einddiepte t.o.v. NAP: #MEASUREMENTVAR = 
                                    29+2k, [diepte], m, diepte onderkant boortraject tov maaiveld.""")
    
    
        

    return d


def gef_sondering(request,d,d_GEF):
    """Haalt specifieke sondering-attributen op, controleert en geeft indien nodig foutmeldingen."""
    gefFile = d['gefFile']

    d['BESTAND_SONDERING'] = d['gefFileNaam'] # bestandsnaam
    d['DATUM_SONDERING'] = d['StartDatum'] # i.p.v. UtlGef.Get_SON_DatumSondering()
    
    # Methode Sondering #MEASUREMENTVAR = 12, [number], -, type of penetration test
    METHODE_SONDERING = UtlGefOpen.Get_SON_MethodeSondering(d_GEF)
    domain_METHODE_SONDERING = ["0","1","2","3","4","5"]
    if METHODE_SONDERING in domain_METHODE_SONDERING:
        d['METHODE_SONDERING'] = METHODE_SONDERING
    elif METHODE_SONDERING != None: # wel waarde, maar niet in domain
        d['g'] = False
        print_log(request, "ERROR", '%s: De methode_sondering (%s) komt niet voor in domein: %s'%(gefFile,METHODE_SONDERING,domain_METHODE_SONDERING))
        print_log(request, "TIP", """tip! #MEASUREMENTVAR = 12, [number], -, type of penetration test
                                    Voorbeeld: #MEASUREMENTVAR= 12, 0.000000, -, elektrische sondering""")    
    else: # None waarde, geen methode gevonden.
        d['g'] = False
        print_log(request, "ERROR", '%s: Geen correcte methode_sondering gevonden! %s'%(gefFile,METHODE_SONDERING))
        print_log(request, "TIP", """tip! #MEASUREMENTVAR = 12, [number], -, type of penetration test
                                    Voorbeeld: #MEASUREMENTVAR= 12, 0.000000, -, elektrische sondering""")
    
    # Sondeer klasse #MEASUREMENTTEXT = 6, [text], according to standard NEN 5140 
    SONDEERKLASSE = UtlGefOpen.Get_SON_KlasseSondering(d_GEF)
    if SONDEERKLASSE != None:
        d['SONDEERKLASSE'] = SONDEERKLASSE
    else:
        d['g'] = False
        print_log(request, "ERROR", '%s: Geen correcte sondeerklasse gevonden! %s'%(gefFile,SONDEERKLASSE))
        print_log(request, "TIP", """tip! #MEASUREMENTTEXT = 6, [text], according to standard NEN 5140 incl. Class\, NEN 3680,... """)
    
    # Einddiepte type #COLUMNINFO = 7, m, corrected depth, 11 
    EINDDIEPTE_TYPE = UtlGefOpen.Get_SON_EindDiepteGegevens(d_GEF)[0]
    if EINDDIEPTE_TYPE != None: # and EINDDIEPTE_TYPE.lower() in ['gecorrigeerd', 'niet gecorrigeerd']:
        d['EINDDIEPTE_TYPE'] = EINDDIEPTE_TYPE
    else:
        #d['g'] = False
        d['EINDDIEPTE_TYPE'] = None
        print_log(request, "ERROR", '%s: (werkt nog niet) Geen correcte einddiepte_type gevonden! %s'%(gefFile,EINDDIEPTE_TYPE))
        print_log(request, "TIP", """tip! #COLUMNINFO = 7, m, corrected depth, 11 """) 

    # Einddiepte #MEASUREMENTVAR = 16, [figure], m, end depth of penetration test
    EINDDIEPTE = UtlGefOpen.Get_SON_EindDiepteGegevens(d_GEF)[1]
    if EINDDIEPTE != None:
        d['EINDDIEPTE'] = EINDDIEPTE
    else:
        #d['g'] = False
        d['EINDDIEPTE'] = None
        print_log(request, "ERROR", '%s: (werkt nog niet) Geen correcte einddiepte gevonden! %s'%(gefFile,EINDDIEPTE))
        print_log(request, "TIP", """tip! #MEASUREMENTVAR = 16, [figure], m, end depth of penetration test """) 

    return d

def gef_peilbuisput(request,d,d_GEF):
    gefFile = d['gefFile']
    # voor specifieke peilbuisput-attributen
    # sPeilbuisputID = sFORMATSTRING % iMaxID, b.k.note: is dit nodig om zelf hier te bepalen of leiden we ID gewoon af na het invoeren?
    # BESTAND_PEILBUISPUT = sGefBestand # bestandsnaam, b.k.note: bestandsnaam weten we al.
    BESTAND_PARENT = UtlGefOpen.Get_PBP_BestandParent(d_GEF)
    BORING_ID = Get_BoringID(BESTAND_PARENT)
    print("BORING_ID = %s"%BORING_ID)
    if not BORING_ID == None:
        BORING_ID = int(BORING_ID)
    PROJECTNUMMER = UtlGefOpen.Get_ALG_ProjectNummer(d_GEF)
    DATUM_PLAATSING = UtlGefOpen.Get_PBP_DatumPlaatsing(d_GEF)
    AANTAL_PEILBUIZEN = UtlGefOpen.Get_PBP_AantalPeilbuizen(d_GEF)
    print(PROJECTNUMMER,DATUM_PLAATSING,AANTAL_PEILBUIZEN)
    # Vul de bijbehorende peilbuisgegevens
    # VulTblPb(i_oGp, i_sPadTargetTblPb, sPeilbuisputID, i_sPadTargetTblFt)
    # iCountPunten += 1
    if BESTAND_PARENT == None or BORING_ID == None:
        print ("geen parent gevonden")
        print_log(request, "ERROR", '%s Parent (boring) niet gevonden!'%(gefFile))
        d['g'] = False

    d['BESTAND_PARENT'] = BESTAND_PARENT
    d['BORING_ID'] = BORING_ID
    d['DATUM_PLAATSING'] = DATUM_PLAATSING
    d['AANTAL_PEILBUIZEN'] = AANTAL_PEILBUIZEN
    d['PROJECTNUMMER'] = PROJECTNUMMER
    return d

    # Print ('\nTotaal aantal GEF bestanden in folder : %6i' % len(oListGefBestanden))
    # Print ('Aantal peilbuisput locaties toegevoegd: %6i' % iCountPunten)
    # Print ('- met daarin aantal peilbuizen        : %6i' % iCountPb)
    # Print ('- met daarin aantal filters           : %6i' % iCountFt)

def gef_peilbuis(request,d,d_GEF):
    iAantalPeilbuizen = d['AANTAL_PEILBUIZEN']
    for k in range(1, iAantalPeilbuizen + 1):
        # zelf verzonnen unieke code voor PEILBUISIDENT
        PEILBUISIDENT = d['gefFileNaam'][:-4] + "_Peilbuis" + str(UtlGefOpen.Get_PBP_Peilbuis_Code(d_GEF,k))
        BOVENKANT_PEILBUIS = UtlGefOpen.Get_PBP_Peilbuis_Bovenkant(d_GEF,k)
        LENGTE_PEILBUIS = UtlGefOpen.Get_PBP_Peilbuis_LengtePeilbuis(d_GEF,k)
        LENGTE_ZANDVANG = UtlGefOpen.Get_PBP_Peilbuis_LengteZandvang(d_GEF,k)
        AANTAL_FILTERS = UtlGefOpen.Get_PBP_Peilbuis_AantalFilters(d_GEF,k)
        #filtergegevens
        i_iFilterNr = 1 # altijd 1 filter
        BOVENKANT_FILTER = UtlGefOpen.Get_PBP_Filter_Bovenkant(d_GEF, k, i_iFilterNr)
        ONDERKANT_FILTER = UtlGefOpen.Get_PBP_Filter_Onderkant(d_GEF, k, i_iFilterNr)
        LENGTE_FILTER = UtlGefOpen.Get_PBP_Filter_LengteFilter(d_GEF, k, i_iFilterNr)
        # FILTER_ID = sFilterID # komt straks bij het opslaan aan bod
        # PEILBUIS_ID = i_sPeilbuisID
        d['PEILBUISIDENT'+str(k)] = PEILBUISIDENT
        d['BOVENKANT_PEILBUIS'+str(k)] = BOVENKANT_PEILBUIS 
        d['LENGTE_PEILBUIS'+str(k)] = LENGTE_PEILBUIS
        d['LENGTE_ZANDVANG'+str(k)] = LENGTE_ZANDVANG
        d['AANTAL_FILTERS'+str(k)] = AANTAL_FILTERS
        #filtergegevens
        d['BOVENKANT_FILTER'+str(k)] = BOVENKANT_FILTER         
        d['ONDERKANT_FILTER'+str(k)] = ONDERKANT_FILTER
        d['LENGTE_FILTER'+str(k)] = LENGTE_FILTER
    return d


#########################################################################################################
################################## deel C: spefifieke save-functies #####################################
#########################################################################################################

def save_boring(request, d, d_GEF):
    # try:
    gefFileNaam = d['gefFileNaam']
    gefFile = d['gefFile']
    CompanyID = d['CompanyID']
    ProjectID = d['ProjectID']
    ProjectNaam = d['ProjectNaam']
    StartDatum = d['StartDatum']
    SoortGef = d['SoortGef']
    Hyperlink_root = d['Hyperlink_root']
    PointGeom = d['PointGeom']
    User = d['User']
    X = d['X']
    Y = d['Y']
    Z = d['Z']
    g = d['g']
    # boring specifiek
    DATUM_BORING = d['DATUM_BORING']
    METHODE_BORING = d['METHODE_BORING']
    EINDDIEPTE = d['EINDDIEPTE']

    if Boring.objects.filter(bestand_gef=gefFileNaam).exists():
        # update row
        print ("Boring %s updaten..."%(gefFileNaam))
        b = Boring.objects.get(bestand_gef=gefFileNaam)
        # boring_id = # automatisch bepaald 
        b.boringident = None
        b.x_rd = X
        b.y_rd = Y
        b.mv_nap = Z
        b.dwarspositie = None
        b.datum_boring = DATUM_BORING
        b.bedrijf = CompanyID
        b.project_id = ProjectID
        b.project_naam = ProjectNaam
        b.startdatum = StartDatum
        b.type_boring = None
        b.methode_boring = METHODE_BORING
        b.einddiepte = EINDDIEPTE
        # b.bestand_boring # klopt dit?? is dit niet gewoon bestand_gef?
        # bestand_pdf # deze komt bij save_pdf() aan bod 
        b.bestand_gef = gefFileNaam
        b.bestand_grondonderzoek = None
        b.bestanden_corsa = None
        b.monstername = None
        b.bestand_labproeven = None
        b.gef_file = gefFile # dit is filefield: voor het opslaan van bronbestand 
        b.gef_file_bf = None # ??
        b.download_gef = (Hyperlink_root+gefFileNaam)
        # status = # automatisch ingevuld 
        # DateCreated = # automatisch ingevuld
        # DateMutated = # automatisch ingevuld
        b.username = User
        b.geometry = PointGeom
        b.save()

    else:
        # insert new row
        boring = Boring(
            # boring_id = # automatisch bepaald 
            boringident = None,
            x_rd = X,
            y_rd = Y,
            mv_nap = Z,
            dwarspositie = None,
            datum_boring = DATUM_BORING,
            bedrijf = CompanyID,
            project_id = ProjectID,
            project_naam = ProjectNaam,
            startdatum = StartDatum,
            type_boring = None,
            methode_boring = METHODE_BORING,
            einddiepte = EINDDIEPTE,
            # bestand_boring = gefFileNaam, # klopt dit??
            # bestand_pdf, = deze komt bij save_pdf() aan bod. Hier niet aankomen 
            bestand_gef = gefFileNaam,
            bestand_grondonderzoek = None,
            bestanden_corsa = None,
            monstername = None,
            bestand_labproeven = None,
            gef_file = gefFile, # dit is filefield: voor het opslaan van bronbestand 
            gef_file_bf = None, # ??
            download_gef = (Hyperlink_root+gefFileNaam),
            # status, = # automatisch ingevuld 
            # DateCreated, = # automatisch ingevuld
            # DateMutated, = # automatisch ingevuld
            username = User,
            geometry = PointGeom
        ) 
        #gef_file_bf=open('/var/www/'+str(gefFile)), Exception Value: can't escape file to binary
        boring.save()
    # except:
    #     print_log(request, "ERROR", '%s: onverwachte fout bij opslaan boring!'%(gefFileNaam))

def save_sondering(request, d, d_GEF):
    # Sondering
    # try:
    gefFileNaam = d['gefFileNaam']
    gefFile = d['gefFile']
    CompanyID = d['CompanyID']
    ProjectID = d['ProjectID']
    ProjectNaam = d['ProjectNaam']
    StartDatum = d['StartDatum']
    SoortGef = d['SoortGef']
    MethodeSondering = d['METHODE_SONDERING']
    EinddiepteType = d['EINDDIEPTE_TYPE'] 
    Einddiepte = d['EINDDIEPTE'] 
    Hyperlink_root = d['Hyperlink_root']
    PointGeom = d['PointGeom']
    User = d['User']
    X = d['X']
    Y = d['Y']
    Z = d['Z']
    g = d['g']
    if Sondering.objects.filter(bestand_gef=gefFileNaam).exists():
        print ("Sondering %s bestaat al"%(gefFileNaam))
        s = Sondering.objects.get(bestand_gef=gefFileNaam)
        s.bestand_gef=gefFileNaam
        s.download_gef=(Hyperlink_root+gefFileNaam)
        s.bedrijf=CompanyID
        s.project_id=ProjectID
        s.project_naam = ProjectNaam
        s.startdatum = StartDatum
        s.datum_sondering= StartDatum
        s.dwarspositie = None
        s.sondeerklasse = None
        s.type_sondeeronderzoek = None
        s.methode_sondering = MethodeSondering
        s.einddiepte = Einddiepte
        s.type_einddiepte = EinddiepteType
        s.voorboring_aanwezig = None
        s.bestand_sondering = None
        s.bestand_pdf = None
        s.bestand_grondonderzoek = None
        s.bestanden_corsa = None
        # status = # automatisch ingevuld 
        # DateCreated = # automatisch ingevuld
        # DateMutated = # automatisch ingevuld
        s.username=User
        s.x_rd=X
        s.y_rd=Y
        s.mv_nap=Z
        s.gef_file=gefFile # FileField, dient ter opslag van bijlages in media folder.
        s.geometry=PointGeom
        s.save()   

        #print_log(request, "SUCCESS", '%s: succesvol overschreven!'%gefFile) # bericht komt bij waypoint
    else: # object bestaat nog niet
        s = Sondering(
            bestand_gef=gefFileNaam, 
            download_gef=(Hyperlink_root+gefFileNaam), 
            bedrijf=CompanyID, 
            project_id=ProjectID,
            project_naam=ProjectNaam,
            startdatum = StartDatum,
            datum_sondering=StartDatum, 
            dwarspositie = None,
            sondeerklasse = None,
            type_sondeeronderzoek = None,
            methode_sondering = MethodeSondering,
            einddiepte = Einddiepte,
            type_einddiepte = EinddiepteType,
            voorboring_aanwezig = None,
            bestand_sondering = None,
            bestand_pdf = None,
            bestand_grondonderzoek = None,
            bestanden_corsa = None,
            # status = # automatisch ingevuld 
            # DateCreated = # automatisch ingevuld
            # DateMutated = # automatisch ingevuld
            username=User, 
            x_rd=X, 
            y_rd=Y, 
            mv_nap=Z, 
            gef_file=gefFile, 
            geometry=PointGeom)
        s.save()
    # except:
    #     print_log(request, "ERROR", '%s: onverwachte fout bij opslaan sondering!'%gefFile)

def save_peilbuisput(request, d, d_GEF):
    # Peilbuisput
    # try:
    gefFileNaam = d['gefFileNaam']
    gefFile = d['gefFile']
    CompanyID = d['CompanyID']
    ProjectID = d['ProjectID']
    ProjectNaam = d['ProjectNaam']
    StartDatum = d['StartDatum']
    SoortGef = d['SoortGef']
    Hyperlink_root = d['Hyperlink_root']
    PointGeom = d['PointGeom']
    User = d['User']
    X = d['X']
    Y = d['Y']
    Z = d['Z']
    g = d['g']
    # Peilbuisput specifiek
    BESTAND_PARENT = d['BESTAND_PARENT']
    BORING_ID = d['BORING_ID']
    DATUM_PLAATSING = d['DATUM_PLAATSING']
    AANTAL_PEILBUIZEN = d['AANTAL_PEILBUIZEN']
    PROJECTNUMMER = d['PROJECTNUMMER']
    
    # print (Peilbuisput.objects.get(bestand_gef=gefFileNaam))
    if Peilbuisput.objects.filter(bestand_gef=gefFileNaam).exists() and g == True:
        # update row
        print ("Peilbuisput %s bestaat al"%(gefFileNaam))
        p = Peilbuisput.objects.get(bestand_gef=gefFileNaam)
        print (p)
        p.status = "test"
        p.boreholeident = None
        p.boring_id_id = BORING_ID
        p.peilbuisraai_id   = None
        p.x_rd = X
        p.y_rd = Y
        p.mv_nap = Z
        p.dwarspositie = None
        p.datum_plaatsing   = StartDatum #DATUM_PLAATSING moet nog omgezet worden naar 'yymmdd'
        p.datum_verwijdering = None
        p.aanwezig = None
        p.bedrijf   = CompanyID
        p.project_id = ProjectID
        p.project_naam = ProjectNaam
        p.startdatum = StartDatum
        p.type_peilbuisput = None
        p.locatiebeschrijving = None 
        p.reden_plaatsing = None
        p.aantal_peilbuizen = AANTAL_PEILBUIZEN
        p.bestand_peilbuisput   = None
        p.bestand_parent = BESTAND_PARENT
        p.bestand_gef = gefFileNaam
        p.bestand_txt = None
        p.bestand_grondonderzoek = None
        p.gef_file = gefFile
        p.download_gef = (Hyperlink_root+gefFileNaam)
        # p.status = # automatisch ingevuld 
        # p.DateCreated = # automatisch ingevuld
        # p.DateMutated = # automatisch ingevuld
        p.username = User
        p.geometry = PointGeom
        p.save()
        #print_log(request, "SUCCESS", '%s: succesvol overschreven!'%gefFile) # bericht komt bij waypoint
    else:
        # insert new row
        p = Peilbuisput(
            boreholeident = None,
            boring_id_id = BORING_ID,
            peilbuisraai_id = None,
            x_rd = X,
            y_rd = Y,
            mv_nap = Z,
            dwarspositie = None,
            datum_plaatsing = StartDatum, #DATUM_PLAATSING moet nog omgezet worden naar 'yymmdd'
            datum_verwijdering = None,
            aanwezig = None,
            bedrijf = CompanyID,
            project_id = ProjectID,
            project_naam = ProjectNaam,
            startdatum = StartDatum,
            type_peilbuisput = None,
            locatiebeschrijving = None, 
            reden_plaatsing = None,
            aantal_peilbuizen = AANTAL_PEILBUIZEN,
            bestand_peilbuisput = None,
            bestand_parent = BESTAND_PARENT,
            bestand_gef = gefFileNaam,
            bestand_txt = None,
            bestand_grondonderzoek = None,
            gef_file = gefFile,
            download_gef = (Hyperlink_root+gefFileNaam),
            # status = # automatisch ingevuld 
            # DateCreated = # automatisch ingevuld
            # DateMutated = # automatisch ingevuld
            username = User,
            geometry = PointGeom
        )
        p.save()
    # except:
    #     print_log(request, "ERROR", '%s: onverwachte fout bij opslaan peilbuisput!'%gefFile)

def save_peilbuis(request,d,d_GEF):
    BESTAND_PARENT = d['gefFileNaam']
    gefFileNaam = BESTAND_PARENT
    iAantalPeilbuizen = d['AANTAL_PEILBUIZEN']
    User = d['User']
    PointGeom = d['PointGeom']
    ProjectID = d['ProjectID']
    ProjectNaam = d['ProjectNaam']

    # Get peilbuisputID
    PeilbuisputID = Get_PeilbuisputID(BESTAND_PARENT)
    if PeilbuisputID == None:
        print_log(request, "ERROR", '%s: Parent (Peilbuisput) niet gevonden!'%(BESTAND_PARENT))
    else:
        print ("PeilbuisputID = %s: "%(PeilbuisputID))
        PeilbuisputID = int(PeilbuisputID)
        # moet hier per se een instance van maken, gewoon ID als integer is niet voldoende
        PeilbuisputID = Peilbuisput.objects.get(id=PeilbuisputID)
        print (PeilbuisputID)
        for k in range(1, iAantalPeilbuizen + 1):
            PEILBUISIDENT = d['PEILBUISIDENT'+str(k)]
            BOVENKANT_PEILBUIS = d['BOVENKANT_PEILBUIS'+str(k)]
            LENGTE_PEILBUIS = d['LENGTE_PEILBUIS'+str(k)]
            LENGTE_ZANDVANG = d['LENGTE_ZANDVANG'+str(k)]
            AANTAL_FILTERS = d['AANTAL_FILTERS'+str(k)]
            #filtergegevens
            BOVENKANT_FILTER = d['BOVENKANT_FILTER'+str(k)]         
            ONDERKANT_FILTER = d['ONDERKANT_FILTER'+str(k)]
            LENGTE_FILTER = d['LENGTE_FILTER'+str(k)]
            
            if Peilbuisgegevens.objects.filter(peilbuisident=PEILBUISIDENT).exists():
                # update row
                print ("Peilbuis %s overschrijven..."%PEILBUISIDENT)
                p = Peilbuisgegevens.objects.get(peilbuisident=PEILBUISIDENT)
                # peilbuis_id = automatisch aangemaakt
                p.peilbuisident = PEILBUISIDENT
                p.borehole_id = PeilbuisputID
                p.project_id = ProjectID
                p.project_naam = ProjectNaam
                p.bovenkant_peilbuis = BOVENKANT_PEILBUIS
                p.lengte_peilbuis = LENGTE_PEILBUIS
                p.lengte_zandvang = LENGTE_ZANDVANG
                p.binnendiameter_mm = None # ???
                p.bovenkant_filter = BOVENKANT_FILTER
                p.onderkant_filter = ONDERKANT_FILTER
                p.lengte_filter = LENGTE_FILTER
                p.bestand_meetreeks = BESTAND_PARENT # klopt dit?
                # status = # automatisch ingevuld 
                # DateCreated = # automatisch ingevuld
                # DateMutated = # automatisch ingevuld
                p.username = User
                p.geometry = PointGeom
                p.save()
                print_log(request, "SUCCESS", '%s: peilbuis %s succesvol overschreven!'%(gefFileNaam,PEILBUISIDENT))
            else:
                p = Peilbuisgegevens(    
                # peilbuis_id = automatisch aangemaakt
                peilbuisident = PEILBUISIDENT,
                borehole_id = PeilbuisputID,
                project_id = ProjectID,
                project_naam = ProjectNaam,
                bovenkant_peilbuis = BOVENKANT_PEILBUIS,
                lengte_peilbuis = LENGTE_PEILBUIS,
                lengte_zandvang = LENGTE_ZANDVANG,
                binnendiameter_mm = None, # ???
                bovenkant_filter = BOVENKANT_FILTER,
                onderkant_filter = ONDERKANT_FILTER,
                lengte_filter = LENGTE_FILTER,
                bestand_meetreeks = BESTAND_PARENT, # klopt dit?
                # status = # automatisch ingevuld 
                # DateCreated = # automatisch ingevuld
                # DateMutated = # automatisch ingevuld
                username = User,
                geometry = PointGeom
                )
                p.save()
                print_log(request, "SUCCESS", '%s: peilbuis %s succesvol opgeslagen!'%(gefFileNaam,PEILBUISIDENT))

def save_waypoint(request, d):
    # try:
    # Waypoint
    User = d['User']
    gefFile = d['gefFile']
    gefFileNaam = d['gefFileNaam']
    CompanyID = d['CompanyID']
    ProjectID = d['ProjectID']
    ProjectNaam = d['ProjectNaam']
    StartDatum = d['StartDatum']
    SoortGef = d['SoortGef']
    Hyperlink_root = d['Hyperlink_root']
    PointGeom = d['PointGeom']
    X = d['X']
    Y = d['Y']
    Z = d['Z']
    # Check of waypoint al bestaat
    if Waypoint.objects.filter(name=gefFileNaam).exists():
        print ("Waypoint %s bestaat al"%(gefFileNaam))
        w = Waypoint.objects.get(name=gefFileNaam)
        w.name=gefFileNaam
        w.download_gef=(Hyperlink_root+gefFileNaam)
        w.company=CompanyID
        w.projectid=ProjectID
        w.project_naam = ProjectNaam
        w.startdatum=StartDatum
        w.username=User
        w.soortgef=SoortGef
        w.x=X
        w.y=Y
        w.z=Z
        w.geometry=PointGeom
        w.save()
        print_log(request, "SUCCESS", '%s: succesvol overschreven!'%gefFile)
    # Waypoint bestaat nog niet. nieuw object opslaan
    else:
        waypoint = Waypoint(
            name=gefFileNaam, 
            download_gef=(Hyperlink_root+gefFileNaam), 
            company=CompanyID, 
            project_id=ProjectID,
            project_naam = ProjectNaam,
            startdatum=StartDatum, 
            username=User, 
            soortgef=SoortGef, 
            x=X, 
            y=Y, 
            z=Z, 
            geometry=PointGeom)
        waypoint.save()
        print_log(request, "SUCCESS", '%s: upload succesvol!'%(gefFileNaam))

    # except:
    #     print_log(request, "ERROR", '%s: onverwachte fout bij opslaan waypoint!'%(gefFileNaam))


def save_project(request, d):
    ProjectID = d['ProjectID'] 
    ProjectNaam = d['ProjectNaam']
    UserId = d['UserId']
    # Projecten
    # optie 1) project hoort altijd bij 1 gebruiker
    # check of project al bestaat onder andere gebruiker
    if Projecten.objects.filter(project_id = ProjectID).exists() and not Projecten.objects.filter(project_id = ProjectID, user_id_id = UserId).exists():
        print_log(request, "ERROR", 'Project: %s al in gebruik door andere gebruiker'%ProjectID)
        d['g'] = False
    # check of project al bestaat voor huidige gebruiker
    if not Projecten.objects.filter(project_id = ProjectID).exists():
        print ("save new project with %s %s "%(ProjectID,UserId))
        project = Projecten(
            project_id=ProjectID,
            project_name = ProjectNaam, # moet nog een keer aanpassen naar 'project_naam'
            user_id_id=UserId, 
            username=request.user.username)
        project.save()
    return d
    # optie 2) gedeeld projecten: kan verschillende gebruikers hebben. geen constraint
    ## if Projecten.objects.filter(project_name = ProjectID, user_id_id = UserId).exists() == False and g == True:  #if Projecten.objects.get(id=files_id)


##############################################################################################
################ deel D: Get-functies en korte checks ########################################
##############################################################################################

def Get_PointGeom(d):
    if d['g']:
        X = d['X']
        Y = d['Y']
        Z = d['Z']
        wkt = 'POINT(%f %f)'%(X,Y) # z niet ondersteund in geometry kennelijk...
        oPoint = OGRGeometry(wkt, SpatialReference('EPSG:28992'))
        oPoint.transform_to(SpatialReference('WGS84')) # transform van RD_NEW naar WGS84
        PointGeom = oPoint.wkt
        return PointGeom
    else:
        return None
       

def Get_hyperlink_root(request):
    try:
        # Site URL for hyperlinkfield
        SiteURL = request.build_absolute_uri()[:-len(request.get_full_path())] # global in views.index werkt niet...
        if SiteURL[-5:] == ":8000": # testomgeving
            Hyperlink_root = SiteURL + '/media/'
        else: # productieomgeving
            Hyperlink_root = SiteURL + '/static/gefupload/media/'
        return Hyperlink_root
    except:
        return None

# -----------------------------------------------------------------------------
# Purpose: Haal uit fc BORING het ID dat hoort bij de opgegeven parent-
#          bestandsnaam
# -----------------------------------------------------------------------------
def Get_BoringID(BESTAND_PARENT):
	# Maximale afstand tussen peilbuisput en parent-boring
	fMAX_AFSTAND = 10.0
	sResult = None
	iCount = 0
	print ("zoekt "+str(BESTAND_PARENT)+" in Boringen.bestand_gef")
	q = Boring.objects.all().filter(bestand_gef = BESTAND_PARENT)
	if len(q)>0:
		print ("%i boringen gevonden met %s"%(len(q),BESTAND_PARENT))
		q = q[0]
		sResult = q.id
	return sResult

def Get_PeilbuisputID(BESTAND_PARENT):
    sResult = None
    print ("zoekt "+str(BESTAND_PARENT)+" in Peilbuisput.bestand_gef")
    q = Peilbuisput.objects.all().filter(bestand_gef = BESTAND_PARENT)
    if len(q)>0:
        print ("%i peilbuisputten gevonden met %s"%(len(q),BESTAND_PARENT))
        q = q[0]
        sResult = q.id
    return sResult

# Paul L. checks
def IsCorrectBestand(request, d, d_GEF, Test1, Test2, Test3, Test4, Test5):
    gefFile = d['gefFile']
    ReportType = d['ReportType']
    bIsOK = True
    if Test1: # Of bestand basisinfo bevat om te plotten
        if not UtlGefOpen.is_plotable(d_GEF):
            print_log(request, "ERROR", '%s: kan niet worden geplot.'%gefFile)
            return False
    if Test2: # Of data block consistent met header
        if not UtlGefOpen.test_gef(d_GEF):
            print_log(request, "ERROR", '%s: heeft inconsistent data block.'%gefFile)
            return False
    if Test3: # Of header (alle keywords) correct
        if not UtlGefOpen.test_gef(d_GEF):
            print_log(request, "ERROR", '%s: heeft incorrecte header.'%gefFile)
            return False
    if Test4: # Of herkend als BORHOLE/BORE/CPT bestand
        if not UtlGefOpen.get_reporttype_flag(ReportType):
            print_log(request, "ERROR", '%s: niet herkend als %s.'%(gefFile,ReportType))
            return False
    if Test5: # Of beschreven als BORHOLE/BORE/CPT bestand
        if not UtlGefOpen.get_reporttype_flag(ReportType):
            print_log(request, "ERROR", '%s: niet beschreven als %s.'%(gefFile,ReportType))
            return False
    return bIsOK

# Bart TestGefData r227 tm r234
def Get_SoortGef(headerdict):
    if  UtlGefOpen.gbr_is_gbr():
        SoortGef='boring' 
    elif UtlGefOpen.gcr_is_gcr(): 
        SoortGef='sondering' 
    elif UtlGefOpen.Brh_Is_Brh(headerdict): # niet in Gef2Open.py
        SoortGef='peilbuisput'
    else: 
        SoortGef='onbekend'
        print ("soort gef onbekend")
        print_log(request, "ERROR", '%s: Soort GEF (boring, sondering of peilbuisput) niet kunnen achterhalen.'%(gefFile))
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
def Convert_Date(date):  # '01/31/15'
    try:
        # omdraaien voor DateField YYYY-MM-DD ipv 'MM/DD/YY'
        datum = '20'+date[6:8]+'-'+date[0:2]+'-'+date[3:5] # '2015-01-31'
        return datum
    except:
        return None


##############################################################################################
############################### deel E: overige functies #####################################
##############################################################################################

def pdf_check(request, pdfFile):
    #blaat
    Result = False
    BESTAND_PARENT = str(pdfFile)
    print ("zoekt "+str(BESTAND_PARENT)+" in Boringen.bestand_gef")
    q = Boring.objects.all().filter(bestand_gef = BESTAND_PARENT[:-4]+".gef") # moet worden bestand_pdf
    if len(q)>0:
        print ("%i pdf gevonden in %s"%(len(q),BESTAND_PARENT))
        q = q[0]
        Result = True
    return Result

# bijwerken van aantal objecten per project en add_message met aantal nieuwe projecten en objecten
def ProjectUpdate(request,d_prj_oud):
    '''Updaten van projectgegevens in projectentabel en printen naar het portaal'''
    # bijwerken projecten overzicht
    d_prj_nieuw = ProjectCount(request)
    print (d_prj_nieuw)
    for project in d_prj_nieuw:
        p = Projecten.objects.get(project_id = project)
        p.aantal_boringen = d_prj_nieuw[project][0]
        p.aantal_sonderingen = d_prj_nieuw[project][1]
        p.aantal_peilbuisputten = d_prj_nieuw[project][2]
        p.aantal_peilbuizen = d_prj_nieuw[project][3]
        p.save()   
        del p
    
    # tel hoeveel nieuwe projecten er zijn bijgekomen
    i_prj_bijgewerkt = len(d_prj_nieuw)-len(d_prj_oud)
    if i_prj_bijgewerkt == 0:
        print_log(request, "INFO", '\nGeen nieuwe projecten toegevoegd!')
    elif i_prj_bijgewerkt == 1:
        print_log(request, "INFO", '\n1 nieuw project toegevoegd:')
    else:
        print_log(request, "INFO", '\n%i nieuwe projecten toegevoegd:'%i_prj_bijgewerkt)
    
    # bepaal welke projecten zijn bijgewerkt in d_prj_bijgewerkt
    i_prj_bijgewerkt=0
    d_prj_bijgewerkt = {}
    for project in d_prj_nieuw: 
        if project in d_prj_oud: # bijgewerkte projecten
            i_bor_oud, i_son_oud, i_pbp_oud, i_pbg_oud = d_prj_oud[project]
            i_bor_nieuw, i_son_nieuw, i_pbp_nieuw, i_pbg_nieuw  = d_prj_nieuw[project]
            i_bor_bijgewerkt = i_bor_nieuw - i_bor_oud
            i_son_bijgewerkt = i_son_nieuw - i_son_oud
            i_pbp_bijgewerkt = i_pbp_nieuw - i_pbp_oud
            i_pbg_bijgewerkt = i_pbg_nieuw - i_pbg_oud
            d_prj_bijgewerkt[project] = [i_bor_bijgewerkt,i_son_bijgewerkt,i_pbp_bijgewerkt,i_pbg_bijgewerkt]
            if i_bor_bijgewerkt != 0 or i_pbp_bijgewerkt != 0 or i_son_bijgewerkt != 0 or i_pbg_bijgewerkt != 0:
                i_prj_bijgewerkt+=1
    
    # print hoeveel projecten zijn bijgewerkt
    if i_prj_bijgewerkt == 0:
        print_log(request, "INFO", 'Geen projecten bijgewerkt!')
    elif i_prj_bijgewerkt == 1:
        print_log(request, "INFO", '1 project bijgewerkt:')
    else:
        print_log(request, "INFO", '%i projecten bijgewerkt:'%i_prj_bijgewerkt)

    i_bor_nieuw_totaal=0
    i_son_nieuw_totaal=0   
    i_pbp_nieuw_totaal=0
    i_pbg_nieuw_totaal=0
    i_bor_bijgewerkt_totaal=0
    i_son_bijgewerkt_totaal=0   
    i_pbp_bijgewerkt_totaal=0
    i_pbg_bijgewerkt_totaal=0
    
    # bereken hoeveel is geupload en send messages
    for project in d_prj_nieuw:
        # print stats voor nieuwe projecten
        if not project in d_prj_oud: 
            i_bor_nieuw, i_son_nieuw, i_pbp_nieuw, i_pbg_nieuw  = d_prj_nieuw[project]
            print_log(request, "INFO", 
                '....nieuw: %s: %i boringen, %i sonderingen,%i peilbuisputten,%i peilbuizen,\
                '%(project,i_bor_nieuw, i_son_nieuw, i_pbp_nieuw, i_pbg_nieuw))
            i_bor_nieuw_totaal += i_bor_nieuw
            i_son_nieuw_totaal += i_son_nieuw
            i_pbp_nieuw_totaal += i_pbp_nieuw
            i_pbg_nieuw_totaal += i_pbg_nieuw
        # print stats voor bijgewerkte projecten
        if project in d_prj_oud: 
            i_bor_bijgewerkt, i_son_bijgewerkt, i_pbp_bijgewerkt, i_pbg_bijgewerkt = d_prj_bijgewerkt[project]
            if i_bor_bijgewerkt != 0 or i_pbp_bijgewerkt != 0 or i_son_bijgewerkt != 0:
                print_log(request, "INFO", 
                    '....bijgewerkt: %s: %i boringen, %i sonderingen, %i peilbuisputten, %i peilbuizen\
                    '%(project,i_bor_bijgewerkt,i_son_bijgewerkt,i_pbp_bijgewerkt,i_pbg_bijgewerkt))
            i_bor_bijgewerkt_totaal += i_bor_bijgewerkt
            i_son_bijgewerkt_totaal += i_son_bijgewerkt
            i_pbp_bijgewerkt_totaal += i_pbp_bijgewerkt
            i_pbg_bijgewerkt_totaal += i_pbg_bijgewerkt
    i_bor_totaal = i_bor_nieuw_totaal + i_bor_bijgewerkt_totaal
    i_son_totaal = i_son_nieuw_totaal + i_son_bijgewerkt_totaal
    i_pbp_totaal = i_pbp_nieuw_totaal + i_pbp_bijgewerkt_totaal
    i_pbg_totaal = i_pbg_nieuw_totaal + i_pbg_bijgewerkt_totaal
    # print totalen
    print_log(request, "INFO", 120*"-")
    print_log(request, "INFO", 
                'Toegevoegd aan nieuwe projecten   : %i boringen, %i sonderingen, %i peilbuisputten, %i peilbuizen\
                '%(i_bor_nieuw_totaal,i_son_nieuw_totaal,i_pbp_nieuw_totaal,i_pbg_nieuw_totaal))
    print_log(request, "INFO", 
                'Toegevoegd aan bestaande projecten: %i boringen, %i sonderingen, %i peilbuisputten, %i peilbuizen\
                '%(i_bor_bijgewerkt_totaal,i_son_bijgewerkt_totaal,i_pbp_bijgewerkt_totaal,i_pbg_bijgewerkt_totaal))
    print_log(request, "INFO", 
                'Totaal aantal toegevoegde objecten: %i boringen, %i sonderingen, %i peilbuisputten, %i peilbuizen\
                '%(i_bor_totaal,i_son_totaal,i_pbp_totaal,i_pbg_totaal))


def ProjectCount(request):
    """geef dictionary terug met aantal objecten per project_id"""
    d_prj = {}
    project_ids = Projecten.objects.filter(user_id_id=request.user.id).values_list('project_id', flat=True) # flat=True voor lijst met single values i.p.v. tuples
    #print (str(projecten))
    for project in project_ids: 
        i_boringen = Boring.objects.filter(project_id=project).count()
        i_peilbuisputten = Peilbuisput.objects.filter(project_id=project).count()
        i_sonderingen = Sondering.objects.filter(project_id=project).count()
        i_peilbuizen = Peilbuisgegevens.objects.filter(project_id=project).count()
        d_prj[project] = [i_boringen,i_sonderingen,i_peilbuisputten,i_peilbuizen] 
        # print ("#boringen:\t\t%s"%i_boringen)
        # print ("#peilbuisputten:\t%s"%i_peilbuisputten)
        # print ("#sonderingen:\t\t%s"%i_sonderingen)
    # print (d_prj)
    return d_prj

def SetActiveProject(ActiveProject):
    """Zet ActiveProject op juist veld"""
    try:
        q_active = Projecten.objects.filter(active=True)
        if len(q_active)>0:
            if q_active == ActiveProject:
                return "gelukt" # breek af, ActiveProject staat al goed.
            else:
                p = Projecten.objects.get(active=True)
                p.active = False
                p.save()
        if len(Projecten.objects.filter(project_id=ActiveProject))>0:
            p = Projecten.objects.get(project_id=ActiveProject)
            p.active = True
            p.save()
            return "gelukt"
        else:
            return "Onverwachte fout: Project komt niet voor in ProjectenTabel!"    
    except Exception as e:
        return e

def GetActiveProject():
    q=Projecten.objects.filter(active=True).values_list('project_id','project_name')#,flat=True)
    print(q)
    if len(q)==0:
        return None
    elif len(q)==1:
        return q[0]
    else:
        return "Er zijn meerdere geactiveerd!" 

def send_email_gefupload():
    # email verzenden werkt nog niet goed, traag, maar lukt soms wel.
   html_header = '''<h1>gefupload in gebruik</h1>'''
   subject = 'Gef upload'
   contact_message = 'Er is een gef-file geupload op het portaal'
   send_mail(subject,
           contact_message,
           settings.EMAIL_HOST_USER,
           ['hhnk.vps@gmail.com'],
           html_message=html_header,
           fail_silently=False)
   print ("email send")
