import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

import jiji.wsgi as w
application = w.application
