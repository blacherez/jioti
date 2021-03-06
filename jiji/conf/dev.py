# -*- coding: UTF-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT = "dev"

ALLOWED_HOSTS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/static/media/"
MEDIA_ROOT = "licornes/static/media/"
