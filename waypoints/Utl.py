#-------------------------------------------------------------------------------
# Name:         Utl
# Purpose:      Algemene utilities
#
# Author:      Bart
#
# Created:     31-10-2015
# Copyright:   (c) Bart 2015
# Licence:     to rock
#-------------------------------------------------------------------------------


# import system modules
import os, sys
# import django modules
from django.contrib import messages
from django.conf import settings
import logging

# Global objects and variables
logger = logging.getLogger(__name__)

def print_log(request,message_type,text):
	if message_type == "DEBUG":
		logger.debug(text)
		messages.debug(request,text)
	if message_type == "INFO":
		logger.info(text)
		messages.info(request,text) # Blauw op het scherm.
		file = settings.UPLOAD_LOGFILE
		if os.path.exists(file):
			upload_log = open(file, "a")
			upload_log.write(text+"\n")
	if message_type == "SUCCESS":
		logger.info(text) # logger heeft geen "success" attribute, daarom als "info"
		messages.success(request,text) # Groen op het scherm
	if message_type == "WARNING":
		logger.warning(text)
		messages.warning(request,text)
	if message_type == "ERROR":
		file = settings.UPLOAD_LOGFILE
		if os.path.exists(file):
			upload_log = open(file, "a")
			upload_log.write(text+"\n")
		logger.error(text)
		messages.error(request,text) # Rood op het scherm


