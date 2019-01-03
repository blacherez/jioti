# -*- coding: UTF-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONNEMENT = "staging"

ALLOWED_HOSTS = ["jioti-staging.benoit.wtf"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = 'https://jioti-static.benoit.wtf/staging/'
STATIC_ROOT = '/home/blacherez/jioti-static.benoit.wtf/staging/'

MEDIA_URL = 'https://jioti-static.benoit.wtf/staging/media/'
MEDIA_ROOT = "/home/blacherez/jioti-static.benoit.wtf/staging/media/"
