from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.gis.gdal import DataSource
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib import messages  # example: print_log(request, messages.INFO, 'Hello world.')
from django.template import RequestContext
from django.db import connection # connection to create cursor object te execute SQL
#settings
from django.conf import settings
# email
from django.core.mail import send_mail
# Import system modules
import itertools
import tempfile
import os
import json
import datetime
# Import custom modules
from waypoints.models import Waypoint, Boring, Sondering, Peilbuisput, Projecten
## from .forms import # import form
# Custom scripts 
import Gef2Open as UtlGefOpen
import TestGefData
import logging
from Utl import print_log 
# nodig voor ophalen headerdict 
import pickle
import ast


# Global objects and variables
BASE_DIR = settings.BASE_DIR
logger = logging.getLogger(__name__)
logtime = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
NoActiveProject = 'Selecteer een project in "Mijn projecten"'

def index(request):
    logger.info("refresh index")
    if str(request.user) == "AnonymousUser":
        return HttpResponseRedirect(reverse('auth_login'))
    # global SiteURL
    # global ActiveProject
    SiteURL = str(request.build_absolute_uri())
    if settings.PRODUCTIE:
        Upload_log = 'http://hhnk.bkgis.nl/static/gefupload/media/logging/upload_log.log'
    else:
        Upload_log = SiteURL+'media/logging/upload_log.log'
    try:
        ActiveProjectInfo = request.POST['project']
        ActiveProject = ActiveProjectInfo[:(ActiveProjectInfo.find(":"))] # extraheert tot ":", dus haalt "id" uit "id:naam"
        
    except:
        ActiveProject = NoActiveProject #AANVULLEND GRONDONDERZOEK I.V.M. MER DIJKVERSTERKING HOORN-EDAM' 
        ActiveProjectInfo = NoActiveProject
    SetProj = TestGefData.SetActiveProject(ActiveProject)
    if SetProj != "gelukt":
        print_log (request,"Error",SetProj)
    waypoints = Waypoint.objects.order_by('name')
    projecten = Projecten.objects.order_by("project_id")
    template = loader.get_template('home.html')
    #template = loader.get_template('waypoints/index.html')
    title = 'Upload Portaal GEF-bestanden'
    context = RequestContext(request, {
        'Upload_log' : Upload_log,
        'SiteURL' : SiteURL,
        'ActiveProjectInfo' : ActiveProjectInfo,
        'ActiveProject': ActiveProject,
        'title' : title,
        'waypoints': waypoints,
        'projecten': projecten,
        'content': render_to_string('waypoints.html', {'waypoints': waypoints})
    })
    return HttpResponse(template.render(context))

@csrf_exempt
################## doesnt work without the @csrf_exempt.  Have to figure out why this is the case#########

def delete(request): # delete all user data
    cursor = connection.cursor()
    if request.user.is_authenticated():
        UserName = request.user.username
        UserId = str(request.user.id)
    else:
        UserName = "AnonymousUser"
        UserId = str(13)
    cursor.execute("DELETE FROM waypoints_boring WHERE username = '" + UserName + "';"+
                   "DELETE FROM waypoints_sondering WHERE username = '" + UserName + "';"+
                   "DELETE FROM waypoints_peilbuisput WHERE username = '" + UserName + "';"+
                   "DELETE FROM waypoints_peilbuisgegevens WHERE username = '" + UserName + "';"+
                   "DELETE FROM waypoints_waypoint WHERE username = '" + UserName + "';"+
                   "DELETE FROM waypoints_projecten WHERE user_id_id = '" + UserId + "';")
    return HttpResponseRedirect(reverse('waypoints-index'))

def del_project(request): # delete active project 
    logger.info("this is an info message!")
    cursor = connection.cursor()
    ActiveProject = TestGefData.GetActiveProject()[0] # [0] = ProjectiD, [1] = ProjectName
    if ActiveProject != NoActiveProject:
        print_log(request, "SUCCESS", '%s succesvol verwijderd!'%ActiveProject)	
        cursor.execute("DELETE FROM waypoints_boring WHERE project_id = '" + ActiveProject + "';"+
                       "DELETE FROM waypoints_sondering WHERE project_id = '" + ActiveProject + "';"+
                       "DELETE FROM waypoints_peilbuisput WHERE project_id = '" + ActiveProject + "';"+
                       "DELETE FROM waypoints_waypoint WHERE project_id = '" + ActiveProject + "';"+
                       "DELETE FROM waypoints_projecten WHERE project_id = '" + ActiveProject + "';")
    else:
        print_log(request, "ERROR", 'Geen project verwijderd.\n\
                                                        Selecteer een project in "Mijn projecten".\n\
                                                        Druk op "F5" (refresh) en vervolgens op \
                                                        "verwijder huidige project" om een project te verwijderen')
    return HttpResponseRedirect(reverse('waypoints-index'))

def truncate(request):
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE waypoints_boring CASCADE;
                      TRUNCATE TABLE waypoints_peilbuisput CASCADE;
                      TRUNCATE TABLE waypoints_peilbuisgegevens CASCADE;
                      TRUNCATE TABLE waypoints_sondering CASCADE;
                      TRUNCATE TABLE waypoints_waypoint;
                      TRUNCATE TABLE waypoints_projecten;""")
    return HttpResponseRedirect(reverse('waypoints-index'))

def opleveren(request):
    ActiveProject = TestGefData.GetActiveProject()[0] # [0] = ProjectiD, [1] = ProjectName
    if ActiveProject != NoActiveProject:    
        p = Projecten.objects.get(project_name = ActiveProject)
        p.project_status = "opgeleverd"
        p.save()
        print_log(request, "SUCCESS", 'Bedankt! Project "%s" is succesvol opgeleverd! \n\
            We nemen zo spoedig mogelijk contact met u up!'%ActiveProject)
        # email verzenden werkt nog niet goed, traag, soms wel.
        html_header = '''<h1>Project opgeleverd</h1>'''
        subject = 'Project opgeleverd'
        contact_message = 'Project "%s" is opgeleverd door gebruiker: "%s"'%(ActiveProject,request.user.username)
        send_mail(subject,
               contact_message,
               settings.EMAIL_HOST_USER,
               ['bart.kropf@gmail.com'],
               # html_message=html_header,
               fail_silently=False)
        print ("email send")
        logger.info("email_verzonden!")
    return HttpResponseRedirect(reverse('waypoints-index'))

def search(request):
    # Build searchPoint
    try:
        searchPoint = Point(float(request.GET.get('lng')), float(request.GET.get('lat')))
    except:
        return HttpResponse(json.dumps(dict(isOk=0, message='Could not parse search point')))
    # Search database
    waypoints = Waypoint.objects.distance(searchPoint).order_by('distance')
    # Return
    return HttpResponse(json.dumps(dict(
        isOk=1,
        content=render_to_string('waypoints/waypoints.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )))

def upload(request):
    '''Behandeld geuploade gef- of pdf-bestanden met behulp van verschillende functies. 
        Houdt bij hoeveel objecten er zijn in projecten, haalt dictonary uit UtlGefOpen, 
        regelt gef-check en opslaan in TestGefData.'''
    
    # open upload logfile en truncate file
    file = settings.UPLOAD_LOGFILE
    upload_log = open(file, "w+")
    upload_log.write("fouten bij gef-upload: "+logtime+"\n\n")
    upload_log.close()

    # tel aantal projecten
    d_projecten_start = TestGefData.ProjectCount(request)
    i_object_fout = 0 # aantal objecten met fouten niet aantal fouten
    if 'gef' in request.FILES:
        try:
            gefTest = request.FILES['gef']
        except IOError:
            print("gef")

        for File in request.FILES.getlist('gef'):
            print (str(File))
            if str(File)[-3:].lower() == "gef":
                gefFile = File
                files = []
                handle, targetPath = tempfile.mkstemp()
                destination = os.fdopen(handle, 'wb')
                for chunk in gefFile.chunks():
                    destination.write(chunk)
                    files.append(targetPath)
                destination.close()

                try:
                    #1.) Header dictionary maken van GEF met UtlGefOpen/Gef2Open
                    UtlGefOpen.read_gef(targetPath) # genereert tmpheaderdict.pk1
                    d_GEF = UtlGefOpen.d_GEF() 
                    
                    # 2.) controleer en save gef.
                    if not TestGefData.gef_main(request,gefFile,d_GEF): 
                        i_object_fout += 1

                except Exception as e:
                    print_log(request, "ERROR", 'fout bij uitlezen gef, %s'%gefFile)
                    print_log(request, "ERROR", str(e))

            elif str(File)[-3:] == "pdf":
                pdfFile = File
                pdfFileNaam = str(pdfFile)
                Hyperlink_root = TestGefData.Get_hyperlink_root(request)
                #print (str(gefFile))
                files = []
                handle, targetPath = tempfile.mkstemp()
                destination = os.fdopen(handle, 'wb')
                for chunk in pdfFile.chunks():
                    destination.write(chunk)
                    files.append(targetPath)
                destination.close()
                gefFileNaam = str(pdfFile)[:-3]+"gef"
                if Boring.objects.filter(bestand_gef=gefFileNaam).exists():
                    b = Boring.objects.get(bestand_gef=gefFileNaam)
                    print (pdfFile)
                    b.gef_file=pdfFile
                    b.bestand_pdf=(Hyperlink_root+pdfFileNaam)
                    b.save()
                    print_log(request, "SUCCESS", '%s succesvol opgeslagen! Bijbehorende boring gevonden'%File)
                elif Sondering.objects.filter(bestand_gef=gefFileNaam).exists():
                    s = Sondering.objects.get(bestand_gef=gefFileNaam)
                    s.gef_file=pdfFile
                    s.bestand_pdf=(Hyperlink_root+pdfFileNaam)
                    s.save()  
                    print_log(request, "SUCCESS", '%s succesvol opgeslagen! Bijbehorende boring gevonden'%File)
                # if TestGefData.pdf_check(request, gefFile):  # overbodig geworden check...
                else:
                    print_log(request, "ERROR", '%s niet opgeslagen, geen bijbehorende boring gevonden'%File)

        print_log(request,"INFO",120*"-")
        print_log(request,"INFO","%i objecten met fouten gevonden\n"%(i_object_fout))

        # update projecten
        TestGefData.ProjectUpdate(request,d_projecten_start) # i.p.v. trigger
        
        # close log
        upload_log.close()

    return HttpResponseRedirect(reverse('waypoints-index'))

def contact(request):
    return render_to_response('contact.html')

def geoportaal(request):
    return render_to_response('geoportaal.html')

def levering(request):
    return render_to_response('project_form.html')


